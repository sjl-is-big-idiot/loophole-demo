# _*_ coding: utf-8 _*_
# @FileName : handlers.py
# @Author   : sjl
# @CreatedAt     :  2021/04/09 09:00:41
# @UpdatedAt     :  2021/04/09 09:00:41
# @description: handlers
# @Software : VSCode

from .formatters import LoopholeNodeFormatter, ManufacturerNodeFormatter, DangerousLevelNodeFormatter, ProductNodeFormatter, ThreatNodeFormatter


class NodeHandler(object):
    LABEL_TO_FORMATTER = {
        "product": ProductNodeFormatter, 
        "loophole": LoopholeNodeFormatter,
        "manufacturer": ManufacturerNodeFormatter,
        "dangerousLevel": DangerousLevelNodeFormatter,
        "threat": ThreatNodeFormatter,
    }

    def set_formatter(self, node_label):
        """
        According to node's lable to choose correct formatter to format node
        """
        print(node_label)
        return self.LABEL_TO_FORMATTER.get(node_label)

