# coding=utf8

import struct
from Network import Network
import time

__author__ = 'DixonShen'


# 数据加载器基类
class Loader(object):
    def __init__(self, path, count):
        '''
        初始化加载器
        :param path: 数据文件路径
        :param count: 文件中的样本个数
        '''
        self.path = path
        self.count = count

    def get_file_content(self):
        '''
        读取文件内容
        :return:
        '''
        f = open(self.path, 'rb')
        content = f.read()
        return content

    def to_int(self, byte):
        '''
        将unsigned byte字符转换为整数
        :param byte:
        :return:
        '''
        return struct.unpack('B', byte)[0]


# 图像数据加载器
class ImageLoader(Loader):
    def get_picture(self, content, index):
        '''
        内部函数，从文件中获取图像
        :param content:
        :param index:
        :return:
        '''
        start = index * 28 * 28 + 16
        picture = []
        for i in range(28):
            picture.append([])
            for j in range(28):
                picture[i].append(
                    self.to_int(content[start + i * 28 + j])
                )
        return picture

    def get_one_sample(self, picture):
        '''
        内部函数，将图像转化为样本的输入向量
        :param picture:
        :return:
        '''
        sample = []
        for i in range(28):
            for j in range(28):
                sample.append(picture[i][j])
        return sample

    def load(self):
        '''
        加载数据文件，获得全部样本的输入向量
        :return:
        '''
        content = self.get_file_content()
        data_set = []
        for index in range(self.count):
            data_set.append(self.get_one_sample(
                self.get_picture(content, index)
            ))
        return data_set


# 标签数据加载器
class LabelLoader(Loader):
    def load(self):
        '''
        加载数据文件，获取全部样本的标签向量
        :return:
        '''
        content = self.get_file_content()
        labels = []
        for index in range(self.count):
            labels.append(self.norm(content[index + 8]))
        return labels

    def norm(self, label):
        '''
        内部函数，将一个值转换为10维标签向量
        :param label:
        :return:
        '''
        label_vec = []
        label_value = self.to_int(label)
        for i in range(10):
            if i == label_value:
                label_vec.append(0.95)
            else:
                label_vec.append(0.05)
        return label_vec


def get_training_data_set():
    '''
    获取训练数据集
    :return:
    '''
    image_loader = ImageLoader('train-images.idx3-ubyte', 60000)
    label_loader = LabelLoader('train-labels.idx1-ubyte', 60000)
    return image_loader.load(), label_loader.load()


def get_test_data_set():
    '''
    获得测试数据集
    :return:
    '''
    image_loader = ImageLoader('t10k-images.idx3-ubyte', 10000)
    label_loader = LabelLoader('t10k-labels.idx1-ubyte', 10000)
    return image_loader.load(), label_loader.load()


# 获取网络的识别结果
def get_result(vec):
    # vec是个10维向量
    max_value_index = 0
    max_value = 0
    for i in len(vec):
        if vec[i] > max_value:
            max_value_index = i
            max_value = vec[i]
    return max_value_index


# 使用错误率进行评估
def evaluate(network, test_data_set, test_labels):
    correct = 0
    total = len(test_data_set)

    for i in range(total):
        label = get_result(test_labels[i])
        predict = get_result(network.predict(test_data_set[i]))
        if label == predict:
            correct += 1
    return float(correct) / float(total)


# 训练。每训练10轮，评估一次准确率，当准确率下降时终止训练。
def train_and_evaluate():
    last_error_ratio = 1.0
    epoch = 0
    # start_time = time.time()
    train_data_set, train_labels = get_training_data_set()
    test_data_set, test_labels = get_test_data_set()
    # print 'Loading dataset takes: %s s' % (time.time()-start_time)
    network = Network([784, 300, 10])
    while True:
        epoch += 10
        network.train(train_labels, train_data_set, 0.1, 10)
        error_ratio = evaluate(network, test_data_set, test_labels)
        print 'after epoch %d, error ratio is %f' % (epoch, error_ratio)
        if error_ratio > last_error_ratio:
            break
        else:
            last_error_ratio = error_ratio

if __name__ == '__main__':
    start_time = time.time()
    train_and_evaluate()
    print 'The executing time is %s' % time.time() - start_time
    # image_loader = ImageLoader('t10k-images.idx3-ubyte', 10000)
    # print len(image_loader.load())
