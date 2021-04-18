// Timer函数
var TimeFn = null; 

// 整个echats画布中添加zrender事件，收起右边侧边栏
myChart.getZr().on('click', function (event) {
    // 没有 target 意味着鼠标/指针不在任何一个图形元素上，它是从“空白处”触发的。
    if (!event.target) {
        // 点击在了空白处，如果右边侧边栏展开了，则收起。
        $("#sideBar").removeClass("addWidth");
        // 清除之前的<li>元素
        $("#sideBar > ul > li").remove();
    }
});

// $('body').on('click',function (e) {
//     console.log(e.target)
//     if (($(e.target).attr('class') != 'sidebarClass') && ($(e.target).attr('class') != 'graph-layout')) {
//         console.log('除了 class 为 mochu 以外的所有元素都可以输出此段文字！');
//     }
// });

// 在echarts图中，双击鼠标的同时，也会触发单击事件，在此处理
function clickEvent(params){
    clearTimeout(TimeFn);
    TimeFn = setTimeout(function(){
        console.log("单击事件");
        var sideBar = $("#sideBar");
        var data = params.data;
        if (params.dataType == 'node') {
            //我的逻辑上是先判断没有这个class，没有的话就添加，这个添加动作会触发宽度加长的过渡效果
            if (!sideBar.hasClass("addWidth")) {
                $("#sideBar").addClass("addWidth");
                // 将节点属性显示到侧边栏
                for (i in params.data) {
                    $("#sideBar > ul").append("<li>" + i + ": " + params.data[i] + "</li>");
                }
            } else {
                // 清除之前的<li>元素
                $("#sideBar > ul > li").remove();
                // 将新的节点属性显示到侧边栏
                for (i in params.data) {
                    $("#sideBar > ul").append("<li>" + i + ": " + params.data[i] + "</li>");
                }
            }
        } else {
            $("#sideBar").removeClass("addWidth");
            // 清除之前的<li>元素
            $("#sideBar > ul > li").remove();
        }
    },300);
}

function dbClickEvent(params){
    clearTimeout(TimeFn);
    console.log("双击事件",params);
    var nodeId = null;
    var sourceType = null;
    if (params.componentSubType == 'graph' && params.dataType == 'node'){
        nodeId = params.data.name;
        sourceType = CATEGORY_TO_SOURCE_TYPE[params.data.category];

        $.get(
            "/api/v1/node/"+nodeId+"?sourceType="+sourceType, 
            function(response){
                console.log(response);
                // 获取已经绘制的图中的旧数据
                var oldGraph = getOldGraph();
                // 获取查询得到的新数据
                var newGraph = new Object();
                newGraph.categories = response.data.categories;
                newGraph.nodes = response.data.nodes;
                newGraph.links = response.data.links;

                // 合并新旧数据
                graph = combineGraph(oldGraph, newGraph)
                console.log(graph)

                graph = dedupGraph(graph);
                console.log(graph)
                setGraphOptions(graph);  
        })
    }
}


//左键单击节点弹出侧边栏
myChart.on("click", function (params) {
    clickEvent(params);
})

// ecahrts图中，添加鼠标双击事件，查询数据库
myChart.on('dblclick', function (params) {
    dbClickEvent(params);
});

// echarts图中，添加鼠标右键事件

//屏蔽浏览器默认的鼠标事件
//document.oncontextmenu = function () { return false; }; 
// 屏蔽Echarts区域的鼠标事件
// var parent = document.getElementById('main'); 
// parent.oncontextmenu = function () { return false}
// 绑定鼠标事件
myChart.on("contextmenu", function (e) {
    console.log("test message.");
    console.log(e)
    if (e.event.event.button == 2) {
        showMenu(e,[
            {
                "name": "相似性分析",
                "fn": function() {
                    if (e.dataType == 'node'){
                        // TODO， 请求后端获取数据
                        var testData = [
                            {"id": 0, "affected_product": "产品0", "possibility": "0%"},
                            {"id": 1, "affected_product": "产品1", "possibility": "10%"},
                            {"id": 2, "affected_product": "产品2", "possibility": "20%"},
                            {"id": 3, "affected_product": "产品3", "possibility": "30%"},
                            {"id": 4, "affected_product": "产品4", "possibility": "40%"},
                            {"id": 5, "affected_product": "产品5", "possibility": "50%"},
                            {"id": 6, "affected_product": "产品6", "possibility": "60%"},
                            {"id": 7, "affected_product": "产品7", "possibility": "70%"},
                            {"id": 8, "affected_product": "产品8", "possibility": "80%"},
                        ];
                        // 填充表格，并以弹窗方式展示
                        initTable($("#analysis-table"), testData);
                        openLayer($(".analysis-table"), testData, e);
                    }
                }
            }, {
                "name": "菜单2",
                "fn": function() {
                    alert("触发-菜单2" + e.data);
                    // TODO， 请求后端获取数据
                }
            },  {
                "name": "菜单3",
                "fn": function() {
                    alert("触发-菜单3" + e.data);
                    // TODO， 请求后端获取数据
                }
            
            }
        ]);
    }
});  

var style_ul = "padding:0px;margin:0px;border: 1px solid #ccc;background-color: #fff;position: absolute;left: 0px;top: 0px;z-index: 2;display: none;";
var style_li = "list-style:none;padding: 5px; cursor: pointer; padding: 5px 20px;margin:0px;";
var style_li_hover = style_li + "background-color: #00A0E9; color: #fff;";


//右键菜单容器
var menubox = $("<div class='echartboxMenu' style='" + style_ul + "'><div style='text-align:center;background:#ccc'></div><ul style='margin:0px;padding:0px;'></ul></div>")
    .appendTo($(document.body));
    
//移除浏览器右键菜单
myChart.getDom().oncontextmenu = menubox[0].oncontextmenu = function(){
    return false;   
}

// 点击其他位置隐藏鼠标右键菜单
$(document).click(function() {
    menubox.hide()
});

// 显示鼠标右键菜单
var showMenu = function(e,menus){
    $("div", menubox).text(e.name);
    var menulistbox = $("ul", menubox).empty();
    $(menus).each(function(i, item) {
        var li = $("<li style='" + style_li + "'>" + item.name + "</li>")
            .mouseenter(function() {
                $(this).attr("style", style_li_hover);
            })
            .mouseleave(function() {
                $(this).attr("style", style_li);
            })
            .click(function() {
                item["fn"].call(this);
                menubox.hide();
            });
        menulistbox.append(li);
    });
    menubox.css({
        "left": event.x,
        "top": event.y
    }).show();
}