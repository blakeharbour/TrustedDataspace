try:
    from matplotlib import use

    use('TkAgg')
except ImportError:
    pass
import matplotlib.pyplot as plt


def draw_losses_test_data(data_name, nnpu_test, nnpusb_test, is_train='Train'):
    plots = []
    legend = []
    title = data_name.upper() + ':'+is_train+' Loss'

    nnpn_test_plot, = plt.plot(nnpu_test, 'r-')
    nnpusb_test_plot, = plt.plot(nnpusb_test, 'b-')
    plots.extend([nnpn_test_plot, nnpusb_test_plot])
    legend.extend(['ImnnPU '+is_train, 'ImnnPUSB '+is_train])

    plt.legend(
        plots,
        legend,
        loc='upper right'
    )
    plt.title(title)
    plt.xlabel('Epoch')
    plt.ylabel(is_train+' Loss')
    plt.grid(True, linestyle="-.")
    plt.savefig("./result/loss_"+is_train+".png")
    plt.show()


def draw_error_test_data(data_name, nnpu_test, nnpusb_test):
    plots = []
    legend = []
    title = data_name.upper() + ':Test Error Rate'

    nnpn_test_plot, = plt.plot(nnpu_test, 'r-')
    nnpusb_test_plot, = plt.plot(nnpusb_test, 'b-')
    plots.extend([nnpn_test_plot, nnpusb_test_plot])
    legend.extend(['ImnnPU test', 'ImnnPUSB test'])

    plt.legend(
        plots,
        legend,
        loc='upper right'
    )
    plt.title(title)
    plt.xlabel('Epoch')
    plt.ylabel('Test Error')
    plt.grid(True, linestyle="-.")
    plt.savefig("./result/error_rate.png")
    plt.show()


def draw_precision_recall(data_name, nnpu_precision, nnpu_recall, nnpusb_precision, nnpusb_recall):
    plots = []
    legend = []
    title = data_name.upper() + ':Precision and Recall'

    nnpn_precision_plot, = plt.plot(nnpu_precision, 'r-')
    nnpn_recall_plot, = plt.plot(nnpu_recall, 'g--')

    nnpusb_precision_plot, = plt.plot(nnpusb_precision, 'b-')
    nnpusb_recall_plot, = plt.plot(nnpusb_recall, 'y--')

    plots.extend([nnpn_precision_plot, nnpn_recall_plot,
                  nnpusb_precision_plot, nnpusb_recall_plot])
    legend.extend(['ImnnPU: Precision', 'ImnnPU: Recall',
                   'ImnnPUSB: Precision', 'ImnnPUSB: Recall'])

    plt.legend(
        plots,
        legend,
        loc='upper right'
    )
    plt.title(title)
    plt.xlabel('Epoch')
    plt.ylabel('Value')
    plt.grid(True, linestyle="-.")
    plt.savefig("./result/precision_recall.png")
    plt.show()
