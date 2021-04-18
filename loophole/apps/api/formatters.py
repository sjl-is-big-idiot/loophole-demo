# _*_ coding: utf-8 _*_
# @FileName : formatters.py
# @Author   : sjl
# @CreatedAt     :  2021/04/09 09:00:48
# @UpdatedAt     :  2021/04/09 09:00:48
# @description: formatters
# @Software : VSCode




class BaseNodeFormatter(object):
    def format(self, *args, **kwargs):
        raise NotImplementedError("This method must be implemented!")


class LoopholeNodeFormatter(BaseNodeFormatter):
    label = "loophole"
    CATEGORY = "漏洞"
    def format(self, node):
        return {
            "name": node.get("name"), 
            "category":self.CATEGORY,
            "cve_id": node.get("cveId"),
            "description": node.get("description"),
            "publish_time": node.get("publishTime"),
            "solution": node.get("solution"),
            "title": node.get("title"),
        }


class ManufacturerNodeFormatter(BaseNodeFormatter):
    label = "manufacturer"
    CATEGORY = "厂商"
    def format(self, node):
        return {"name": node.get("name"), "category":self.CATEGORY}


class ThreatNodeFormatter(BaseNodeFormatter):
    label = "threat"
    CATEGORY = "威胁"
    def format(self, node):
        return {"name": node.get("name"), "category":self.CATEGORY}


class DangerousLevelNodeFormatter(BaseNodeFormatter):
    label = "dangerousLevel"
    CATEGORY = "危险等级"
    def format(self, node):
        return {"name": node.get("name"), "category":self.CATEGORY}


class ProductNodeFormatter(BaseNodeFormatter):
    label = "product"
    CATEGORY = "产品"
    def format(self, node):
        return {"name": node.get("name"), "category":self.CATEGORY}


class BaseRelationshipFormatter(object):
    def format(self, *args, **kwargs):
        raise NotImplementedError("This method must be implemented!")


class L2PRelationshipFormatter(BaseRelationshipFormatter):
    label = ""
    RELATIONSHIP = "Loophole2Product"


class L2DRelationshipFormatter(BaseRelationshipFormatter):
    label = ""
    RELATIONSHIP = "Loophole2DangerousLevel"


class L2TRelationshipFormatter(BaseRelationshipFormatter):
    label = ""
    RELATIONSHIP = "Loophole2Threat"    


class M2LRelationshipFormatter(BaseRelationshipFormatter):
    label = ""
    RELATIONSHIP = "Manufacturer2Loophole"
    

class P2MRelationshipFormatter(BaseRelationshipFormatter):
    label = ""
    RELATIONSHIP = "Product2Manufacturer"
