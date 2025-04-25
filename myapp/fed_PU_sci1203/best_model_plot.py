import pickle

from plot import draw_losses_test_data, draw_error_test_data, draw_precision_recall


if __name__ == '__main__':
    data_name = 'container'

    with open('best_model/imbalancednnPUSB/test_result.pkl', 'rb') as f:
        nnPUSB_result = pickle.load(f)

    with open('best_model/imbalancednnPU/test_result.pkl', 'rb') as f:
        nnPU_result = pickle.load(f)

    draw_losses_test_data(data_name, nnPU_result[4], nnPUSB_result[4])
    draw_losses_test_data(data_name, nnPU_result[3], nnPUSB_result[3], is_train="Test")
    draw_error_test_data(data_name, nnPU_result[2], nnPUSB_result[2])
    draw_precision_recall(
        data_name, nnPU_result[0], nnPU_result[1], nnPUSB_result[0], nnPUSB_result[1])