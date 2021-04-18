// 初始化表格
function initTable(elem, data){
    layui.use('table', function(){
        var table = layui.table;

        // 构造一个表格
        table.render({
            elem: elem,
            height: 312,
            // url: '/demo/table/user/', //数据接口
            page: true, //开启分页
            cols: [[ //表头
                {field: 'id', title: 'ID', width:80, sort: true, fixed: 'left'},
                {field: 'affected_product', title: '可能影响的产品', width:180},
                {field: 'possibility', title: '可能性', width:80, sort: true},
            ]],
            data: data,
        });
    })
}

// 绘制表格
function openLayer(elem, data, event){
    // 使用layer
    layui.use('layer', function(){
        var layer = layui.layer;

        // 初始化layer弹出层
        layer.open({
            type: 1,
            title: "节点(" + event.name + ")相似性分析",
            content: elem,
            // area: ['500px', '300px'],
            offset: 'auto',
            maxmin: true,
        })
        // 显示隐藏的表格
        elem.css("display", "block");
      });  
} 