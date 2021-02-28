var sgnSS;
var myTimer;
var c=0;
var mc=0;
var uname;
var start_btn_counter=0;
var currentWorkingProject;
var ts=0;
var lableOfCurrentwork;
window.onload = function WindowLoad(event) {
    window.resizeTo(400,450) 
    eel.getUserDetailsForTime()(pyGetDataPassToHtml);
//    console.log("in timer "+ currentWorkingProject + uname);
    
    
}

function pyGetDataPassToHtml(data)
{
//data has all details of current user
    window.uname = data[0]["name"];
    window.currentWorkingProject = data[1];
    console.log(data);
    console.log("sgn:-"+window.currentWorkingProject);
    console.log("user name :- "+window.uname);    
    document.getElementById("setUname").innerHTML = "Emp id :- "+data[0]["name"];
    eel.getOldWork(currentWorkingProject,uname)(putOldWork);       
}


// this is the function that i want 
//in this mc is minute and c is second ont implement in python
var is_startNotPressed = true;

function clock(){
    window.is_startNotPressed = false;
    if(start_btn_counter == 0){
    eel.sgnStartKeyListenerPy(true);    //to start append time of key stroks in list
    myTimer = setInterval(myClock, 1000);
    window.start_btn_counter = 1;
    sgnSS = setInterval(function(){ eel.sgn_screen(window.uname) }, 10000);   // will take ss in every 60 s
    console.log("start");
    }
     function myClock() {
       document.getElementById("demo_min").innerHTML = mc+":";
       document.getElementById("demo").innerHTML = ++c;
       ++ts; 
       if (c == 60) {
         window.c = 0;
         window.mc +=1;
            
       }
     }
   }

function hold_timer(){
    clearInterval(myTimer);
    window.start_btn_counter = 0;
    eel.sgnHoldKey(); //to Hold append time of key stroks in list
}
function stop_timer(){
//now pss counter data into python
    window.is_startNotPressed = true;
    clearInterval(myTimer);
    clearInterval(sgnSS);
    eel.sgnStartKeyListenerPy(false); //to stop key append in list
    console.log(window.ts); 
    var locw = window.lableOfCurrentwork;
    if (locw == null || locw.length == 0){
        alert("enter lable and stop again");

    }
    else{
        eel.addTimerDataPy(uname,window.ts,window.currentWorkingProject,window.lableOfCurrentwork);
    }
}

function putOldWork(data){

console.log(data);
var i;
var div1;
var div0 = document.getElementById("maindiv");
document.getElementById("privious_work_name").innerHTML = "privious Work : " + window.currentWorkingProject ;
for (i=0;i<data.length;i++){

        div1 = document.createElement("div");
        div1.id = "idoldWork";
        div0.appendChild(div1);    

        newbtn = document.createElement("p");   
        //newbtn.id = "idoldWork";               
        newbtn.innerHTML = data[i][3]+" : " + data[i][1] + " work for : " + data[i][2] + " seconds" ;
        div1.appendChild(newbtn);                 //
    
        newbtn = document.createElement("p");
        //newbtn.id = "idoldWork"               
        newbtn.innerHTML = " Keyboard : "+data[i][4] +"%" + " Mouse : "+data[i][5] + "%" ;
        div1.appendChild(newbtn);                 //
} 
}

function addLableToWork(btn1){

    window.lableOfCurrentwork = document.getElementById("lableOfWork").value;
    var locw = window.lableOfCurrentwork;
    if (locw == null || locw.length == 0){
        alert("enter lable and stop again");

    }
    else{
        btn1.remove();
        var div1 = document.getElementById("lableDiv");
        newbtn = document.createElement("p");   
        newbtn.id = "CurrentWorkLable1";               
        newbtn.innerHTML = window.lableOfCurrentwork;
        div1.appendChild(newbtn);                 //
        document.getElementById("lableOfWork").remove();
    }
}

function goBack(){
    if (window.is_startNotPressed ){
        window.location = 'home.html';
    }
    else{
        if (confirm("your work is started are you sure you want to go back")){
            window.location = 'home.html';
        }
    }
}
