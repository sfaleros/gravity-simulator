from ctypes.wintypes import POINT
from email.policy import default
from msilib.schema import Class
from tkinter import *
import time
import math
import random
import threading




G=6.6743 * 10**(-11)
LforPixel= 10 #meters
roundK= 16
inhibK=0
window = Tk()
window.title('Работа с canvas')
isRun= False
IsRealTime=False
points=[]
lb=0
atoms=[]

windowWidth= window.winfo_screenwidth()-10
windowHeight= window.winfo_screenheight()-50

canvas = Canvas(window,width=windowWidth,height=windowHeight,bg="black",cursor="pencil")
canvas.pack()

 


class Point :
    def __init__(self, masa, angle, speed0 , oper):
        #self.isStoped= False         need new name 
        self.oper=oper
        self.masa = masa 
        self.pos = canvas.coords(oper)
        self.centerx =(self.pos[2]+self.pos[0])/2
        self.centery =(self.pos[3]+self.pos[1])/2

        self.radius= self.pos[2]-self.centerx


        self.vx=(math.cos(math.radians(angle))*speed0)
        self.vy=(math.sin(math.radians(angle))*speed0)

    def Move(self):
        for i in points: 
            if i!= self:
                longAngle = getLongAndAngle(self.centerx, self.centery, i.centerx, i.centery)
                long=longAngle[0]

                if long<self.radius+i.radius:
                    return stop(self,i)
                    #self.isStoped= True
                    #i.isStoped= True
                else:
                    angl= longAngle[1]
                    f= G*self.masa*i.masa/(long**2) # H 
                    a = f/self.masa
                    self.vx=self.vx+ (math.cos(math.radians(angl)))*a
                    self.vy=self.vy+ (math.sin(math.radians(angl)))*a




        canvas.move(self.oper, self.vx/LforPixel,  self.vy/LforPixel )
        canvas.update()

        #canvas.create_line(self.centerx, self.centery, self.centerx +self.vx/LforPixel, self.centery +self.vy/LforPixel, fill="red")
        self.centerx += self.vx/LforPixel
        self.centery += self.vy/LforPixel

    
def onScale(val):
    global roundK
    roundK = int(float(val))

def inhibitor(val):
    global inhibK
    inhibK = int(float(val))    


def stoper():
    global isRun
    isRun= not isRun
    print("11111111111111111111111111111111111")
    if isRun:
        loop()




def getLongAndAngle(x1,y1,x2,y2):
    longKv= (x2-x1)**2 + (y2-y1)**2  

    long = math.sqrt(longKv) 

    angle= math.atan2((y2 - y1), (x2-x1))  / math.pi * 180
        

    return [round(long,roundK),round(angle,roundK)]



def stop(p1,p2):
    global points

    canvas.delete(p1.oper)
    canvas.delete(p2.oper)
    canvas.update()

    if p1 in points:
        points.remove(p1)
        print("-------------------------1ok" )

    if p2 in points:
        points.remove(p2)
        print("-------------------------2ok")


        #print("ddddddddddddddd", points, p1)
        #points.remove(p1)
        #points.remove(p2)
        

        #print(type(points))
    masa= p1.masa+p2.masa

    if p1.radius/p2.radius >2 :
        centerx= p1.centerx
        centery= p1.centery
    elif p2.radius/p1.radius >2:
        centerx= p2.centerx
        centery= p2.centery
    else:
        centerx=(p1.centerx+p2.centerx)/2
        centery=(p1.centery+p2.centery)/2

    vx= (p1.vx*p1.masa + p2.vx*p2.masa)/masa
    vy= (p1.vy*p1.masa + p2.vy*p2.masa)/masa

    radius = round(math.sqrt((p1.radius**2) +(p2.radius**2) ),roundK)
    print(p1.radius,p2.radius,radius)

    pp= canvas.create_oval([centerx-radius,centery-radius],[centerx+radius,centery+radius],fill="red")
    newPoint=Point(masa, 0,0,pp)
    newPoint.radius=radius
    newPoint.vx= vx
    newPoint.vy= vy
    points.append(newPoint)







def loop():
    global points
    while isRun:
        currentTime= time.time()
        for point in points:
            point.Move()
                #t = threading.Thread(target=point.Move())
                #t.start()
        timer=time.time()-currentTime

        if IsRealTime and timer<1 :
            time.sleep(1-timer)
        else:
            time.sleep(inhibK/100)

        lb.config(text = round(1/(time.time()-currentTime),1))
            
    

        
        #canvas.move(point1,-1,0)
        #canvas.update()
def GraviSimulator():
    global points
    global lb

    StartBtn1.destroy()
    StartBtn2.destroy()





    

    #canvas = Canvas(window,width=1300,height=1000,bg="gray",cursor="pencil")


    btn1 = Button(window,height=1,width=10,bg="red",text="on/off",command=stoper)
    btn1.place(x=windowWidth/2.1,y=windowHeight-50)

    scale = Scale(window, from_=0, to=16, command=onScale, orient=HORIZONTAL)
    scale.place(x=windowWidth/1.8,y=windowHeight-50)

    scaleInhibitor = Scale(window, from_=50, to=0, command=inhibitor, orient=HORIZONTAL)
    scaleInhibitor.place(x=windowWidth/1.5,y=windowHeight-50)

    lb= Label(window,width=9, height=1, text="000")
    lb.place(x=0,y=0)
    #btn1.bind("<Button-1>", stoper)



    point1 = canvas.create_oval([648,408],[670,430],fill="pink")  #point1 = canvas.create_oval([915,775],[965,825],fill="pink")
    point2= canvas.create_oval([548,568],[650,670],fill="blue")
    point3= canvas.create_oval([360,350],[370,360],fill="black")

    points1=[point1,point2,point3]

    #for pointt in points1:
    #    canvas.move(pointt,900,500)
    #    canvas.update()

    point1=Point(100000, 170,40,point1)
    point2=Point(600000000000000, 270,0,point2)
    point3=Point(6000000, 90,60,point3)
    
    points=[point1,point2, point3]


    for i in range(15):
        xrand=random.randint(40,windowWidth-30)
        yrand=random.randint(40,windowHeight-30)
        masa=random.randint(10000,1000000000000)
        pp= canvas.create_oval([xrand, yrand],[xrand+6 + masa/500000000000,yrand+6+masa/500000000000],fill="blue")
        pointrand=Point(masa, random.randint(0,360),random.randint(0,9000)/100,pp)
        points.append(pointrand)


    for i in range(15):
        xrand=random.randint(40,windowWidth-30)
        yrand=random.randint(40,windowHeight-30)
        pp= canvas.create_oval([xrand, yrand],[xrand+4,yrand+4],fill="yellow")
        pointrand=Point(random.randint(1,100), random.randint(0,360),random.randint(0,2000)/100,pp)
        points.append(pointrand)




    




def chemSimulator():
    StartBtn1.destroy()
    StartBtn2.destroy()

    class Atom(Point):
        def __init__(self,name, *args, **kwargs ):
            super().__init__(*args, **kwargs)
            self.name = name
    
    #atom1= canvas.create_oval([548,568],[650,670],fill="yellow")
    #a= Atom("hidrogen", 100000, 170,40,atom1)
    #print(a.name)


    for i in range(15):
        xrand=random.randint(40,windowWidth-30)
        yrand=random.randint(40,windowHeight-30)
        pp= canvas.create_oval([xrand, yrand],[xrand+2,yrand+2],fill="yellow")
        atomrand=Atom("hidrogen", 1, random.randint(0,360),random.randint(0,9000)/100,pp)
        atoms.append(atomrand)

    for i in range(15):
        пуxrand=random.randint(40,windowWidth-30)
        yrand=random.randint(40,windowHeight-30)
        pp= canvas.create_oval([xrand, yrand],[xrand+3,yrand+3],fill="blue")
        atomrand=Atom("oxigen",16, random.randint(0,360),random.randint(0,9000)/100,pp)
        atoms.append(atomrand)

 

StartBtn1 = Button(window,height=10,width=19,bg="red",text="graviti simulator",command=GraviSimulator )
StartBtn1.place(x=1400,y=850)

StartBtn2 = Button(window,height=10,width=19,bg="blue",text="chemical simulator",command=chemSimulator)
StartBtn2.place(x=1550,y=850)




window.mainloop()