# coding=utf8

from Node import Node
from Node import ConstNode

__author__ = 'DixonShen'


# 负责初始化一层。此外，作为Node的集合对象，提供对Node集合的操作。
class Layer(object):
    def __init__(self, layer_index, node_count):
        '''
        初始化一层
        :param layer_index:
        :param node_count: 层所包含的节点个数
        '''
        self.layer_index = layer_index
        self.nodes = []
        for i in range(node_count):
            self.nodes.append(Node(layer_index, i))
        self.nodes.append(ConstNode(layer_index, node_count))

    def set_output(self, data):
        '''
        设置层的输出，当层是输入层时用到
        :param data:
        :return:
        '''
        for i in range(len(data)):
            self.nodes[i].set_output(data[i])

    def calc_output(self):
        '''
        计算层的输出向量
        :return:
        '''
        for node in self.nodes:
            node.calc_output()

    def dump(self):
        '''
        打印层的信息
        :return:
        '''
        for node in self.nodes:
            print node
