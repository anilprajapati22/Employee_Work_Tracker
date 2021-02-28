function getAuthentic(){
    var eid = document.getElementById("empid").value 
    var passwd = document.getElementById("password01").value
    eel.authenticate(eid,passwd)(setVerified)
}

function setVerified(v){

    if (v[0] && v[1] == "emp")
    {
        window.location = "home.html";
    }
    else if (v[0] && v[1] == "admin"){
        window.location = "admin_home.html";
    }
    else {
        document.getElementById("seeauth").innerHTML = "you are not authorised user please try again";
    }
}


