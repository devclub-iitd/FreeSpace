function preProcessTable(id){
    var content = document.getElementById(id).innerHTML;
    var l = document.getElementById(id).childNodes;
    var tableHead; //Dataframe of the table
    for (var a = 0 ; a<l.length; a++){
        if (typeof(l[a].data) != "string"){
			tableHead = l[a];
        }
    };
    var tableChild = tableHead.childNodes;
    var finalTable = [];
    for (var a = 0 ; a< tableChild.length; a++){
        if (typeof(tableChild[a].data) != "string"){
            finalTable[finalTable.length] = tableChild[a];
        }
    }
    return finalTable;
}
function merge(){
    finalTable = preProcessTable("storage");
    // finalTable has element 0 as thead while the other as tbody
    var table_head_row = finalTable[0].rows[0];
    for (var i= 1,col; col=table_head_row.cells[i];i++){
        col.setAttribute("class","topRow");
    }
    var table_body = finalTable[1];
    for (var i = 0,row; row = table_body.rows[i];i++){
        var col;     
        var j = 1;
        var last_ind = row.cells.length;
        while (col = row.cells[j]){
            var col2
            var ct = 0;
            try{
                while((row.cells[j+ct]).innerHTML == (col).innerHTML){
                    ct++;
                }
            }catch(err){

            }
            finally{
                var temp_ct = ct;
                ct--;
            while (ct != 0){
                row.deleteCell(j);
                ct--;
            }
            try{
                row.cells[j].setAttribute("colspan",temp_ct);
                
            }
            finally{
                if (row.cells[j].innerHTML == 'Free'){
                    row.cells[j].style.background="";
                    row.cells[j].innerHTML = "Free Space"
                } else if(row.cells[j].innerHTML == 'Not Allowed'){
                    row.cells[j].style.background="red";
                    // row.cells[j].innerHTML = "Free Space";
                } else if (row.cells[j].innerHTML == 'Exam'){
                    row.cells[j].style.background="yellow";
                }
                else{
                    // row.cells[j].innerHTML = "Class Going On...";
                    row.cells[j].style.background="lightgray";
                }
                j++;
            }
            }
        }
    }
}

function smallTableEdit(id){
    var table_list = document.getElementsByClassName("dataframe");
    var tableF = preProcessTable(id);
    var table_body = tableF[1];
    var table_head = tableF[0];
    try{
        table_head.rows[0].deleteCell(0);  //Removes an extra column.
        table_head.rows[0].deleteCell(0); //Removes the header 
    }catch(err){}
    finally{}
    for (var i = 0,row;row = table_body.rows[i];i++){
        row.deleteCell(0);
    }
    if (table_body.rows.length == 0) {
        var addedRow = table_body.insertRow(0);
        var newCell = document.createElement('td');
        newCell = addedRow.insertCell(0);
        newCell.innerText = "All LHs are free."
    }
    for (var i = 0;i<table_list.length;i++){
        var currTable = table_list[i];
        if (currTable.rows[0].cells.length <= 1){
        currTable.setAttribute("class","smallTables");
        }
    }

}
