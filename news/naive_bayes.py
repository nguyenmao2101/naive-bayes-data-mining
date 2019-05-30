import pickle
import numpy as np
from collections import defaultdict

def split_with_label(dataset):
    """Trả về index dòng dữ liệu trong các nhóm có nhãn giống nhau"""
    output_data = defaultdict(list)
    for ind, val in enumerate(dataset):
        output_data[val[-1]].append(ind)
    return output_data

def calculate_probability(label_index):
    """Trả về xác suất của mỗi nhóm trong dữ liệu với label"""
    probability = {}
    for label in label_index:
        probability[label] = len(label_index[label])
    sample_number = sum(probability.values())
    for label in probability:
        probability[label] /= sample_number
    return probability

def calculate_conditional_probability(dataset, label_index, laplace_smooth=0):
    """Trả về một dict có key là các nhãn, value là một vector có số chiều bằng số thuộc tính, 
    lưu xác suất có điều kiện với MLE của mỗi thuộc tính. theo mô hình multinomial naive bayes"""
    conditional_prob = {}
    for label in label_index:
       index = label_index[label]
       data_list = np.array([i[:-1] for i in np.asarray(dataset)[index]])
       data_list = data_list.sum(axis=0) + laplace_smooth
       total_number = data_list.sum()
       conditional_prob[label] = data_list / total_number
    return conditional_prob

def predict(test_vector, label_prob, feature_prob):
    """Trả về nhãn dự đoán với vector dữ liệu đầu vào"""
    for i in test_vector:
        # * Ở đây sẽ dùng logarit tự nhiên với tích p(X|c) * p(c) trở thành ln(p(X|c)) + ln(p(c))
        for label in label_prob:
            p_label = label_prob[label]
            p_features_c = np.log(feature_prob)

if __name__ == "__main__":

    # ! Chuẩn bị dữ liệu
    # * Đọc dữ liệu
    with open('vectorlist.bin', 'rb') as fb:
        word_vector = pickle.load(fb)

    # * chia dữ liệu 20000 dòng để train
    train_set = word_vector[:10]
    # print(train_set)

    # * lấy 6000 dòng còn lại để test
    test_set = word_vector[200:250]
    # print(test_set)

    # ! training
    # * tính xác suất của nhãn
    label_index = split_with_label(train_set)
    # print(label_index)
    label_proba = calculate_probability(label_index)
    # print(label_proba)

    # * tính xác suất có điều kiện của mỗi thuộc tính theo mô hình multinomial naive bayes
    calculate_conditional_probability(train_set, label_index, laplace_smooth=1)

    # ! test
    