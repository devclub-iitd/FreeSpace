async function preProcessTable(id){
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
async function merge(){
    finalTable = await preProcessTable("storage");
    // finalTable has element 0 as thead w+hile the other as tbody
    var table_body = finalTable[1];
    for (var i = 0,row; row = table_body.rows[i];i++){
        var col;
        var j = 1;
        while (col = row.cells[j]){
            var ct = 0;
            while ((row.cells[j+ct]).innerHTML == (col).innerHTML){
                ct++;
            }
            while (ct != 0){
                if (col.getAttribute("colSpan") == null){
                    col.setAttribute("colSpan",1)
                };
                var curr_colspan = col.getAttribute("colspan");
                row.deleteCell(j+1);
                col.setAttribute("colspan",curr_colspan+1);
                ct--;
            }
            j++;
        }
    }
}
async function allRoomMerge(){
    finalTable = await preProcessTable("allRooms");
    tableBody = finalTable[1];
    var start_cell,start_cell_row_index,end_row_index,end_col_index;
    end_col_index = tableBody.rows[0].cells.length;
    for (var i = 0,row;row = tableBody.rows[i];i++){
        var curr_row_head = row.cells[0].innerHTML;
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
    }
};
// function delAndMerge(start_cell){

// }