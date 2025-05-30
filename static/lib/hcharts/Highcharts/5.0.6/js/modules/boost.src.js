/**
 * @license Highcharts JS v5.0.6 (2016-12-07)
 * Boost module
 *
 * (c) 2010-2016 Highsoft AS
 * Author: Torstein Honsi
 *
 * License: www.highcharts.com/license
 */
(function(factory) {
    if (typeof module === 'object' && module.exports) {
        module.exports = factory;
    } else {
        factory(Highcharts);
    }
}(function(Highcharts) {
    (function(H) {
        /**
         * License: www.highcharts.com/license
         * Author: Torstein Honsi
         * 
         * This is an experimental Highcharts module that draws long data series on a canvas
         * in order to increase performance of the initial load time and tooltip responsiveness.
         *
         * Compatible with HTML5 canvas compatible browsers (not IE < 9).
         *
         *
         * 
         * Development plan
         * - Column range.
         * - Heatmap. Modify the heatmap-canvas hotel so that it uses this module.
         * - Treemap.
         * - Check how it works with Highstock and data grouping. Currently it only works when navigator.adaptToUpdatedData
         *   is false. It is also recommended to set scrollbar.liveRedraw to false.
         * - Check inverted charts.
         * - Check reversed axes.
         * - Chart callback should be async after last series is drawn. (But not necessarily, we don't do
        	 that with initial series animation).
         * - Cache full-size image so we don't have to redraw on hide/show and zoom up. But k-d-tree still
         *   needs to be built.
         * - Test IE9 and IE10.
         * - Stacking is not perhaps not correct since it doesn't use the translation given in 
         *   the translate method. If this gets to complicated, a possible way out would be to 
         *   have a simplified renderCanvas method that simply draws the areaPath on a canvas.
         *
         * If this module is taken in as part of the core
         * - All the loading logic should be merged with core. Update styles in the core.
         * - Most of the method wraps should probably be added directly in parent methods.
         *
         * Notes for boost mode
         * - Area lines are not drawn
         * - Point markers are not drawn on line-type series
         * - Lines are not drawn on scatter charts
         * - Zones and negativeColor don't work
         * - Initial point colors aren't rendered
         * - Columns are always one pixel wide. Don't set the threshold too low.
         *
         * Optimizing tips for users
         * - For scatter plots, use a marker.radius of 1 or less. It results in a rectangle being drawn, which is 
         *   considerably faster than a circle.
         * - Set extremes (min, max) explicitly on the axes in order for Highcharts to avoid computing extremes.
         * - Set enableMouseTracking to false on the series to improve total rendering time.
         * - The default threshold is set based on one series. If you have multiple, dense series, the combined
         *   number of points drawn gets higher, and you may want to set the threshold lower in order to 
         *   use optimizations.
         */

        'use strict';

        var win = H.win,
            doc = win.document,
            noop = function() {},
            Color = H.Color,
            Series = H.Series,
            seriesTypes = H.seriesTypes,
            each = H.each,
            extend = H.extend,
            addEvent = H.addEvent,
            fireEvent = H.fireEvent,
            grep = H.grep,
            isNumber = H.isNumber,
            merge = H.merge,
            pick = H.pick,
            wrap = H.wrap,
            plotOptions = H.getOptions().plotOptions,
            CHUNK_SIZE = 50000,
            destroyLoadingDiv;

        function eachAsync(arr, fn, finalFunc, chunkSize, i) {
            i = i || 0;
            chunkSize = chunkSize || CHUNK_SIZE;

            var threshold = i + chunkSize,
                proceed = true;

            while (proceed && i < threshold && i < arr.length) {
                proceed = fn(arr[i], i);
                i = i + 1;
            }
            if (proceed) {
                if (i < arr.length) {
                    setTimeout(function() {
                        eachAsync(arr, fn, finalFunc, chunkSize, i);
                    });
                } else if (finalFunc) {
                    finalFunc();
                }
            }
        }

        // Set default options
        each(
            ['area', 'arearange', 'bubble', 'column', 'line', 'scatter'],
            function(type) {
                if (plotOptions[type]) {
                    plotOptions[type].boostThreshold = 5000;
                }
            }
        );

        /**
         * Override a bunch of methods the same way. If the number of points is below the threshold,
         * run the original method. If not, check for a canvas version or do nothing.
         */
        each(['translate', 'generatePoints', 'drawTracker', 'drawPoints', 'render'], function(method) {
            function branch(proceed) {
                var letItPass = this.options.stacking && (method === 'translate' || method === 'generatePoints');
                if ((this.processedXData || this.options.data).length < (this.options.boostThreshold || Number.MAX_VALUE) ||
                    letItPass) {

                    // Clear image
                    if (method === 'render' && this.image) {
                        this.image.attr({
                            href: ''
                        });
                        this.animate = null; // We're zooming in, don't run animation
                    }

                    proceed.call(this);

                    // If a canvas version of the method exists, like renderCanvas(), run
                } else if (this[method + 'Canvas']) {

                    this[method + 'Canvas']();
                }
            }
            wrap(Series.prototype, method, branch);

            // A special case for some types - its translate method is already wrapped
            if (method === 'translate') {
                each(['arearange', 'bubble', 'column'], function(type) {
                    if (seriesTypes[type]) {
                        wrap(seriesTypes[type].prototype, method, branch);
                    }
                });
            }
        });

        /**
         * Do not compute extremes when min and max are set.
         * If we use this in the core, we can add the hook to hasExtremes to the methods directly.
         */
        wrap(Series.prototype, 'getExtremes', function(proceed) {
            if (!this.hasExtremes()) {
                proceed.apply(this, Array.prototype.slice.call(arguments, 1));
            }
        });
        wrap(Series.prototype, 'setData', function(proceed) {
            if (!this.hasExtremes(true)) {
                proceed.apply(this, Array.prototype.slice.call(arguments, 1));
            }
        });
        wrap(Series.prototype, 'processData', function(proceed) {
            if (!this.hasExtremes(true)) {
                proceed.apply(this, Array.prototype.slice.call(arguments, 1));
            }
        });


        H.extend(Series.prototype, {
            pointRange: 0,
            allowDG: false, // No data grouping, let boost handle large data 
            hasExtremes: function(checkX) {
                var options = this.options,
                    data = options.data,
                    xAxis = this.xAxis && this.xAxis.options,
                    yAxis = this.yAxis && this.yAxis.options;
                return data.length > (options.boostThreshold || Number.MAX_VALUE) && isNumber(yAxis.min) && isNumber(yAxis.max) &&
                    (!checkX || (isNumber(xAxis.min) && isNumber(xAxis.max)));
            },

            /**
             * If implemented in the core, parts of this can probably be shared with other similar
             * methods in Highcharts.
             */
            destroyGraphics: function() {
                var series = this,
                    points = this.points,
                    point,
                    i;

                if (points) {
                    for (i = 0; i < points.length; i = i + 1) {
                        point = points[i];
                        if (point && point.graphic) {
                            point.graphic = point.graphic.destroy();
                        }
                    }
                }

                each(['graph', 'area', 'tracker'], function(prop) {
                    if (series[prop]) {
                        series[prop] = series[prop].destroy();
                    }
                });
            },

            /**
             * Create a hidden canvas to draw the graph on. The contents is later copied over 
             * to an SVG image element.
             */
            getContext: function() {
                var chart = this.chart,
                    width = chart.plotWidth,
                    height = chart.plotHeight,
                    ctx = this.ctx,
                    swapXY = function(proceed, x, y, a, b, c, d) {
                        proceed.call(this, y, x, a, b, c, d);
                    };

                if (!this.canvas) {
                    this.canvas = doc.createElement('canvas');
                    this.image = chart.renderer.image('', 0, 0, width, height).add(this.group);
                    this.ctx = ctx = this.canvas.getContext('2d');
                    if (chart.inverted) {
                        each(['moveTo', 'lineTo', 'rect', 'arc'], function(fn) {
                            wrap(ctx, fn, swapXY);
                        });
                    }
                } else {
                    ctx.clearRect(0, 0, width, height);
                }

                this.canvas.width = width;
                this.canvas.height = height;
                this.image.attr({
                    width: width,
                    height: height
                });

                return ctx;
            },

            /** 
             * Draw the canvas image inside an SVG image
             */
            canvasToSVG: function() {
                this.image.attr({
                    href: this.canvas.toDataURL('image/png')
                });
            },

            cvsLineTo: function(ctx, clientX, plotY) {
                ctx.lineTo(clientX, plotY);
            },

            renderCanvas: function() {
                var series = this,
                    options = series.options,
                    chart = series.chart,
                    xAxis = this.xAxis,
                    yAxis = this.yAxis,
                    ctx,
                    c = 0,
                    xData = series.processedXData,
                    yData = series.processedYData,
                    rawData = options.data,
                    xExtremes = xAxis.getExtremes(),
                    xMin = xExtremes.min,
                    xMax = xExtremes.max,
                    yExtremes = yAxis.getExtremes(),
                    yMin = yExtremes.min,
                    yMax = yExtremes.max,
                    pointTaken = {},
                    lastClientX,
                    sampling = !!series.sampling,
                    points,
                    r = options.marker && options.marker.radius,
                    cvsDrawPoint = this.cvsDrawPoint,
                    cvsLineTo = options.lineWidth ? this.cvsLineTo : false,
                    cvsMarker = r && r <= 1 ?
                    this.cvsMarkerSquare :
                    this.cvsMarkerCircle,
                    strokeBatch = this.cvsStrokeBatch || 1000,
                    enableMouseTracking = options.enableMouseTracking !== false,
                    lastPoint,
                    threshold = options.threshold,
                    yBottom = yAxis.getThreshold(threshold),
                    hasThreshold = isNumber(threshold),
                    translatedThreshold = yBottom,
                    doFill = this.fill,
                    isRange = series.pointArrayMap && series.pointArrayMap.join(',') === 'low,high',
                    isStacked = !!options.stacking,
                    cropStart = series.cropStart || 0,
                    loadingOptions = chart.options.loading,
                    requireSorting = series.requireSorting,
                    wasNull,
                    connectNulls = options.connectNulls,
                    useRaw = !xData,
                    minVal,
                    maxVal,
                    minI,
                    maxI,
                    fillColor = series.fillOpacity ?
                    new Color(series.color).setOpacity(pick(options.fillOpacity, 0.75)).get() :
                    series.color,
                    stroke = function() {
                        if (doFill) {
                            ctx.fillStyle = fillColor;
                            ctx.fill();
                        } else {
                            ctx.strokeStyle = series.color;
                            ctx.lineWidth = options.lineWidth;
                            ctx.stroke();
                        }
                    },
                    drawPoint = function(clientX, plotY, yBottom, i) {
                        if (c === 0) {
                            ctx.beginPath();

                            if (cvsLineTo) {
                                ctx.lineJoin = 'round';
                            }
                        }

                        if (wasNull) {
                            ctx.moveTo(clientX, plotY);
                        } else {
                            if (cvsDrawPoint) {
                                cvsDrawPoint(ctx, clientX, plotY, yBottom, lastPoint);
                            } else if (cvsLineTo) {
                                cvsLineTo(ctx, clientX, plotY);
                            } else if (cvsMarker) {
                                cvsMarker.call(series, ctx, clientX, plotY, r, i);
                            }
                        }

                        // We need to stroke the line for every 1000 pixels. It will crash the browser
                        // memory use if we stroke too infrequently.
                        c = c + 1;
                        if (c === strokeBatch) {
                            stroke();
                            c = 0;
                        }

                        // Area charts need to keep track of the last point
                        lastPoint = {
                            clientX: clientX,
                            plotY: plotY,
                            yBottom: yBottom
                        };
                    },

                    addKDPoint = function(clientX, plotY, i) {

                        // The k-d tree requires series points. Reduce the amount of points, since the time to build the 
                        // tree increases exponentially.
                        if (enableMouseTracking && !pointTaken[clientX + ',' + plotY]) {
                            pointTaken[clientX + ',' + plotY] = true;

                            if (chart.inverted) {
                                clientX = xAxis.len - clientX;
                                plotY = yAxis.len - plotY;
                            }

                            points.push({
                                clientX: clientX,
                                plotX: clientX,
                                plotY: plotY,
                                i: cropStart + i
                            });
                        }
                    };

                // If we are zooming out from SVG mode, destroy the graphics
                if (this.points || this.graph) {
                    this.destroyGraphics();
                }

                // The group
                series.plotGroup(
                    'group',
                    'series',
                    series.visible ? 'visible' : 'hidden',
                    options.zIndex,
                    chart.seriesGroup
                );

                series.markerGroup = series.group;
                addEvent(series, 'destroy', function() {
                    series.markerGroup = null;
                });

                points = this.points = [];
                ctx = this.getContext();
                series.buildKDTree = noop; // Do not start building while drawing 

                // Display a loading indicator
                if (rawData.length > 99999) {
                    chart.options.loading = merge(loadingOptions, {
                        labelStyle: {
                            backgroundColor: H.color('#ffffff').setOpacity(0.75).get(),
                            padding: '1em',
                            borderRadius: '0.5em'
                        },
                        style: {
                            backgroundColor: 'none',
                            opacity: 1
                        }
                    });
                    clearTimeout(destroyLoadingDiv);
                    chart.showLoading('Drawing...');
                    chart.options.loading = loadingOptions; // reset
                }

                // Loop over the points
                eachAsync(isStacked ? series.data : (xData || rawData), function(d, i) {
                    var x,
                        y,
                        clientX,
                        plotY,
                        isNull,
                        low,
                        chartDestroyed = typeof chart.index === 'undefined',
                        isYInside = true;

                    if (!chartDestroyed) {
                        if (useRaw) {
                            x = d[0];
                            y = d[1];
                        } else {
                            x = d;
                            y = yData[i];
                        }

                        // Resolve low and high for range series
                        if (isRange) {
                            if (useRaw) {
                                y = d.slice(1, 3);
                            }
                            low = y[0];
                            y = y[1];
                        } else if (isStacked) {
                            x = d.x;
                            y = d.stackY;
                            low = y - d.y;
                        }

                        isNull = y === null;

                        // Optimize for scatter zooming
                        if (!requireSorting) {
                            isYInside = y >= yMin && y <= yMax;
                        }

                        if (!isNull && x >= xMin && x <= xMax && isYInside) {

                            clientX = Math.round(xAxis.toPixels(x, true));

                            if (sampling) {
                                if (minI === undefined || clientX === lastClientX) {
                                    if (!isRange) {
                                        low = y;
                                    }
                                    if (maxI === undefined || y > maxVal) {
                                        maxVal = y;
                                        maxI = i;
                                    }
                                    if (minI === undefined || low < minVal) {
                                        minVal = low;
                                        minI = i;
                                    }

                                }
                                if (clientX !== lastClientX) { // Add points and reset
                                    if (minI !== undefined) { // then maxI is also a number
                                        plotY = yAxis.toPixels(maxVal, true);
                                        yBottom = yAxis.toPixels(minVal, true);
                                        drawPoint(
                                            clientX,
                                            hasThreshold ? Math.min(plotY, translatedThreshold) : plotY,
                                            hasThreshold ? Math.max(yBottom, translatedThreshold) : yBottom,
                                            i
                                        );
                                        addKDPoint(clientX, plotY, maxI);
                                        if (yBottom !== plotY) {
                                            addKDPoint(clientX, yBottom, minI);
                                        }
                                    }


                                    minI = maxI = undefined;
                                    lastClientX = clientX;
                                }
                            } else {
                                plotY = Math.round(yAxis.toPixels(y, true));
                                drawPoint(clientX, plotY, yBottom, i);
                                addKDPoint(clientX, plotY, i);
                            }
                        }
                        wasNull = isNull && !connectNulls;

                        if (i % CHUNK_SIZE === 0) {
                            series.canvasToSVG();
                        }
                    }

                    return !chartDestroyed;
                }, function() {
                    var loadingDiv = chart.loadingDiv,
                        loadingShown = chart.loadingShown;
                    stroke();
                    series.canvasToSVG();

                    fireEvent(series, 'renderedCanvas');

                    // Do not use chart.hideLoading, as it runs JS animation and will be blocked by buildKDTree.
                    // CSS animation looks good, but then it must be deleted in timeout. If we add the module to core,
                    // change hideLoading so we can skip this block.
                    if (loadingShown) {
                        extend(loadingDiv.style, {
                            transition: 'opacity 250ms',
                            opacity: 0
                        });
                        chart.loadingShown = false;
                        destroyLoadingDiv = setTimeout(function() {
                            if (loadingDiv.parentNode) { // In exporting it is falsy
                                loadingDiv.parentNode.removeChild(loadingDiv);
                            }
                            chart.loadingDiv = chart.loadingSpan = null;
                        }, 250);
                    }

                    // Pass tests in Pointer. 
                    // Replace this with a single property, and replace when zooming in
                    // below boostThreshold.
                    series.directTouch = false;
                    series.options.stickyTracking = true;

                    delete series.buildKDTree; // Go back to prototype, ready to build
                    series.buildKDTree();

                    // Don't do async on export, the exportChart, getSVGForExport and getSVG methods are not chained for it.
                }, chart.renderer.forExport ? Number.MAX_VALUE : undefined);
            }
        });

        seriesTypes.scatter.prototype.cvsMarkerCircle = function(ctx, clientX, plotY, r) {
            ctx.moveTo(clientX, plotY);
            ctx.arc(clientX, plotY, r, 0, 2 * Math.PI, false);
        };

        // Rect is twice as fast as arc, should be used for small markers
        seriesTypes.scatter.prototype.cvsMarkerSquare = function(ctx, clientX, plotY, r) {
            ctx.rect(clientX - r, plotY - r, r * 2, r * 2);
        };
        seriesTypes.scatter.prototype.fill = true;

        if (seriesTypes.bubble) {
            seriesTypes.bubble.prototype.cvsMarkerCircle = function(ctx, clientX, plotY, r, i) {
                ctx.moveTo(clientX, plotY);
                ctx.arc(clientX, plotY, this.radii && this.radii[i], 0, 2 * Math.PI, false);
            };
            seriesTypes.bubble.prototype.cvsStrokeBatch = 1;
        }


        extend(seriesTypes.area.prototype, {
            cvsDrawPoint: function(ctx, clientX, plotY, yBottom, lastPoint) {
                if (lastPoint && clientX !== lastPoint.clientX) {
                    ctx.moveTo(lastPoint.clientX, lastPoint.yBottom);
                    ctx.lineTo(lastPoint.clientX, lastPoint.plotY);
                    ctx.lineTo(clientX, plotY);
                    ctx.lineTo(clientX, yBottom);
                }
            },
            fill: true,
            fillOpacity: true,
            sampling: true
        });

        extend(seriesTypes.column.prototype, {
            cvsDrawPoint: function(ctx, clientX, plotY, yBottom) {
                ctx.rect(clientX - 1, plotY, 1, yBottom - plotY);
            },
            fill: true,
            sampling: true
        });

        /**
         * Return a full Point object based on the index. The boost module uses stripped point objects
         * for performance reasons.
         * @param   {Number} boostPoint A stripped-down point object
         * @returns {Object}   A Point object as per http://api.highcharts.com/highcharts#Point
         */
        Series.prototype.getPoint = function(boostPoint) {
            var point = boostPoint;

            if (boostPoint && !(boostPoint instanceof this.pointClass)) {
                point = (new this.pointClass()).init(this, this.options.data[boostPoint.i]); // eslint-disable-line new-cap
                point.category = point.x;

                point.dist = boostPoint.dist;
                point.distX = boostPoint.distX;
                point.plotX = boostPoint.plotX;
                point.plotY = boostPoint.plotY;
            }

            return point;
        };

        /**
         * Extend series.destroy to also remove the fake k-d-tree points (#5137). Normally
         * this is handled by Series.destroy that calls Point.destroy, but the fake
         * search points are not registered like that.
         */
        wrap(Series.prototype, 'destroy', function(proceed) {
            var series = this,
                chart = series.chart;
            if (chart.hoverPoints) {
                chart.hoverPoints = grep(chart.hoverPoints, function(point) {
                    return point.series === series;
                });
            }

            if (chart.hoverPoint && chart.hoverPoint.series === series) {
                chart.hoverPoint = null;
            }
            proceed.call(this);
        });

        /**
         * Return a point instance from the k-d-tree
         */
        wrap(Series.prototype, 'searchPoint', function(proceed) {
            return this.getPoint(
                proceed.apply(this, [].slice.call(arguments, 1))
            );
        });

    }(Highcharts));
}));
