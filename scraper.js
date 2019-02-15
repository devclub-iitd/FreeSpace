function loadHTML(url,storage){
    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange=function(){ 
        if(xhr.readyState == 4){
            var ans = xhr.responseText;
            storage.innerHTML =ans.trim();
        } 
    }; 
    xhr.open("GET", url , true);
    xhr.send(null); 
} 

function accessByDOM(url,id){
    var responseHTML = document.getElementById(id);
    loadHTML(url, responseHTML);
}