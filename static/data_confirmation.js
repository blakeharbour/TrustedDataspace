// 数据确权模块的JavaScript交互代码
$(document).ready(function() {

    // 筛选表单的自动提交
    $('.form-inline select').change(function() {
        $(this).closest('form').submit();
    });

    // 日期选择器变更时自动提交
    $('input[type="date"]').change(function() {
        if ($(this).val() !== '') {
            $(this).closest('form').submit();
        }
    });

    // 详情展示逻辑
    $('.show-details').click(function(e) {
        e.preventDefault();
        var targetId = $(this).data('target');
        $('#' + targetId).slideToggle();
    });

    // 批准申请前的确认
    $('.approve-request-btn').click(function() {
        return confirm('确定要批准此申请吗？');
    });

    // 拒绝申请前的确认
    $('.reject-request-btn').click(function() {
        // 检查是否有拒绝原因
        var remarkField = $(this).closest('form').find('textarea[name="remark"]');
        if (remarkField.val().trim() === '') {
            alert('请填写拒绝原因');
            remarkField.focus();
            return false;
        }
        return confirm('确定要拒绝此申请吗？');
    });

    // 模态框功能增强
    $('[data-toggle="modal"]').click(function() {
        var target = $(this).data('target');
        $(target).modal('show');
    });

    // 数据表格初始化
    if($.fn.dataTable) {
        $('.table-sort').dataTable({
            "aaSorting": [[ 0, "desc" ]],
            "bStateSave": true,
            "aoColumnDefs": [
                {"orderable":false, "aTargets":[5]}
            ],
            "language": {
                "sProcessing":   "处理中...",
                "sLengthMenu":   "显示 _MENU_ 项结果",
                "sZeroRecords":  "没有匹配结果",
                "sInfo":         "显示第 _START_ 至 _END_ 项结果，共 _TOTAL_ 项",
                "sInfoEmpty":    "显示第 0 至 0 项结果，共 0 项",
                "sInfoFiltered": "(由 _MAX_ 项结果过滤)",
                "sInfoPostFix":  "",
                "sSearch":       "搜索:",
                "sUrl":          "",
                "sEmptyTable":     "表中数据为空",
                "sLoadingRecords": "载入中...",
                "sInfoThousands":  ",",
                "oPaginate": {
                    "sFirst":    "首页",
                    "sPrevious": "上页",
                    "sNext":     "下页",
                    "sLast":     "末页"
                }
            }
        });
    }
});

// 显示申请详情模态框
function showDetails(id) {
    $("#detailsModal" + id).modal("show");
}

// 显示批准申请模态框
function showApproveModal(id) {
    $("#approveModal" + id).modal("show");
}

// 显示拒绝申请模态框
function showRejectModal(id) {
    $("#rejectModal" + id).modal("show");
}