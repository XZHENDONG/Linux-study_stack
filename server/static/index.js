

page=0
function requestTable(){

    ajax=$.ajax({
        url:'/api/v1/practices',
        data:{"table_rows":page},
        contentType: 'application/json; charset=UTF-8',
        type:'GET',
        dataType:'json',
        statusCode: {
            404: function() {
              alert( "已加载全部题目" );
              document.getElementById("load_exerc").innerHTML = "已加载全部题目";
            }
          }
    }).done(function(){
            responseText=ajax.responseJSON
            page=responseText.next_page
            createTable(responseText.exerc)
    });

}

function createTable(title_list){
    var table = document.getElementById('practice_tb');
    table.width = "100%";
    table.border = 1;
    var tr,td;
    for(var i in title_list){
        //循环插入元素
        tr = table.insertRow(table.rows.length);
        for(var j=0;j<3;j++){
            td = tr.insertCell(tr.cells.length);
            if (j==0){
                td.innerHTML = table.rows.length;
                td.width=50;
                td.align = "center";
            }
            if (j==1){
                div = document.createElement("div");
                div.setAttribute("style", "width:100%;word-wrap:break-word;")
                div.innerHTML = title_list[i].exerc_markdown.trim().split('\n')[0].replace(/^#+/,'');
                td.appendChild(div);
                td.align = "center";
            }
            if (j==2){
                edit_button= document.createElement("input");
                edit_button.setAttribute("type", "button")
                edit_button.setAttribute("title_id",title_list[i].exerc_id)
                edit_button.setAttribute("class", "btn btn-primary form-control")
                edit_button.setAttribute("style", "margin-right:2px;")
                edit_button.setAttribute("value", "编辑")
                edit_button.setAttribute("onclick", "javascrtpt:window.open('/editor/?exerc_id="+title_list[i].exerc_id+"')")
                edit_button.innerHTML = "编辑";
                status_button= document.createElement("input");
                status_button.setAttribute("type", "button")
                status_button.setAttribute("class", "btn btn-primary form-control")
                status_button.setAttribute("value", "查看学生数据")
                status_button.setAttribute("title_id",title_list[i].exerc_id)
                delete_button= document.createElement("input");
                delete_button.setAttribute("type", "button")
                delete_button.setAttribute("class", "btn btn-primary form-control")
                delete_button.setAttribute("style", "margin-left:2px;")
                delete_button.setAttribute("value", "删除")
                delete_button.setAttribute("id",title_list[i].exerc_id)
                delete_button.setAttribute("onclick",'delete_exerc(event)')
                td.appendChild(edit_button);
                td.appendChild(status_button);
                td.appendChild(delete_button);
                td.width=220;
                td.align = "center";
            }
        }
    }
}

function delete_exerc(event){
    delete_button = event.currentTarget
    ajax=$.ajax({
        url:'/api/v1/practices',
        data:JSON.stringify({"delete_id":delete_button.id}),
        contentType: 'application/json; charset=UTF-8',
        type:'DELETE',
        dataType:'json',
    }).done(function(){
            if(data.status){
                alert(data.message);
            }else{
                alert(data.error);
            }
    });
}