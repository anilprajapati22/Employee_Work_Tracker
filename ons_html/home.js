window.onload = function WindowLoad(event) {
    window.resizeTo(400,450)
    //setInterval(function(){ eel.sgn_screen() }, 10000);    will take ss in every 10 s 
    eel.getUserDetails()(pyGetDataPassToHtml);
}

function pyGetDataPassToHtml(data)
{

    document.getElementById("setUname").innerHTML = "Emp id :- "+data[0]["name"];
    var i;
    var pl =data[0]["project"];
    console.log(pl);
    var div1 = document.getElementById("list_projectDiv");
    for(i=0;i<pl.length;i++)
    {
        console.log("sgn working");
        newbtn = document.createElement("input");   //create a input button
        newbtn.id = pl[i];                      //add an id
        newbtn.style.margin = "5px";
        newbtn.type = "button";
        newbtn.value = pl[i];       // give value to button that is name of project
        newbtn.onclick = function() { selectProject(this); };
        div1.appendChild(newbtn); 
        if (i%2 == 1){
           newbr = document.createElement("br");         
           div1.appendChild(newbr);
        }
    }    


}
var current_project;
function selectProject(uname){
    window.current_project = uname.value;
    console.log("sgn in side select pro");
    console.log(uname.value);
    document.getElementById("list_projectDiv").remove();
    eel.setcurrentProject(window.current_project);
    console.log(current_project);
    show_timer();   
}

function show_timer(){
window.location = "start_stop_counter.html";    

}

function logout(){
window.location = "sgn_login.html";
}


