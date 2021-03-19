# _*_ coding: utf-8 _*_
# @FileName : generate_graph.py
# @Author   : sjl
# @CreatedAt     :  2021/03/16 11:05:49
# @UpdatedAt     :  2021/03/16 11:05:49
# @description: 生成xx节点.csv和xx关系.csv，用于将数据导入neo4j
# @Software : VSCode


import csv
import os
from logger import SimpleLogger
from concurrent.futures import ProcessPoolExecutor

from load_csv import (
    DangerousLevelNodeCsv, LoopholeNodeCsv, ManufacturerNodeCsv, ProductNodeCsv, ThreatNodeCsv,
    L2DRelationshipCsv, L2PRelationshipCsv, L2TRelationshipCsv, P2MRelationshipCsv, M2LRelationshipCsv
)
from nodes import DangerousLevelNode, LoopholeNode, ManufacturerNode, ProductNode, ThreatNode
from relationships import L2DRelationship, L2PRelationship, L2TRelationship, P2MRelationship, M2LRelationship

from exceptions import LackAttributeError, UnImplementedError, InstantiateError


sp_logger = SimpleLogger(__name__, './log/generate_graph.log').get_logger()



class GeneratingGraphInterface(object):
    def __init__(self):
        raise UnImplementedError("Interface class could't instantiate!")

    def handle(self):
        raise UnImplementedError("This methods must be implemented!")


class BaseGeneratingGraph(GeneratingGraphInterface):
    node_classes = []
    relationship_classes = []

    def __init__(self):
        raise InstantiateError("The class {} could't instantiat!")

    def handle(self, csv_path, workers=1):
        """
        """
        csv_path = csv_path
        csv_files = (os.path.join(csv_path, cfile) for cfile in os.listdir(csv_path)  if os.path.isfile(os.path.join(csv_path, cfile)))
        with ProcessPoolExecutor(max_workers=workers) as executor:
            result = executor.map(self.generate, csv_files)
        return result

    def generate(self, csv_file):
        """
        """
        self.parse(csv_file)
        
    def parse(self, csv_file):
        """
        parse data from raw csv file
        """
        nodes = {}
        relationships = {}
        sp_logger.info("Prepare to generates nodes and relationships csv file for imports data to neo4j.")

        # base class is `object` that already implements `__hash__` methods.
        for node_class in self.node_classes:
            nodes.setdefault(node_class, set()) 

        for rel_class in self.relationship_classes:
            relationships.setdefault(rel_class, set())

        # parse csv file's content, and generate given nodes and relastionships' data
        try:
            with open(csv_file, 'r', newline="", encoding="utf-8-sig") as f:
                reader = csv.DictReader(f)
                sp_logger.info("Starting read {}.".format(csv_file))
                for row in reader:
                    for node_class in self.node_classes:
                        valid, node_line = self.formating_nodes(row, node_class)
                        if valid:
                            nodes[node_class].add(node_line)

                    for rel_class in self.relationship_classes:
                        valid, rel_line = self.formating_rels(row, rel_class)
                        if valid:
                            relationships[rel_class].add(rel_line)
            sp_logger.info("Completed read {}.".format(csv_file))
        except Exception as e:
            sp_logger.error(str(e))
        
        return nodes, relationships


    def check_Id(self, line, row):
        """check primary field whether is `None`or not.
        """
        if len(line) == 0:
            sp_logger.warn("There is a blank line, don't write to csv file that need import to neo4j. Row is {}".format(row))
            return False
        if not line[0]:
            sp_logger.warn("There is lack primary key, don't write to csv file that need import to neo4j. Row is {}".format(row))
            return False
        return True

    def formating_nodes(self, row, node_class):
        """
        construct node csv file's content for per line
        """
        line = []
        try:
            for header, raw_field in getattr(node_class, "fields", {}).items():
                print(header, raw_field)
                content = raw_field if header == 'LABEL' else row.get(raw_field)
                content = content.replace(" ", "")
                content = "未知" if content == "" else content

                line.append(content)
            valid = self.check_Id(line, row)
            print(line, row)
        except Exception as e:
            sp_logger.error(str(e))
        return valid, tuple(line)

    def formating_rels(self, row, rel_class):
        """
        construct relationship csv file's content for per line
        """
        line = []
        try:
            for header, raw_field in getattr(rel_class, "field", {}).items():
                content = raw_field if header == 'TYPE' else row.get(raw_field, "未知")
                line.append(content)

            valid = self.check_Id(line, row)
        except Exception as e:
            sp_logger.error(str(e))
        return valid, tuple(line)


class GeneratingGraphByPy2neo(BaseGeneratingGraph):
    node_classes = [DangerousLevelNode, LoopholeNode, ManufacturerNode, ProductNode, ThreatNode]
    relationship_classes = [L2DRelationship, L2PRelationship, L2TRelationship, P2MRelationship, M2LRelationship]

    def __init__(self):
        pass

    
class GeneratingGraphByCsv(BaseGeneratingGraph):
    node_classes = [DangerousLevelNodeCsv, LoopholeNodeCsv, ManufacturerNodeCsv, ProductNodeCsv, ThreatNodeCsv]
    relationship_classes = [L2DRelationshipCsv, L2PRelationshipCsv, L2TRelationshipCsv, P2MRelationshipCsv, M2LRelationshipCsv]

    def __init__(self):
        pass

    def handle(self, csv_path, write_path, workers=1):
        """
        """
        result = super().handle(csv_path, workers=workers)
        nodes, relationships = result
        self.write_nodes_and_relationships(nodes, relationships, write_path)


    def write_csv(self, dirpath, data):
        """
        write data to destination csv file
        """
        try:
            for node_or_rel_class,value in data.items():
                if not (hasattr(node_or_rel_class, 'csv_filename') and hasattr(node_or_rel_class, 'fields')):
                    raise LackAttributeError("{} doesn't has csv_filename or fields attribute!".format(type(node_or_rel_class)))

                csv_filename = getattr(node_or_rel_class, "csv_filename")
                csv_header = getattr(node_or_rel_class, "fields")
                csv_filepath = os.path.join(dirpath, csv_filename)
                # don't repeat write csv header!
                if os.path.exists(csv_filepath):
                    # with open(csv_filepath, 'a', newline="", encoding="utf-8") as f:
                    with open(csv_filepath, 'a', newline="", encoding="utf-8") as f:
                        writer = csv.writer(f)
                        writer.writerows(list(value))
                else:
                    with open(csv_filepath, 'a', newline="", encoding="utf-8") as f:
                        writer = csv.writer(f)
                        writer.writerow(csv_header)
                        writer.writerows(list(value))
        except Exception as e:
            sp_logger.error(str(e))

    def write_nodes_and_relationships(self, nodes, relationships, write_path):
        try:
            destination_dir = os.path.join(write_path)
            
            # ensure nodes/ and relationships/ dir already exists.
            if not (os.path.exists(destination_dir) and os.path.isdir(destination_dir)):
                os.mkdir(destination_dir)

            sp_logger.info("Starting write nodes and relationships to {}, respectively."\
                .format(destination_dir))
            self.write_csv(destination_dir, nodes)
            self.write_csv(destination_dir, relationships)
            sp_logger.info("Completed write nodes and relationships to {} respectively."\
                .format(destination_dir))
        except Exception as e:
            sp_logger.error(str(e))

