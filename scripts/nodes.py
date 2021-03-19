# _*_ coding: utf-8 _*_
# @FileName : nodes.py
# @Author   : sjl
# @CreatedAt     :  2021/03/17 08:00:11
# @UpdatedAt     :  2021/03/17 08:00:11
# @description: nodes class use to generate csv file that need import to neo4j
# @Software : VSCode


from py2neo import Graph, Node, Relationship
from py2neo.bulk import create_nodes, merge_nodes
from exceptions import UnImplementedError
from tools import spend_time


# 显然，不可能一次性将大数据集的节点/关系插入图数据库 因此，建议将输入数据分批处理，然后在单独的事务中进行处理。
# example 
"""
>>> from py2neo.bulk import merge_nodes
>>> g = Graph()
>>> keys = ["name", "age"]
>>> data = [
    ["Alice", 33],
    ["Bob", 44],
    ["Carol", 55],
    ["Carol", 66],
    ["Alice", 77],
]
>>> merge_nodes(g.auto(), data, ("Person", "name"), keys=keys)
"""



class BaseNode(object):
    merge_key = tuple()
    fields = {}
    LIMIT = 300 # 300个节点执行一次事务，避免超过neo4j heap space 

    @spend_time
    def merge_nodes(self, g, data, merge_key=None, keys=None):
        """
        :param tx: Transaction in which to carry out this operation
        :param data: node data supplied as a list of lists (if keys are provided) or a list of dictionaries (if keys is None
        :param merge_key: tuple of (label, key1, key2…) on which to merge
        :param labels: additional labels to apply to the merged nodes
        :param keys: optional set of keys for the supplied data (if supplied as value lists)
        """
        merge_key = merge_key or self.merge_key
        keys = keys or list(self.fields.keys())
        if len(data) > self.LIMIT:
            for small_data in self.split_data(data):
                merge_nodes(g.auto(), small_data, merge_key, keys=keys)
        else:
            merge_nodes(g.auto(), data, merge_key, keys=keys)

    def split_data(self, data):
        """
        split big array to several small array if data bigger than self.LIMIT
        :param data: list.
        """
        splited_data = []
        for i in range(len(data)//self.LIMIT):
            small_data = data[i*self.LIMIT: (i+1)*self.LIMIT]
            splited_data.append(small_data)

        return splited_data

class DangerousLevelNode(BaseNode):
    """
    dangerousLevel node
    """
    merge_key = ("dangerousLevel", "name") # label, property1, property2...
    fields = {"name": "serverity"}  


class LoopholeNode(BaseNode):
    """
    loophole node
    """
    merge_key = ("loophole", "name") # label, property1, property2...
    fields = {"name": "number", "title": "title", "description": "description", "solution": "formalWay", "cveId": "cveStr", "publishTime": "openTime"}    


class ManufacturerNode(BaseNode):
    """
    manufacturer node
    """
    merge_key = ("manufacturer", "name") # label, property1, property2...
    fields = {"name": "manufacturer"}     


class ProductNode(BaseNode):
    """
    product node
    """
    merge_key = ("product", "name") # label, property1, property2...
    fields = {"name": "reflectProduct"}     


class ThreatNode(BaseNode):
    """
    threat node
    """
    merge_key = ("threat", "name") # label, property1, property2...
    fields = {"name": "thread"}     
