# _*_ coding: utf-8 _*_
# @FileName : relationships.py
# @Author   : sjl
# @CreatedAt     :  2021/03/17 08:30:53
# @UpdatedAt     :  2021/03/17 08:30:53
# @description: relationships class use to generate csv file that need import to neo4j
# @Software : VSCode


from exceptions import UnImplementedError
from py2neo import Graph, Node, Relationship
from py2neo.bulk import create_relationships, merge_relationships
from nodes import DangerousLevelNode, LoopholeNode, ProductNode, ManufacturerNode, ThreatNode
from tools import spend_time


class BaseRelationship(object):
    merge_key = tuple()
    start_node_key = tuple()
    end_node_key = tuple()
    fields = {}
    keys = [] # 关系的属性
    LIMIT = 100 # 10个关系执行一次事务，避免超过neo4j heap space

    @spend_time
    def merge_relationships(self, g, data, merge_key=None, start_node_key=None, end_node_key=None, keys=None):
        """
        :param tx: Transaction in which to carry out this operation
        :param data: node data supplied as a list of lists (if keys are provided) or a list of dictionaries (if keys is None. [(start_node, detail, end_node)]
        :param merge_key: tuple of (label, key1, key2…) on which to merge
        :param start_node_key: optional tuple of (label, key1, key2…) on which to match relationship start nodes, matching by node ID if not provided
        :param end_node_key: optional tuple of (label, key1, key2…) on which to match relationship end nodes, matching by node ID if not provided
        :param labels: additional labels to apply to the merged nodes
        :param keys: optional set of keys for the supplied data (if supplied as value lists)
        """
        merge_key = merge_key or self.merge_key
        start_node_key = start_node_key or self.start_node_key 
        end_node_key = end_node_key or self.end_node_key
        keys = keys or self.keys

        if len(data) > self.LIMIT:
            for small_data in self.split_data(data):
                merge_relationships(g.auto(), small_data, merge_key,start_node_key=start_node_key,end_node_key=end_node_key, keys=keys)
        else:
            merge_relationships(g.auto(), data, merge_key,start_node_key=start_node_key,end_node_key=end_node_key, keys=keys)


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

    def __str__(self):
        return "<class '{}', at {}>".format("BaseRelationship", id(self)) 


class L2DRelationship(BaseRelationship):
    """loophole to dangerousLevel
    """
    merge_key = ("belongsTo", "name") # label, property1, property2...
    start_node_key = LoopholeNode.merge_key # label, property1, property2...
    end_node_key = DangerousLevelNode.merge_key # label, property1, property2...
    fields = {"from": "number", "name": "loophole_2_dangerousLevel", "to": "serverity"}
    keys = ["name"]

    def __str__(self):
        return "<class '{}', at {}>".format("L2DRelationship", id(self)) 


class L2PRelationship(BaseRelationship):
    """
    loophole to product
    """
    merge_key = ("affects", "name") # label, property1, property2...
    start_node_key = LoopholeNode.merge_key
    end_node_key = ProductNode.merge_key
    fields = {"from": "number", "name": "loophole_2_product", "to": "reflectProduct"}
    keys = ["name"]

    def __str__(self):
        return "<class '{}', at {}>".format("L2PRelationship", id(self)) 


class L2TRelationship(BaseRelationship):
    """
    loophole to threat
    """
    merge_key = ("has", "name") # label, property1, property2...
    start_node_key = LoopholeNode.merge_key
    end_node_key = ThreatNode.merge_key
    fields = {"from": "number", "name": "loophole_2_threat", "to": "thread"}
    keys = ["name"]

    def __str__(self):
        return "<class '{}', at {}>".format("L2TRelationship", id(self)) 


class P2MRelationship(BaseRelationship):
    """
    product to manufacturer
    """
    merge_key = ("ownBy", "name") # label, property1, property2...
    start_node_key = ProductNode.merge_key
    end_node_key = ManufacturerNode.merge_key
    fields = {"from": "reflectProduct", "name": "product_2_manufacturer", "to": "manufacturer"}
    keys = ["name"]

    def __str__(self):
        return "<class '{}', at {}>".format("P2MRelationship", id(self)) 


class M2LRelationship(BaseRelationship):
    """
    manufacturer to loophole
    """
    merge_key = ("reports", "name") # label, property1, property2...
    start_node_key = ManufacturerNode.merge_key
    end_node_key = LoopholeNode.merge_key
    fields = {"from": "manufacturer", "name": "manufacturer_2_loophole", "to": "number"}
    keys = ["name"]

    def __str__(self):
        return "<class '{}', at {}>".format("M2LRelationship", id(self)) 
