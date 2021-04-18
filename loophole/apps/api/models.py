# _*_ coding: utf-8 _*_
# @FileName : models.py
# @Author   : sjl
# @CreatedAt     :  2021/04/08 08:29:57
# @UpdatedAt     :  2021/04/08 08:29:57
# @description: neo4j model
# @Software : VSCode


class BaseNode(object):
    pass


class LoopholeNode(BaseNode):
    label = "loophole"


class ManufacturerNode(BaseNode):
    label = "manufacturer"


class ThreatNode(BaseNode):
    label = "threat"


class DangerousLevelNode(BaseNode):
    label = "dangerousLevel"


class ProductNode(BaseNode):
    label = "product"


class BaseRelationship(object):
    pass


class L2PRelationship(BaseRelationship):
    label = ""


class L2DRelationship(BaseRelationship):
    label = ""


class L2TRelationship(BaseRelationship):
    label = ""
    

class M2LRelationship(BaseRelationship):
    label = ""


class P2MRelationship(BaseRelationship):
    label = ""

