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

    def __init__(self):
        raise UnImplementedError("Interface class could't instantiate!")

    def merge_nodes(self, tx, data, merge_key, keys=None):
        """
        :param tx: Transaction in which to carry out this operation
        :param data: node data supplied as a list of lists (if keys are provided) or a list of dictionaries (if keys is None
        :param merge_key: tuple of (label, key1, key2…) on which to merge
        :param labels: additional labels to apply to the merged nodes
        :param keys: optional set of keys for the supplied data (if supplied as value lists)
        """
        merge_key = merge_key or self.merge_key
        keys = keys or self.fields.keys()
        merge_nodes(tx, data, merge_key, keys=keys)


class DangerousLevelNode(BaseNode):
    """
    dangerouseLevel node
    """
    merge_key = ("dangerouseLevel", "name")
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
    merge_key = ("manufacturer", "name")
    fields = {"name": "manufacturer"}     


class ProductNode(BaseNode):
    """
    product node
    """
    merge_key = ("product", "name")
    fields = {"name": "reflectProduct"}     


class ThreatNode(BaseNode):
    """
    threat node
    """
    merge_key = ("threat", "name")
    fields = {"name": "thread"}     
