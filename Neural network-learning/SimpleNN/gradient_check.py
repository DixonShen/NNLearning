# coding=utf8

__author__ = 'DixonShen'


def gradient_check(network, sample_feature, sample_label):
    '''
    梯度检查
    :param network: 神经网络对象
    :param sample_feature: 样本的特征
    :param sample_label: 样本的标签
    :return:
    '''
    # 计算网络误差
    network_error = lambda vec1, vec2: \
        0.5 * reduce(lambda a, b: a + b,
                     map(lambda v: (v[0] - v[1]) * (v[0] - v[1]),
                         zip(vec1, vec2)))

    # 获取网络在当前样本下每个连接的梯度
    network.get_gradient(sample_feature, sample_label)

    # 对每个权重做梯度检查
    for conn in network.connections.connections:
        # 获取指定连接的梯度
        actual_gradient = conn.get_gradient()

        # 增加一个很小的值， 计算网络的误差
        epsilon = 0.0001
        conn.weight += epsilon
        error1 = network_error(network.predict(sample_feature), sample_label)

        # 减去一个很小的值，计算网络的误差
        conn.weight -= 2*epsilon  # 刚才加过一次，因此这里需要减去2倍
        error2 = network_error(network.predict(sample_feature), sample_label)

        # 计算期望的梯度值
        expected_gradient = (error1 - error2) / (2 * epsilon)

        print 'expected gradient: \t%f\nactual gradient: \t%f' % (
            expected_gradient, actual_gradient
        )
