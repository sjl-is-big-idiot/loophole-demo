# _*_ coding: utf-8 _*_
# @FileName : main.py
# @Author   : sjl
# @CreatedAt     :  2021/03/16 11:36:51
# @UpdatedAt     :  2021/03/16 11:36:51
# @description: import csv data into neo4j
# @Software : VSCode


import sys

from py2neo import Graph
from generate_graph import GeneratingGraphByCsv, GeneratingGraphByPy2neo
from nodes import  DangerousLevelNode, LoopholeNode, ManufacturerNode, ProductNode, ThreatNode
from relationships import L2DRelationship, L2PRelationship, L2TRelationship, M2LRelationship, P2MRelationship
from logger import SimpleLogger
import csv


sp_logger = SimpleLogger(__name__, "./log/loophole.log").get_logger()


def import_with_load_csv():
    """
    生成标准的csv文件，通过load csv 命令导入数据
    """
    csv_read_path = r"C:\Users\Administrator\Desktop\sunjinlong\lou-dong\data\raw-data\csv"
    csv_write_path = r"C:\Users\Administrator\Desktop\sunjinlong\lou-dong\data\import"
    ggc = GeneratingGraphByCsv()
    ggc.handle(csv_read_path, csv_write_path)    

def import_with_py2neo_bulk():
    """
    通过使用py2neo的批量导入功能
    """
    # URI = ""

    csv_read_path = r"C:\Users\Administrator\Desktop\sunjinlong\lou-dong\data\raw-data\csv"
    g = Graph(password="neo4j123456")
    ggp = GeneratingGraphByPy2neo()
    result = ggp.handle(csv_read_path)
    for res in result:
        nodes, relationships = res
        
        for node_class in ggp.node_classes:
            data = nodes.get(node_class, [])
            with open('nodes.csv', 'a', newline="") as f:
                writer = csv.writer(f)
                writer.writerows(data)
            sp_logger.info("merging {} nodes...... count={}".format(str(node_class), len(data)))
            node_class().merge_nodes(g, data)
    
        for rel_class in ggp.relationship_classes:
            # if rel_class in [L2PRelationship, P2MRelationship]:
            data = relationships.get(rel_class, [])
            with open('rels.csv', 'a', newline="") as f:
                writer = csv.writer(f)
                writer.writerows(data)
            sp_logger.info("merging {} relationships...... count={}".format(str(rel_class), len(data)))
            rel_class().merge_relationships(g, data)


def run():
    """
    entry function
    """
    # import_with_load_csv()
    import_with_py2neo_bulk()

if __name__ == "__main__":
    run()


