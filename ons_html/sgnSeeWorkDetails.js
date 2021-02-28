window.onload = function WindowLoad(event) {
    window.resizeTo(400,450)
    eel.getUserDetailsForShow()(pyGetOldWokDataPassToHtml);    
    
    
}
var uName;
function pyGetOldWokDataPassToHtml(data){

    document.getElementById("setUname").innerHTML = "Emp id :- "+data["name"];
    window.uName = data["name"];
    var i;
    var j;
    var pl =data["project"];
    var insidePl;
    console.log(pl);
    var div1; 
    data1 = data[0];
    for(i=0;i<pl.length;i++)
    {
        div1 = document.createElement("div");
        div1.id = pl[i];
        document.body.appendChild(div1);
        newbtn = document.createElement("h3");   //create a input button
        newbtn.id = pl[i]+"h3";                      //add an id
        newbtn.innerHTML = pl[i];       // give value to button that is name of project
        div1.appendChild(newbtn); 
        insidePl = data[pl[i]];
        for(j=0;j<insidePl.length;j++){

        newbtn = document.createElement("p");   //create a input button
        newbtn.id = pl[i]+"p";                      //add an id
        newbtn.innerHTML =  insidePl[j][3] +" : "+ insidePl[j][1]+" : " + " work for : " + insidePl[j][2] + " seconds" ; 
        div1.appendChild(newbtn);                 //
                
        }
    }

}
