# coding=utf8

from numpy.lib import function_base

__author__ = 'DixonShen'


def sigmoid(x):
    return 1.0 / (1 + function_base.exp(-x))


# 节点类，负责记录和维护节点自身信息以及与这个节点相关的上下游连接，实现输出值和误差项的计算。
class Node(object):
    def __init__(self, layer_index, node_index):
        '''
        构造节点对象
        :param layer_index: 节点所属的层的编号
        :param node_index: 节点的编号
        '''
        self.layer_index = layer_index
        self.node_index = node_index
        self.downstream = []
        self.upstream = []
        self.output = 0
        self.delta = 0

    def set_output(self, output):
        '''
        设置节点的输出值。如果节点属于输入层会用用到这个函数
        :param output:
        :return:
        '''
        self.output = output

    def append_downstream_connection(self, conn):
        '''
        添加一个到下游节点的连接
        :param conn:
        :return:
        '''
        self.downstream.append(conn)

    def append_upstream_connection(self, conn):
        '''
        添加一个到上游节点的连接
        :param conn:
        :return:
        '''
        self.upstream.append(conn)

    def calc_output(self):
        '''
        计算节点的输出
        :return:
        '''
        output = reduce(lambda ret, conn: ret + conn.upstream_node.output * conn.weight,
                        self.upstream, 0)
        self.output = sigmoid(output)

    def calc_hidden_layer_delta(self):
        '''
        节点属于隐藏层时，计算delta
        :return:
        '''
        downstream_delta = reduce(lambda ret, conn: ret + conn.downstream_node.delta * conn.weight,
                                  self.downstream, 0.0)
        self.delta = self.output * (1 - self.output) * downstream_delta

    def calc_output_layer_delta(self, label):
        '''
        节点属于输出层时，计算delta
        :param label:
        :return:
        '''
        self.delta = self.output * (1 - self.output) * (label - self.output)

    def __str__(self):
        '''
        打印节点信息
        :return:
        '''
        node_str = '%u-%u: output: %f delta: %f' % (self.layer_index, self.node_index,
                                                    self.output, self.delta)
        downstream_str = reduce(lambda ret, conn: ret + '\n\t' + str(conn), self.downstream, '')
        upstream_str = reduce(lambda ret, conn: ret + '\n\t' + str(conn), self.upstream, '')
        return node_str + '\n\tdownstream: ' + downstream_str + '\n\tupstream: ' + upstream_str


# 实现一个输出恒为1的节点(计算偏置项时需要)
class ConstNode(object):
    def __init__(self, layer_index, node_index):
        '''
        构造节点对象
        :param layer_index: 节点所属的层的编号
        :param node_index: 节点的编号
        '''
        self.layer_index = layer_index
        self.node_index = node_index
        self.downstream = []
        self.output = 0
        self.delta = 0

    def append_downstream_connection(self, conn):
        '''
        添加一个到下游节点的连接
        :param conn:
        :return:
        '''
        self.downstream.append(conn)

    def calc_output(self):
        '''
        计算节点的输出
        :return:
        '''
        self.output = 1

    def calc_hidden_layer_delta(self):
        '''
        节点属于隐藏层时计算delta
        :return:
        '''
        downstream_delta = reduce(
            lambda ret, conn: ret + conn.downstream_node.delta * conn.weight,
            self.downstream, 0.0
        )
        self.delta = self.output * (1 - self.output) * downstream_delta

    def __str__(self):
        '''
        打印节点的信息
        :return:
        '''
        node_str = '%u-%u: output: 1' % (self.layer_index, self.node_index)
        downstream_str = reduce(lambda ret, conn: ret + '\n\t' + str(conn), self.downstream, '')
        return node_str + '\n\tdownstream:' + downstream_str

