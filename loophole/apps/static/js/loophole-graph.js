
    // 中文node label 映射 英文type
    var CATEGORY_TO_SOURCE_TYPE = {
        "产品": "product",
        "厂商": "manufacturer",
        "漏洞": "loophole",
        "威胁": "threat",
        "危险等级": "dangerous-level",
    }
    
    // 英文link relationship 映射 中文关系名
    var REALTIONSHIP_TO_LINK_NAME = {
        "loophole_2_dangerousLevel": "属于",
        "loophole_2_threat": "存在",
        "loophole_2_product": "影响",
        "manufacturer_2_loophole": "上报",
        "product_2_manufacturer": "所属",
    }

    function setGraphOptions(graph) {
        option = {
            title: {
                text: '漏洞展示图',
                subtext: 'Default layout',
                top: 'top',
                left: 'left'
            },
            tooltip: {
                position: function(point, params, dom, rect, size) {
                    return point;
                },
                formatter: function(params) {
                    var data = params.data;
                    var content = "";
                    if (params.dataType == 'node') {
                        for (i in data) {
                            content = content + i + ": " + data[i] + "</br>"
                        }
                    } else if (params.dataType == 'edge') {
                        content = params.data.source + " --" + REALTIONSHIP_TO_LINK_NAME[params.data.relationship] + "--> " + params.data.target
                    }
                    return content
                }
            },
            legend: [{
                itemHeight: 14,
                // selectedMode: 'single',
                data: graph.categories.map(function (a) {
                    return a.name;
                })
            }],
            series: [
                {
                    name: '漏洞展示图',
                    type: 'graph',
                    layout: 'force',
                    data: graph.nodes,
                    links: graph.links,
                    categories: graph.categories,
                    roam: true,
                    draggable: true,
                    cursor: 'pointer',
                    symbolSize: [20, 20],
                    edgeSymbol: ['none', 'arrow'], // 线的起点和终点样式。
                    edgeSymbolSize: [10, 7],
                    label: {
                        position: 'right'
                    },
                    force: {
                        repulsion: 100
                    },
                }
            ]
        };

        myChart.setOption(option);
    };

    // CNVD-2020-35433
    //Ajax请求
    $("#submit_btn").click(function(){
        var nodeId = $("#input_search").val();
        var sourceType = $("#sourceType").val();
        console.log(nodeId);
        $.get(
            "/api/v1/node/"+nodeId+"?sourceType="+sourceType, 
            function(response){
                var graph = new Object();
                graph.categories = response.data.categories;
                graph.nodes = response.data.nodes;
                graph.links = response.data.links;
                console.log(graph)
                setGraphOptions(graph);  
                console.log(myChart);
                console.log(myChart._model.option.series);
        })
    });


    // 获取旧图
    function getOldGraph(){
        var oldGraph = new Object();
        oldGraph.categories = myChart._model.option.series[0].categories;
        oldGraph.nodes = myChart._model.option.series[0].data;
        oldGraph.links = myChart._model.option.series[0].links;
        return oldGraph;
    }

    // 合并新图和旧图
    function combineGraph(oldGraph, newGraph) {
        var graph = new Object();
        graph.categories = $.merge(oldGraph.categories, newGraph.categories);
        graph.nodes = $.merge(oldGraph.nodes, newGraph.nodes);
        graph.links = $.merge(oldGraph.links, newGraph.links);
        return graph;
    }

    function dedupGraph(graph) {
        var dedupedGraph = new Object();
        dedupedGraph.categories = dedup(graph.categories);
        dedupedGraph.nodes = dedup(graph.nodes);
        dedupedGraph.links = dedup(graph.links);
        return dedupedGraph;
    }

    // 图的属性数组去重
    function dedup(array, key){
        var uniqueArray = [];
        var seen = {};
        for(var i = 0; i < array.length; i++){
            if (array[i].name) {
                if(!seen[array[i].name]){
                    uniqueArray.push(array[i]);
                    seen[array[i].name] = 1;
                }
            } else {
                if(!seen[array[i].source + array[i].target]){
                    uniqueArray.push(array[i]);
                    seen[array[i].source + array[i].target] = 1;
                }
                
            }
        }
        return uniqueArray;
       }

