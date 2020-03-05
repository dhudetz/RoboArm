from math import pi, sin, cos
from numpy import deg2rad
import vis
from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
import threading
import sys

class visualizer(ShowBase):

    def __init__(self):
        ShowBase.__init__(self)
        w, h = 2000, 750
        self.thickness=10

        props = WindowProperties()
        props.setSize(w, h)

        base.win.requestProperties(props)
        base.setBackgroundColor(0,0,0)
        self.a=31.5
        self.b=31.5
        self.c=7
        self.t0=0
        self.center = LVector3f(0,0,0)
        self.back=vis.backEnd(self.a,self.b,self.c)
        self.aSeg = LineSegs("a")
        self.bSeg = LineSegs("b")
        self.cSeg = LineSegs("c")
        self.aSeg.setColor(1, 0 ,0 ,1)
        self.bSeg.setColor(0, 1 ,0 ,1)
        self.cSeg.setColor(0, 0 ,1 ,1)
        self.segments=(self.aSeg,self.bSeg,self.cSeg)
        for s in self.segments:
            s.setThickness(self.thickness)
        self.segmentNodes=[]
        for s in self.segments:
            self.segmentNodes.append(s.create(False))
        self.taskMgr.add(self.spinCameraTask, "SpinCameraTask")
        self.taskMgr.add(self.moveArmTask, "moveArmTask")

    def changeSegments(self,a,b,c):
        self.a=a
        self.b=b
        self.c=c
        self.back=vis.backEnd(self.a,self.b,self.c)

    def drawSegments(self, t0, t1, t2, t3):
        self.t0=180+t0
        for sNode in self.segmentNodes:
            np=NodePath(sNode)
            np.removeNode()
        (ar,az,br,bz,cr,cz)=self.back.calculateComponents(t1,t2,t3)
        aVector = LVector3f(ar,0,az)
        bVector = LVector3f(br,0,bz)
        cVector = LVector3f(cr,0,cz)
        POI = self.center+aVector+bVector+cVector
        vertices=[self.center,self.center+aVector,self.center+aVector+bVector,POI]
        self.aSeg.drawTo(vertices[0])
        self.aSeg.drawTo(vertices[1])
        self.bSeg.drawTo(vertices[1])
        self.bSeg.drawTo(vertices[2])
        self.cSeg.drawTo(vertices[2])
        self.cSeg.drawTo(vertices[3])
        self.segmentNodes=[]
        for s in self.segments:
            self.segmentNodes.append(s.create(False))
        for vertex in vertices:
            vertexSegment=LineSegs("v")
            vertexSegment.setColor(1,1,1,1)
            vertexSegment.setThickness(self.thickness*10)
            vertexSegment.drawTo(vertex+LVector3f(0,-1,0))
            vertexSegment.drawTo(vertex+LVector3f(0,1,0))
            self.segmentNodes.append(vertexSegment.create(False))
        for sNode in self.segmentNodes:
            render.attachNewNode(sNode)

    def spinCameraTask(self, task):
        angleDegrees = task.time * 100.0
        angleRadians = angleDegrees * (pi / 180.0)
        self.camera.setPos(300 * sin(deg2rad(self.t0)), -300 * cos(deg2rad(self.t0)), 0)
        self.camera.setHpr(self.t0, 0, 180)
        #self.camera.setPos(250 * sin(angleRadians), -250 * cos(angleRadians), -20)
        #self.camera.setHpr(angleDegrees, 0, 180)
        return Task.cont

    def moveArmTask(self, task):
        angleDegrees = task.time * 1000.0
        for s in self.segments:
            s.reset()
        #self.drawSegments(angleDegrees,angleDegrees/2,angleDegrees/4)
        return Task.cont

    def close(self):
        sys.exit()

app = visualizer()
previousAngles=currentAngles=resetAngles=(0,0,0,0)
done=False
file=None

def userInputLoop():
    global done, file, circles, currentAngles, previousAngles, back, app
    print("\nMegarm Visualizer")
    f=None
    while not done:
        userInput = input("Import coordinate r z? Type \'help\' for more options: ")
        words=userInput.split()
        if len(words)==3:
            if file!=None:
                servoAngles=vis.getServoAngles(file, float(words[0]),float(words[2]))
                app.drawSegments(float(words[1]), servoAngles[0],servoAngles[1],servoAngles[2])
            else:
                print("File not imported.")
        elif len(words)==2:
            if(words[0]=='f'):
                (file,a,b,c) = vis.getFile(words[1])
                if file!=None:
                    app.changeSegments(a,b,c)
                    currentAngles=resetAngles
                    previousAngles=resetAngles
                    app.drawSegments(resetAngles[0],resetAngles[1],resetAngles[2],resetAngles[3])
            else:
                print("Improper syntax")
        elif len(words)==0:
            print("Improper syntax")
        elif words[0]=="help":
            print("To enter a coordinate just type the r and z.")
            print("Example: 15.0 10.0")
            print("To change hdf5 file reference, type f and the file name.")
            print("Example: f 31.5-31.5-7.0.hdf5")
            print("To quit, type q.")
        elif words[0]=="q":
            done=True
            app.close()
        else:
            print("Improper syntax")

try:
    userThread = threading.Thread(target=userInputLoop, args=())
    userThread.start()
except:
    print("Error: unable to start thread")

app.run()
