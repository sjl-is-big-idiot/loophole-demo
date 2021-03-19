# _*_ coding: utf-8 _*_
# @FileName : main.py
# @Author   : sjl
# @CreatedAt     :  2021/03/16 11:36:51
# @UpdatedAt     :  2021/03/16 11:36:51
# @description: loopholes project's entry
# @Software : VSCode


import sys

from py2neo import Graph
from generate_graph import GeneratingGraphByCsv, GeneratingGraphByPy2neo
from nodes import  DangerousLevelNode, LoopholeNode, ManufacturerNode, ProductNode, ThreatNode
from relationships import L2DRelationship, L2PRelationship, L2TRelationship, M2LRelationship, P2MRelationship


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
    node_classes = [DangerousLevelNode, LoopholeNode, ManufacturerNode, ProductNode, ThreatNode]
    relationship_classes = [L2DRelationship, L2PRelationship, L2TRelationship, M2LRelationship, P2MRelationship]

    csv_read_path = r"C:\Users\Administrator\Desktop\sunjinlong\lou-dong\data\raw-data\csv"
    # nodes, relationships = GeneratingGraphByPy2neo().handle(csv_read_path)
    result = GeneratingGraphByPy2neo().handle(csv_read_path)
    # print(result)
    g = Graph(password="neo4j123456")

    # for node_class in node_classes:
    #     node_class().merge_nodes(
    #         g.auto(), 
    #         nodes, 
    #         node_class.merge_key, 
    #         )
    
    # for rel_class in relationship_classes:
    #     rel_class().merge_relationships(
    #         g.auto(), 
    #         relationships, 
    #         rel_class.merge_key, 
    #         rel_class.start_node_key, 
    #         rel_class.end_node_key, 
    #         )




def run():
    """
    entry function
    """
    # import_with_load_csv()
    import_with_py2neo_bulk()

if __name__ == "__main__":
    run()


