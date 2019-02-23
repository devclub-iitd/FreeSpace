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
    // finalTable has element 0 as thead w+hile the other as tbody
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
                if (row.cells[j].innerHTML == '0'){
                    row.cells[j].innerHTML = "Free Space"
                } else{
                    // row.cells[j].innerHTML = "Class Going On...";
                    row.cells[j].style.background="lightgray";
                }
                j++;
            }
            }
        }
    }
}
function allRoomMerge(){
    finalTable = preProcessTable("allRooms");
    tableBody = finalTable[1];
    var start_cell,start_cell_row_index,end_row_index,end_col_index;
    end_col_index = tableBody.rows[0].cells.length;
    for (var i = 0,row;row = tableBody.rows[i];i++){
        var curr_row_head = row.cells[0].innerHTML;
        for (var j = 1,col; col = row.cells[j]; j++){
            if (col.innerHTML == ""){
                col.innerHTML = "All LHs Free";
                col.style.fontWeight = "bold";
            }
        }
        if (curr_row_head == "13:00"){
            start_cell = row.cells[1];
            start_cell_row_index = i;;
        }
        if (curr_row_head == "16:30"){
            end_row_index = i;
        }
    }
    for (var i = start_cell_row_index,row;row = tableBody.rows[i],i<=end_row_index;i++){
        for (var j = 1;j<end_col_index-1;j++){
            row.deleteCell(1);
        }
        row.cells[1].setAttribute("colSpan",end_col_index-1);
        row.cells[1].innerHTML="All LHs are free(Not Counting Tutorials)."
        if (i != start_cell_row_index){
            row.deleteCell(1);
        }else{
            row.cells[1].setAttribute("rowSpan",(end_row_index-start_cell_row_index+ 1));
            row.cells[1].innerHTML="All LHs are Free(Not Counting Tutorials...)";
            row.cells[1].style.fontWeight = "bold";

        }
    }
};

function smallTableEdit(id){
    var tableF = preProcessTable(id);
    var table_body = tableF[1];
    var table_head = tableF[0];
    table_head.rows[0].deleteCell(0);
    for (var i = 0,row;row = table_body.rows[i];i++){
        row.deleteCell(0);
    }
}
