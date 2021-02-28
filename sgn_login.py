import eel
import pymongo
import time
import pyautogui as gui
from datetime import datetime as dt
from pynput.keyboard import Key, Listener
from pynput import mouse
import threading
import sqlite3
from pwd import getpwuid
from platform import system
from os import getuid
import os



sgncli = pymongo.MongoClient("mongodb://localhost:27017/")
#connection
sgndb=sgncli["sgn_pymongo"]
sgncol = sgndb["sgn_emp"]
sgnworkcol = sgndb["sgn_emp_work"]
eel.init("ons_html")
l=[]
l2=[]
sl=[]
current_project = "" # for track of which project is clicked
@eel.expose
def authenticate(eid,passwd):
    s=sgncol.find({"name":eid,"passwd":passwd})
    s1=sgnworkcol.find({"_name":eid,})
    global l,l2
    l=list(s) 
    sl=list(s1) 
    l[0].update(sl[0])  
    #print("user details\n",l)
    if len(l) == 0:
        return [False,""]
    elif len(l) == 1 and l[0]["is_admin"] == 1:
        return [True,"admin"]
    elif len(l) == 1 and l[0]["is_admin"] == 0:
        return [True,"emp"]

@eel.expose
def getUserDetails():
    global l
    if len(l) == 1:
        l.append("")
    print("length of list is",len(l))
    return l

@eel.expose
#here uname is for use it second time in admin we can pass use name
def getUserDetailsForShow(uName="jkh"): 
    global l,l2,sl                
    l2 = l
    if uName != "jkh":
        glist = sgnworkcol.find({"_name":uName})
        sl1=list(glist)
        glist = sgncol.find({"name":uName})
        l2 = list(glist)
        l2[0].update(sl1[0])     
    print("sgn first",len(l2))
    print("this is l\n",l2)
    userl=l2[0]
    print("this is l2\n",userl)
    for i in userl["project"]:
        for j in range(len(userl[i])):
            if type(userl[i][j][1]) != str:
                d=userl[i][j][1]
                userl[i][j][1] = str(d.day)+":"+str(d.month)+":"+str(d.year)
    l2=[]
    return userl


@eel.expose
def getUserDetailsForTime():
    #to pass data of selected project into timer page
    global l
    l[1]=current_project
    return l




ssc=0
t1=0
screenshotc=0
screenShotList=[]
#make this function take ss every time give new name
@eel.expose
def sgn_screen(uName1):
    global ssc,t1,workStartingTime,screenshotc,screenShotList
    sgnDirectory = os.getcwd()
    if not os.path.exists(sgnDirectory+"/ons_html/sgnScreenShot"):
        if not os.path.exists(sgnDirectory+"/ons_html"):    
            os.mkdir("ons_html")
        os.mkdir("ons_html/sgnScreenShot")
    cDate = dt.now()
    img=gui.screenshot('ons_html/sgnScreenShot/'+str(uName1)+str(cDate.day)+str(cDate.minute)+str(cDate.second)+str(screenshotc)+'.png') 
    print(sgnDirectory)       
    sgn_img = str(uName1)+str(cDate.day)+str(cDate.minute)+str(screenshotc)+'.png'
    screenShotList.append(sgn_img)
    print(sgn_img)
    screenshotc +=1
    #return sgn_img        
    
    #img=gui.screenshot('ons_html/sgn_01.png')            
    #return "sgn_01.png"        
    

@eel.expose
def getSgnData():
    print(l)
    s=["sgn01","sgn02","sgn03"]
    return s    
@eel.expose
def addProjectPy(np):
    print(l)
    old_n={"name":l[0]["name"]} #current user name
    p = l[0]["project"] #project list
    p.append(np)
    up_p = {"$set":{"project":p}}
    sgncol.update_one(old_n,up_p) # add new project to project list in db
    cName=l[0]["com_name"]
    slist=sgncol.find({"com_name":cName},{"_id":0,"name":1}) #give only id and name
    sl = list(slist)
    nl=[] # it will give all  name releted to admin compony
    for i in sl:
        nl.append(i["name"])
    print(nl)
    nl.remove(l[0]["name"]) # will remove name of admin from list
    return nl

@eel.expose
def remProjectPy(np):
    ndb = sgncol.find()
    nlist = list(ndb)
    for i in nlist:
        if np in i["project"]:
            print("sgn")
            old_n={"name":i["name"]}
            p_list = i["project"]
            p_list.remove(np)
            up_p = {"$set":{"project":p_list}}
            sgncol.update_one(old_n,up_p)


@eel.expose
def getSameCompEmpName():
    cName=l[0]["com_name"]
    ulist = slist=sgncol.find({"com_name":cName},{"_id":0,"name":1})        
    sl = list(slist)
    nl=[] # it will give all  name releted to admin compony
    for i in sl:
        nl.append(i["name"])
    print(nl)
    nl.remove(l[0]["name"]) # will remove name of admin from list
    return nl


@eel.expose
def sgn_addEmpToProject(uname,pName):
    print(uname,pName)
    old_n={"name":uname} #clicked button name which is user that admin want to add in project
    u_ditg = sgncol.find(old_n)
    u_dit = list(u_ditg)
    plist = u_dit[0]["project"]
    plist.append(pName) # add new project to clicked user's project list
    up_p = {"$set":{"project":plist}} 
    sgncol.update_one(old_n,up_p)                  
    up_p1 = {"$set":{pName:[]}}       
    sgnworkcol.update_one({"_name":uname},up_p1) # add new project to project list in db
 
@eel.expose
def addTimerDataPy(uname1,ts,cwp,clow):
    global workStartingTime,screenShotList
    old_n={"_name":uname1}
    u_ditg = sgnworkcol.find(old_n)
    u_dit = list(u_ditg)
    ptlist = u_dit[0][cwp]
    listOfPercentage = getsgnLengthOfListTime(ts)
    print("\n\n",listOfPercentage)
    ptlist.append([workStartingTime,dt.now(),ts,clow,listOfPercentage[0],listOfPercentage[1],getBrowserHistory(workStartingTime),screenShotList])
    u_dict={"$set":{cwp:ptlist}}    
    sgnworkcol.update_one(old_n,u_dict)        
    #sgnworkcol.update_one(old_n,u_dict)   

def getsgnLengthOfListTime(totals):
    global keyPressTime,mouse_event_list,sgncheck,sgnListCheck,onlyOnesTime
    setOfKeyTime =set(keyPressTime)
    setOfMouseTime = set(mouse_event_list)    

    lenofKeylist= len(setOfKeyTime)      
    lenofMouselist = len(setOfMouseTime)

    keyParcentage = round((lenofKeylist*100)/totals)
    mouseParcentage = round((lenofMouselist*100)/totals) 
    sgncheck =False
    sgnListCheck = False
    print(keyPressTime,"\n\n\n",mouse_event_list)
    keyPressTime=[] #after it stored in db it will clear list   
    mouse_event_list = []
    onlyOnesTime = True
    return [keyParcentage,mouseParcentage]       
@eel.expose
def setcurrentProject(csp):
    global current_project
    current_project = csp
    print("set :",current_project)

#to get privious work data
@eel.expose
def getOldWork(cwp,uname1):
    print(cwp,uname1)
    old_n={"_name":uname1}
    u_ditg = sgnworkcol.find(old_n)
    u_dit = list(u_ditg)
    t_list = u_dit[0][cwp]
    for i in range(len(t_list)):
        d=t_list[i][1]
        t_list[i][1] = str(d.day)+":"+str(d.month)+":"+str(d.year)
    print(t_list)
    return t_list
    

#https://www.w3schools.com/jsref/met_win_setinterval.asp
#this is link for see other timer program

sgncheck = False #to close key function if it is True
sgnListCheck = False # to start list append of keys if it is True
keycount = 0
keyPressTime = []
def sgn_keyEvent():
    global keycount,sgnListCheck,sgncheck,keycount,sgnt1,sgnt2
    def on_press(key):
        global keycount,sgnListCheck,sgncheck,keycount
        if sgncheck :
            print("stop button pressed")
            #print(keyPressTime)
            sgnListCheck =False
            #return False
        if sgnListCheck:
            keyPressTime.append(int(time.time()))
            
                        
        #print('{0} pressed'.format(
         #   key))
        if key == Key.esc:
            # Stop listener
            return False
        if not sgnt1.isAlive() :
            print("other process is over i am going to die")
            return False
    # Collect events until released
    with Listener(
            on_press=on_press,
            ) as listener:
        listener.join()    

sgnt1=""
sgnt2=""
sgnt3=""

mouse_event_list=[]
def sgn_mouseEvent():
    
    def on_moveM(x, y):
        global mouse_event_list,keycount,sgnListCheck,sgncheck,keycount,sgnt1,sgnt2
        if not sgnt1.isAlive() :
            print("other process is over i am going to die")
            return False

        if sgncheck :
         #   print("stop button pressed")
            #print(mouse_event_list)
            sgnListCheck = False
            #return False

        if sgnListCheck:
            #if it is true (only when we press start button) it will store data of mouse events 
            mouse_event_list.append(int(time.time()))
        
       # print('Pointer moved to {0}'.format(
        #    (x, y)))

    def on_clickM(x, y, button, pressed):
        global mouse_event_list,keycount,sgnListCheck,sgncheck,keycount,sgnt1,sgnt2
        if not sgnt1.isAlive() :
            print("other process is over i am going to die")
            return False

        if sgncheck :
            print("stop button pressed")
            #print(mouse_event_list)
            sgnListCheck = False
            #return False


        if sgnListCheck:
            mouse_event_list.append(int(time.time()))

       # print('{0} at {1}'.format(
        #    'Pressed' if pressed else 'Released',
         #   (x, y)))

    def on_scrollM(x, y, dx, dy):
        global mouse_event_list,keycount,sgnListCheck,sgncheck,keycount,sgnt1,sgnt2
        if not sgnt1.isAlive() :
            print("other process is over i am going to die")
            return False

        if sgncheck :
            print("stop button pressed")
            #print(mouse_event_list)
            sgnListCheck = False                
            #return False


        if sgnListCheck:
            mouse_event_list.append(int(time.time()))

       # print('Scrolled {0} at {1}'.format(
        #    'down' if dy < 0 else 'up',
        #    (x, y)))



    # Collect events until released

    with mouse.Listener(
            on_move=on_moveM,
            on_click=on_clickM,
            on_scroll=on_scrollM) as listener:
        listener.join()



@eel.expose
def sgnOn():
    global sgnt1,sgnt2
    sgnt1 = threading.Thread(target=sgnONWindow)
    sgnt2 = threading.Thread(target=sgn_keyEvent)
    sgnt3 = threading.Thread(target=sgn_mouseEvent)            
    sgnt1.start()
    sgnt2.start()
    sgnt3.start()
    sgnt1.join()
    sgnt2.join()
    sgnt3.join()

workStartingTime = "" #for get the browser histrory from starting of work
onlyOnesTime = True
@eel.expose
def sgnStartKeyListenerPy(ds):
    global listOfKey,sgnListCheck,sgncheck,workStartingTime,onlyOnesTime
    if onlyOnesTime:
        workStartingTime = dt.now()
        onlyOnesTime = False  
    #ds = Fasle it will stop 
    #ds = true it will start appending list  
    if ds:
        sgnListCheck = True
    else :
        sgncheck =True
@eel.expose
def sgnHoldKey():
    global sgnListCheck
    sgnListCheck =False

def sgnONWindow():
    eel.start("sgn_login.html", size=(500,400))

################################ for browser history


def sgnGetChromHistory(dateAndTime):
    global currentPcUser
    os.system('cp /home/'+currentPcUser+'/.config/google-chrome/Default/History /home/'+currentPcUser)   
    con = sqlite3.connect('/home/'+currentPcUser+'/History')
    scur = con.cursor()
    scur.execute("SELECT url,title,datetime((last_visit_time/1000000)-11644473600, 'unixepoch','localtime') as sgntime from urls where sgntime >'"+str(dateAndTime)+"'")
    lscb=scur.fetchall()
    lscb1=[]
    for i in lscb:
        lscb1.append([i[0],i[1]])

    os.system('rm /home/'+currentPcUser+'/History')
    return lscb1


currentPcUser = getpwuid( getuid() )[ 0 ]
BrowserHistoryList =[]
def getBrowserHistory(dateAndTime):
    global BrowserHistoryList,currentPcUser
    if system() == 'Linux' :
        unixTime = dateAndTime.timestamp()*1000000
        os.system('cp /home/'+currentPcUser +'/.mozilla/firefox/xk1uxyq9.Parrot/places.sqlite /home/'+currentPcUser)
        con = sqlite3.connect('/home/'+currentPcUser +'/places.sqlite')
        scur = con.cursor()
        scur.execute("select id,last_visit_date,url,title from moz_places where last_visit_date >"+str(unixTime))
        for i in scur.fetchall():
#            print(i[2])
#            print(i[3])
            BrowserHistoryList.append([i[2],i[3]])
        chromHistory=sgnGetChromHistory(dateAndTime)
        print(len(BrowserHistoryList))
        BrowserHistoryList = BrowserHistoryList +[" "]+chromHistory
#        print(BrowserHistoryList)
#        print(len(BrowserHistoryList))
        for i in BrowserHistoryList:
            print(i[0]) 
        return BrowserHistoryList    
        con.close()
        os.system('rm /home/'+currentPcUser +'/places.sqlite')



sgnOn()
"""
import pymongo
sgncli = pymongo.MongoClient("mongodb://localhost:27017/")
from datetime import datetime as dt
sgndb=sgncli["sgn_pymongo"]
sgncol = sgndb["sgn_emp"]
sgnworkcol = sgndb["sgn_emp_work"]
g=sgncol.find()
l=list(g)
for i in l:
    print(i)
"""
