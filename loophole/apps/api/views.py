# _*_ coding: utf-8 _*_
# @FileName : views.py
# @Author   : sjl
# @CreatedAt     :  2021/03/24 11:26:50
# @UpdatedAt     :  2021/03/24 11:26:50
# @description: api blueprint
# @Software : VSCode

from . import api
from flask import current_app, g, request, url_for, jsonify, redirect, render_template
from apps.utils import login_required, dedup
from apps.db import get_db
from .models import (
    DangerousLevelNode, ProductNode, ManufacturerNode, LoopholeNode, ThreatNode,
    L2DRelationship, L2PRelationship, L2TRelationship, M2LRelationship, P2MRelationship,
)

from .handlers import NodeHandler



categories = {
    "manufacturer": "厂商",
    "loophole": "漏洞",
    "threat": "威胁",
    "product": "产品",
    "dangerousLevel": "危险等级",
}

categories = [
    {"number": 0, "name": "漏洞"},
    {"number": 1, "name": "厂商"},
    {"number": 2, "name": "产品"},
    {"number": 3, "name": "威胁"},
    {"number": 4, "name": "危险等级"},
]

TYPE_TO_LABEL = {
    "product": "product",
    "loophole": "loophole",
    "manufacturer": "manufacturer",
    "dangerous-level": "dangerousLevel",
    "threat": "threat",
}   

MESSAGES = {
    "source_type_error": "invalid source type",
    "no_data": "no data for database",
    "success": "success",
}


@api.route('/', methods=['GET', 'POST'])
def index():
    return render_template("index.html")


@api.route('/node/<string:node_id>', methods=['GET'])
# @api.route('/search', methods=['GET'])
# @login_required
def get_graph(node_id):
    """According to the node name to serach detail infomation in neo4j
    """
    graph = {"nodes": [], "links": [], "categories": categories}
    source_type = request.args.get("sourceType")
    if not TYPE_TO_LABEL.get(source_type):
        return jsonify({'data': graph, 'message': MESSAGES.get("source_type_error")})
    # node_id = "CNVD-2020-35433"
    graph_db = get_db()
    cql = "MATCH p=(n:%s{name:'%s'})-[]-() RETURN p LIMIT 100" % (TYPE_TO_LABEL.get(source_type), node_id)
    
    try:
        result = graph_db.run(cql)
        paths = result.data()
        if not paths:
            return jsonify({'data': graph, "message": MESSAGES.get("no_data")})

        nodes, links = consturct_graph(paths)
        graph["nodes"] = list(dedup(nodes, lambda x: x["name"]))
        graph["links"] = list(dedup(links, lambda x: (x["source"], x["target"])))
        print(nodes)
    except Exception as e:
        current_app.logger.error(str(e))
    
    return jsonify({'data':graph, "message": MESSAGES.get("success")})
 

def consturct_graph(paths):
    """
    According to the result of executing cypher to constuct graph content
    """
    nodes = []
    links = []
    for path in paths:
        p = path.get('p') # pywneo.data.path object
        rels = p.relationships
        for rel in rels:
            try:
                node_handler = NodeHandler()
                start_node = rel.start_node
                end_node = rel.end_node
                start_node_label = str(start_node.labels).replace(":", "")
                end_node_label = str(end_node.labels).replace(":", "")
                # according node's label to choose correct formatter
                start_formatter = node_handler.set_formatter(start_node_label)
                end_formatter = node_handler.set_formatter(end_node_label)
                nodes.append(start_formatter().format(start_node))
                nodes.append(end_formatter().format(end_node))
                # construct relationships
                link = {
                    "source": start_node.get("name"),
                    "target": end_node.get("name"),
                    "relationship": rel.get("name")
                }
                links.append(link)
            except Exception as e:
                current_app.logger.error(e)
    return nodes, links


@api.route("/get-similarity/<string:node_id>", methods=["GET"])
def get_similarity_of_node(node_id):
    """
    According the node id and category to seach similar product/loophole
    """
    # TODO
    similarity_result = {}
    # node_id = request.args.get("node_id")
    source_type = request.args.get("sourceType")
    if not TYPE_TO_LABEL.get(source_type):
        return jsonify({'data': similarity_result, 'message': MESSAGES.get("source_type_error")})
    try:
        pass
    except Exception as e:
        current_app.logger.error(e)

    return jsonify({'data':similarity_result, "message": MESSAGES.get("success")})