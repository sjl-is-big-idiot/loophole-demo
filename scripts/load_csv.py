# _*_ coding: utf-8 _*_
# @FileName : load_csv.py
# @Author   : sjl
# @CreatedAt     :  2021/03/16 11:39:40
# @UpdatedAt     :  2021/03/16 11:39:40
# @description: import nodes and relationships with csv file from given import path
# @Software : VSCode



from exceptions import UnImplementedError


class BaseCsv(object):
    pass


class DangerousLevelNodeCsv(BaseCsv):
    """
    dangerouseLevel node
    """
    fields = {"dangerousLevelId": "serverity","LABEL": "dangerousLevel"}
    csv_filename = "dangerousLevels.csv"


class LoopholeNodeCsv(BaseCsv):
    """
    loophole node
    """
    fields = {
        "loopholeId": "number","title": "title", 
        "description": "description", "solution": "formalWay",
        "cveId": "cveStr", "publishTime": "openTime", "LABEL": "loophole"}
    csv_filename = "loopholes.csv"


class ManufacturerNodeCsv(BaseCsv):
    """
    manufacturer node
    """
    fields = {"manufacturerId": "manufacturer","LABEL": "manufacturer"}
    csv_filename = "manufacturers.csv"


class ProductNodeCsv(BaseCsv):
    """
    product node
    """
    fields = {"productId": "reflectProduct","LABEL": "product"}
    csv_filename = "products.csv"


class ThreatNodeCsv(BaseCsv):
    """
    threat node
    """
    fields = {"threatId": "thread","LABEL": "threat"}
    csv_filename = "threats.csv"



class L2DRelationshipCsv(BaseCsv):
    """loophole to dangerousLevel
    """
    fields = {"START_ID": "number", "END_ID": "serverity", "TYPE": "belongsTo"}
    csv_filename = "loophole-2-dangerousLevel.csv"


class L2PRelationshipCsv(BaseCsv):
    """
    loophole to product
    """
    fields = {"START_ID": "number", "END_ID": "reflectProduct", "TYPE": "affects"}
    csv_filename = "loophole-2-product.csv"


class L2TRelationshipCsv(BaseCsv):
    """
    loophole to threat
    """
    fields = {"START_ID": "number", "END_ID": "thread", "TYPE": "belongsTo"}
    csv_filename = "loophole-2-threat.csv"


class P2MRelationshipCsv(BaseCsv):
    """
    product to manufacturer
    """
    fields = {"START_ID": "reflectProduct", "END_ID": "manufacturer", "TYPE": "belongsTo"}
    csv_filename = "product-2-manufacturer.csv"


class M2LRelationshipCsv(BaseCsv):
    """
    manufacturer to loophole
    """
    fields = {"START_ID": "manufacturer", "END_ID": "number", "TYPE": "reports"}
    csv_filename = "manufacturer-2-loophole.csv"


class LoadNodeCsvInterface(object):
    import_cql = ""


class LoadDangerousLevelCsv(LoadNodeCsvInterface):
    import_cql = ":auto USER PERIODIC COMMIT 100 LOAD CSV WITH HEADERS FROM file:///dangerousLevels.csv AS line " \
        "MERGE (a:dangerousLevel{name:line.dangerousLevelId, type:line.LABEL})"
    

class LoadLoopholeCsv(LoadNodeCsvInterface):
    import_cql = ":auto USER PERIODIC COMMIT 100 LOAD CSV WITH HEADERS FROM file:///loopholes.csv AS line " \
        "MERGE (a:loophole{name:line.loopholeId, title:line.title, description:line.description, " \
        "cveId:line.cveId, solution:line.solution, publishTime:line.publishTime, type:line.LABEL})"    
    pass


class LoadManufacturerCsv(LoadNodeCsvInterface):
    import_cql = ":auto USER PERIODIC COMMIT 100 LOAD CSV WITH HEADERS FROM file:///manufacturers.csv AS line " \
        "MERGE (a:manufacturer{name:line.manufacturerId, type:line.LABEL})" 
    pass


class LoadProductCsv(LoadNodeCsvInterface):
    import_cql = ":auto USER PERIODIC COMMIT 100 LOAD CSV WITH HEADERS FROM file:///products.csv AS line " \
        "MERGE (a:product{name:line.productId, type:line.LABEL})"
    pass


class LoadThreatCsv(LoadNodeCsvInterface):
    import_cql = ":auto USER PERIODIC COMMIT 100 LOAD CSV WITH HEADERS FROM file:///threats.csv AS line " \
        "MERGE (a:threat{name:line.threatId, type:line.LABEL})"
    pass


class LoadRelationshipCsvInterface(object):
    pass


class LoadL2DRelationship(LoadRelationshipCsvInterface):
    pass


class LoadL2MRelationship(LoadRelationshipCsvInterface):
    pass


class LoadL2PRelationship(LoadRelationshipCsvInterface):
    pass


class LoadL2TRelationship(LoadRelationshipCsvInterface):
    pass


class LoadM2LRelationship(LoadRelationshipCsvInterface):
    pass


class LoadP2MRelationship(LoadRelationshipCsvInterface):
    pass

