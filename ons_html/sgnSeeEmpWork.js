window.onload = function WindowLoad(event) {
    window.resizeTo(500,600)
    eel.getUserDetails()(passToHtml)
    eel.getSameCompEmpName()(sgn_btnForAddEmp);
}


function sgn_btnForAddEmp(sdata){
    window.s = sdata;
    var i;
    var si;    
    var div1 = document.getElementById("add_pro_div");

    for(i=0;i<s.length;i++)
    {
        console.log(s[i]);
        newbtn = document.createElement("input");   //create a div
        newbtn.id = "btnEmp";                      //add an id
        newbtn.type = "button";
        newbtn.value = s[i];       
        newbtn.onclick = function() { showEmpData(this); };
        div1.appendChild(newbtn);                 //
    }    

}

function showEmpData(uname){
    if (document.getElementById("divhis")){
    document.getElementById("divhis").remove();}
    
    document.getElementById("showEmpDetails").remove();
    eel.getUserDetailsForShow(uname.value)(pyGetOldWokDataPassToHtml);
    var div1 = document.createElement("div");
    div1.id = "showEmpDetails";
    document.body.appendChild(div1);
}

var uName;
var historyList;
function pyGetOldWokDataPassToHtml(data){

    document.getElementById("setUname").innerHTML = "Emp id :- "+data["name"];
    document.getElementById("ifadmin").innerHTML = "";
    window.uName = data["name"];
    var i;
    var j;
    var pl =data["project"];
    var insidePl;
    console.log(pl);
    var div1; 
    data1 = data[0];
    var divput = document.getElementById("showEmpDetails");
    for(i=0;i<pl.length;i++)
    {
        div1 = document.createElement("div");
        div1.id = "projectDiv";
        divput.appendChild(div1);
        newbtn = document.createElement("h3");   //create a input button
        newbtn.id = "Projecth3";                      //add an id
        newbtn.innerHTML = pl[i];       // give value to button that is name of project
        div1.appendChild(newbtn); 
        insidePl = data[pl[i]];
        window.historyList = insidePl;
        for(j=0;j<insidePl.length;j++){

            newbtn = document.createElement("p");   //create a input button
            newbtn.id = "Projectp";                      //add an id
            newbtn.innerHTML =  insidePl[j][3] +" : "+ insidePl[j][1]+" : " + " work for : " + insidePl[j][2] + " seconds" ; 
            div1.appendChild(newbtn);        

            newbtn = document.createElement("p");
            newbtn.id = "Workper"               
            newbtn.innerHTML = " Keyboard : "+insidePl[j][4] +"%" + " Mouse : "+insidePl[j][5] + "%" ;
            div1.appendChild(newbtn);                 //

            newbtn = document.createElement("button");     
            newbtn.id = "projectDiv"+i;                      //add an id
            newbtn.type = "button";
            newbtn.value = insidePl[j][6];
            newbtn.innerHTML ="Browser History";
            newbtn.onclick = function() { showHistoryData(this);
                                        
                                         };
            div1.appendChild(newbtn);                 //
                        
            
                    
        }
    }

}



function showHistoryData(btn){
    if (document.getElementById("divhis")){
    document.getElementById("divhis").remove();}

    var i;
    s=btn.value;
    console.log(btn.id);
    var div1=document.createElement("div");
    div1.id="divhis";
    document.body.appendChild(div1); 
    var l=[];   
    var l1=[];
    for(i=0;i<s.length;i++)
    {
        if (s[i] == ","){
        l.push(i);
        }

    }
    for(i=0;i<l.length;i++)
    {
        l1.push(s.slice(l[i]+1,l[i+1]));

    }    

    for(i=0;i<l1.length;i++){
        newbtn = document.createElement("p");   //create a input button
        newbtn.id = "Projectp";                      //add an id
        newbtn.innerHTML = l1[i]; 
        div1.appendChild(newbtn);        
    
    }   
}
function passToHtml(data)
{
    document.getElementById("setUname").innerHTML = data[0]["name"];
    document.getElementById("ifadmin").innerHTML = "admin";
}

