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


class BaseRelationship(object):
    merge_key = tuple()
    start_node_key = tuple()
    end_node_key = tuple()
    fields = []

    def __init__(self):
        raise UnImplementedError("Interface class could't instantiate!")

    def merge_relationships(self, tx, data, merge_key, start_node_key, end_node_key, keys=None):
        """
        :param tx: Transaction in which to carry out this operation
        :param data: node data supplied as a list of lists (if keys are provided) or a list of dictionaries (if keys is None
        :param merge_key: tuple of (label, key1, key2…) on which to merge
        :param start_node_key: optional tuple of (label, key1, key2…) on which to match relationship start nodes, matching by node ID if not provided
        :param end_node_key: optional tuple of (label, key1, key2…) on which to match relationship end nodes, matching by node ID if not provided
        :param labels: additional labels to apply to the merged nodes
        :param keys: optional set of keys for the supplied data (if supplied as value lists)
        """
        merge_key = merge_key or self.merge_key
        start_node_key = start_node_key or self.start_node_key 
        end_node_key = end_node_key or self.end_node_key
        keys = keys or self.fields
        merge_relationships(tx, data, merge_key, keys=keys)


class L2DRelationship(BaseRelationship):
    """loophole to dangerousLevel
    """
    merge_key = ("belongsTo", "name")
    start_node_key = LoopholeNode.merge_key
    end_node_key = DangerousLevelNode.merge_key
    fields = ["name"]


class L2PRelationship(BaseRelationship):
    """
    loophole to product
    """
    merge_key = ("affects", "name")
    start_node_key = LoopholeNode.merge_key
    end_node_key = DangerousLevelNode.merge_key
    fields = ["name"]



class L2TRelationship(BaseRelationship):
    """
    loophole to threat
    """
    merge_key = ("belongsTo", "name")
    start_node_key = LoopholeNode.merge_key
    end_node_key = DangerousLevelNode.merge_key
    fields = ["name"]


class P2MRelationship(BaseRelationship):
    """
    product to manufacturer
    """
    merge_key = ("belongsTo", "name")
    start_node_key = LoopholeNode.merge_key
    end_node_key = DangerousLevelNode.merge_key
    fields = ["name"]


class M2LRelationship(BaseRelationship):
    """
    manufacturer to loophole
    """
    merge_key = ("reports", "name")
    start_node_key = LoopholeNode.merge_key
    end_node_key = DangerousLevelNode.merge_key
    fields = ["name"]
