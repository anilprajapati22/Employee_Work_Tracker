window.onload = function WindowLoad(event) {
    window.resizeTo(500,600)
    eel.getUserDetails()(passToHtml)
    
}
var s;
var pName;
function passToHtml(data)
{
    document.getElementById("setUname").innerHTML = data[0]["name"];
    document.getElementById("ifadmin").innerHTML = "admin";
}


function logout(){
window.location = "sgn_login.html";
}

//sgn
function addEmpToProject(){
    eel.getSgnData()(sgn_btnForAddEmp)

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
        newbtn.id = s[i];                      //add an id
        newbtn.type = "button";
        newbtn.value = s[i];       
        newbtn.onclick = function() { submitEmpData(this); };
        div1.appendChild(newbtn);                 //
    }    

}
function submitEmpData(uname){
    console.log("sgn in side function");
    console.log(uname.value);
    eel.sgn_addEmpToProject(uname.value,window.pName)
    uname.remove();

}
var add_count =0;
//this function will  add new project

function addProject(){
        if (window.add_count == 1)
        {
                var myNode = document.getElementById("add_pro_div");
                while (myNode.firstChild) {
                    myNode.removeChild(myNode.lastChild);
                }
            window.add_count = 0
        }
        window.pName = document.getElementById("projectName").value
        if (pName.length != 0){
            console.log(window.pName)  
            eel.addProjectPy(window.pName)(sgn_btnForAddEmp) 
            window.add_count += 1;
        }
        else{
            alert("please enter project name")
        }
}
var rpName;
function remProject(){
    window.rpName = document.getElementById("projectName").value;
        if (rpName.length != 0){
            eel.remProjectPy(window.rpName) 
           
        }
        else{
            alert("please enter project name")
        }    
}
