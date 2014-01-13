#Setup
import serial
import math
from datetime import datetime
import time
from Tkinter import *
import tkFont
import Image #This is the PIL Image library
import ImageTk
from random import randint

#Connect to Serial Monitor
#try:
#	ser=serial.Serial('COM5', 9600)
#except:
#	print "Failed to connect to COM5"

class App:

    def __init__(self, master):

        frame = Frame(master, width=200, height=100)
        frame.pack()

        startHeaderImg = Image.open('StartHeader.gif')#.convert('RGBA')
        startHeaderImg = ImageTk.PhotoImage(startHeaderImg)
        startHeader = Label(frame, image = startHeaderImg, width = 115)
        startHeader.image = startHeaderImg
        startHeader.pack()

        Label(frame, text="Where is the piston?").pack()
        fullScale = Scale(frame, from_=0, to=20, orient = VERTICAL,length=400)
        fullScale.pack()

        def manual():
            self.fill = fullScale.get()
            if self.fill < 10:
                print 0
            print self.fill
     #      ser.write(manual)
            self.openManTray()

        def automatic():
            self.fill = fullScale.get()
            if self.fill < 10:
                print 0
            print self.fill
     #   	ser.write(manual)
            self.openAutoTray()

        self.manualButton = Button(frame, text="Manual", command=manual)
        self.manualButton.pack(side=LEFT)

        self.automaticButton = Button(frame, text="Automatic", command=automatic)
        self.automaticButton.pack(side=LEFT)

    def openManTray(self):
    	trayWin = Toplevel()
        trayWin.protocol("WM_DELETE_WINDOW", exit)
    	trayFrame = Frame(trayWin, width=400, height=565)
    	trayFrame.pack()
        root.withdraw()

        mainHeaderImg = Image.open('mainHeader.gif')#.convert('RGBA')
        mainHeaderImg = ImageTk.PhotoImage(mainHeaderImg)
        mainHeader = Label(trayFrame, image = mainHeaderImg)
        mainHeader.image = mainHeaderImg
        mainHeader.pack()

        self.newAmount = 0
        self.cookieCount = 0
        self.cookieMaxAmount = 100
        self.cookiePic = [PhotoImage() for _ in range(self.cookieMaxAmount)]
        self.cookie = [int for _ in range(self.cookieMaxAmount)]
        self.cookieScaleSize = [int for _ in range(self.cookieMaxAmount)]
        self.randTurn = [int for _ in range(self.cookieMaxAmount)]
        self.trayMargin = 50
        self.outputBuffer = []
        self.refillOption = 0
        self.secret = 0

        def onObjectClick(event):
            if (event.x > self.trayMargin and event.x<(400 - self.trayMargin)) and (event.y > self.trayMargin and event.y < (565 - self.trayMargin)):
                if self.cookieCount < self.cookieMaxAmount:
                    self.randTurn[self.cookieCount] = randint(0,360)
                    cookieScaleConstant = 20
                    self.cookieScaleSize[self.cookieCount] = cookieScale.get()*cookieScaleConstant
                    cookiePic = Image.open('RedCookie.gif').convert('RGBA').rotate(self.randTurn[self.cookieCount])
                    cookiePic = cookiePic.resize((self.cookieScaleSize[self.cookieCount], self.cookieScaleSize[self.cookieCount]))
                    self.cookiePic[self.cookieCount] = ImageTk.PhotoImage(cookiePic)
                    self.cookie[self.cookieCount] = trayCanvas.create_image(event.x-self.cookieScaleSize[self.cookieCount]*.5,event.y-self.cookieScaleSize[self.cookieCount]*.5, image = self.cookiePic[self.cookieCount], anchor = NW)
                    self.cookieCount += 1
                    if event.x < 100:
                        self.outputBuffer.append(0)
                    self.outputBuffer.append(event.x)
                    if event.y < 100:
                        self.outputBuffer.append(0)
                    self.outputBuffer.append(event.y)
                    self.outputBuffer.append(cookieScale.get())
                    self.newAmount += 1
                    print(self.outputBuffer)

        
        trayCanvas = Canvas(trayFrame, width = 400, height = 565, bg = "blue")
        self.sheetPic = PhotoImage(file = "Sheet.gif")
        Sheet = trayCanvas.create_image(0, 0, image = self.sheetPic, anchor = NW)
        trayCanvas.tag_bind(Sheet,'<Button-1>', onObjectClick)
        trayCanvas.pack()

        Label(trayFrame, text="Size:").pack()

        cookieScale = Scale(trayFrame, from_=1, to=9, orient = HORIZONTAL,length=300)
        cookieScale.set(3)
        cookieScale.pack()


        def clearTray():
            for i in range(self.cookieMaxAmount):
                trayCanvas.delete(self.cookie[i])
            self.cookieCount = 0
            self.cookiePic = [PhotoImage() for _ in range(self.cookieMaxAmount)]
            self.cookie = [int for _ in range(self.cookieMaxAmount)]
            self.cookieScaleSize = [int for _ in range(self.cookieMaxAmount)]
            self.outputBuffer = []
            self.newAmount = 0
        
        def clearNew():
            for i in range(self.cookieCount-self.newAmount, self.cookieCount):
                trayCanvas.delete(self.cookie[i])
            self.cookieCount = self.cookieCount - self.newAmount
            self.outputBuffer = []
            self.newAmount = 0
            self.secret += 1
            if self.secret == 20:
                secret()

        def secret():
            secretWin = Toplevel()
            secretWin.protocol("WM_DELETE_WINDOW", secretWin.withdraw)
            secretFrame = Frame(secretWin)
            secretFrame.pack()

            Label(secretFrame, text="Make up your mind and place some damn cookies already!").pack()


        def clearLast():
            if self.newAmount > 0 :
                trayCanvas.delete(self.cookie[self.cookieCount-1])
                self.cookieCount -= 1
                del self.outputBuffer[-1] 
                del self.outputBuffer[-1]
                if self.outputBuffer[-1] == 0:
                    del self.outputBuffer[-1]
                del self.outputBuffer[-1]
                if self.outputBuffer != []:
                    if self.outputBuffer[-1] == 0:
                        del self.outputBuffer[-1]
                self.newAmount -= 1

        def sendNew():
            self.secret = 0
            while self.newAmount != 0:
                if self.outputBuffer[0] == 0:
                    if self.outputBuffer[2] == 0:
                        sizeLocation = 4
                    else:
                        sizeLocation = 3
                else:
                    if self.outputBuffer[1] == 0:
                        sizeLocation = 3
                    else:
                        sizeLocation = 2

                self.fill += self.outputBuffer[sizeLocation]
                if (self.fill >= 20):
                     self.refillOption = 1
                     refill()
                     break
                #ser.write(outputBuffer[i])
                for i in range(sizeLocation+1):
                    print(self.outputBuffer[0])
                    del self.outputBuffer[0]

                     
                cookieScaleConstant = 20
                current = self.cookieCount-self.newAmount
                cookiePic = Image.open('Cookie.gif').convert('RGBA').rotate(self.randTurn[current])
                cookiePic = cookiePic.resize((self.cookieScaleSize[current], self.cookieScaleSize[current]))
                self.cookiePic[current] = ImageTk.PhotoImage(cookiePic)
                trayCanvas.itemconfigure(self.cookie[current], image = self.cookiePic[current])

                self.newAmount -= 1


        def refill():
            print 9999990
            refillWin = Toplevel()
            refillFrame = Frame(refillWin)
            refillFrame.pack()

            if self.refillOption == 1:
                 #Send Non-immeadiate refill to Arduino
                 Label(refillFrame, text="You have used all available dough.").pack()
                 Label(refillFrame, text="Some cookies may not have been sent.").pack()
                 Label(refillFrame, text="Cookie Monster will place all the cookies it can.").pack()
                 Label(refillFrame, text="Please wait until the dough empties to press done.").pack()

            Label(refillFrame, text="How far do you want to refill?").pack()
            refillScale = Scale(refillFrame, from_=0, to=20, orient = VERTICAL,length=400)
            refillScale.pack()
        
            def done():
                self.fill = refillScale.get()
                self.refillOption = 0
                refillWin.destroy()
                print 9999991
                print self.fill

            doneButton = Button(refillFrame, text="Done", command=done)
            doneButton.pack(padx=5, pady=5)

            refillWin.protocol("WM_DELETE_WINDOW",done)


        buttonFrame = Frame(trayWin, width=400, height=565)
        buttonFrame.pack()

        sendButton = Button(buttonFrame, text = "Make New Cookies!", command=sendNew)
        sendButton.pack(side=LEFT, padx=5, pady=5)

        clearLastButton = Button(buttonFrame, text = "Undo", command=clearLast)
        clearLastButton.pack(side=LEFT,padx=5, pady=5)

        clearNewButton = Button(buttonFrame, text = "Clear New", command=clearNew)
        clearNewButton.pack(side=LEFT,padx=5, pady=5)

        clearButton = Button(buttonFrame, text = "Clear All", command=clearTray)
        clearButton.pack(side=LEFT,padx=5,pady=5)

        refillButton = Button(buttonFrame, text="Refill", command=refill)
        refillButton.pack(padx=5, pady=5)

        quitButton = Button(buttonFrame, text="Quit", command=trayFrame.quit)
        quitButton.pack(padx=5, pady=5)


    ##########################################################################################
    ##########################################################################################


    def openAutoTray(self):
        trayWin = Toplevel()
        trayWin.protocol("WM_DELETE_WINDOW", exit)
        trayFrame = Frame(trayWin, width=400, height=565)
        trayFrame.pack()
        root.withdraw()

        mainHeaderImg = Image.open('mainHeader.gif')#.convert('RGBA')
        mainHeaderImg = ImageTk.PhotoImage(mainHeaderImg)
        mainHeader = Label(trayFrame, image = mainHeaderImg)
        mainHeader.image = mainHeaderImg
        mainHeader.pack()

        self.refillAmount = 0
        self.outputBuffer = []
        self.sent = 0
        self.cookiePic = [PhotoImage() for _ in range(12)]
        self.cookie = [int for _ in range(12)]
        self.secret = []
           
        trayCanvas = Canvas(trayFrame, width = 400, height = 565, bg = "blue")
        self.sheetPic = PhotoImage(file = "Sheet.gif")
        Sheet = trayCanvas.create_image(0, 0, image = self.sheetPic, anchor = NW)
        trayCanvas.pack()

        def clearTray():
            for i in range(12):
                trayCanvas.delete(self.cookie[i])
            self.cookiePic = [PhotoImage() for _ in range(12)]
            self.cookie = [int for _ in range(12)]
            preset1Button.config(relief=RAISED)
            preset2Button.config(relief=RAISED)
            preset3Button.config(relief=RAISED)
            sendButton.config(relief=RAISED)
            self.sent = 0


        def preset1():
            if self.sent == 0 :
                self.secret.append(1)
                clearTray()
                cookieScaleConstant = 20
                cookieScale = 3
                cookieScaleSize = cookieScale * cookieScaleConstant
                for x in range(3):
                    for y in range(4):
                        currentCookie = 4*(x-1)+y-1
                        xExp = int (115*x-cookieScaleSize*.5+80)
                        yExp = int (150*y-cookieScaleSize*.5+60)
                        cookiePic = Image.open('Cookie.gif').convert('RGBA').rotate(randint(0,360))
                        cookiePic = cookiePic.resize((cookieScaleSize, cookieScaleSize))
                        self.cookiePic[currentCookie] = ImageTk.PhotoImage(cookiePic)
                        self.cookie[currentCookie] = trayCanvas.create_image(xExp,yExp, image = self.cookiePic[currentCookie], anchor = NW)
                        if xExp < 100:
                            self.outputBuffer.append(0)
                        self.outputBuffer.append(xExp)
                        if yExp < 100:
                            self.outputBuffer.append(0)
                        self.outputBuffer.append(yExp)
                        self.outputBuffer.append(cookieScale)
                self.pressed = 1
                preset1Button.config(relief=SUNKEN)        

        def preset2():
            if self.sent == 0:
                self.secret.append(2)
                clearTray()
                cookieScaleConstant = 20
                cookieScale = 4
                cookieScaleSize = cookieScale * cookieScaleConstant
                for x in range(2):
                    for y in range(4):
                        currentCookie = 4*(x-1)+y-1
                        xExp = int (190*x-cookieScaleSize*.5+105)
                        yExp = int (135*y-cookieScaleSize*.5+80)
                        cookiePic = Image.open('Cookie.gif').convert('RGBA').rotate(randint(0,360))
                        cookiePic = cookiePic.resize((cookieScaleSize, cookieScaleSize))
                        self.cookiePic[currentCookie] = ImageTk.PhotoImage(cookiePic)
                        self.cookie[currentCookie] = trayCanvas.create_image(xExp,yExp, image = self.cookiePic[currentCookie], anchor = NW)
                        if xExp < 100:
                            self.outputBuffer.append(0)
                        self.outputBuffer.append(xExp)
                        if yExp < 100:
                            self.outputBuffer.append(0)
                        self.outputBuffer.append(yExp)
                        self.outputBuffer.append(cookieScale)
                preset2Button.config(relief=SUNKEN)

        def preset3():
            if self.sent == 0:
                self.secret.append(3)
                if self.secret == [3,1,2,3,2,1,2,3,2,1,3]:
                    secret()
                clearTray()
                cookieScaleConstant = 20
                cookieScale = 4
                cookieScaleSize = cookieScale * cookieScaleConstant
                for x in range(3):
                    for y in range(3):
                        currentCookie = 4*(x-1)+y-1
                        xExp = int (115*x-cookieScaleSize*.5+90)
                        yExp = int (200*y-cookieScaleSize*.5+80)
                        cookiePic = Image.open('Cookie.gif').convert('RGBA').rotate(randint(0,360))
                        cookiePic = cookiePic.resize((cookieScaleSize, cookieScaleSize))
                        self.cookiePic[currentCookie] = ImageTk.PhotoImage(cookiePic)
                        self.cookie[currentCookie] = trayCanvas.create_image(xExp,yExp, image = self.cookiePic[currentCookie], anchor = NW)
                        if xExp < 100:
                            self.outputBuffer.append(0)
                        self.outputBuffer.append(xExp)
                        if yExp < 100:
                            self.outputBuffer.append(0)
                        self.outputBuffer.append(yExp)
                        self.outputBuffer.append(cookieScale)
                preset3Button.config(relief=SUNKEN)

 
        def send():
            self.secret = []
            if self.outputBuffer != []:
                sendButton.config(relief=SUNKEN)
                self.sent = 1
            for i in range(len(self.outputBuffer)):
                #ser.write(outputBuffer[i])
                print(self.outputBuffer[i])
            self.outputBuffer = []

        def refill():
            print 9999990
            refillWin = Toplevel()
            refillFrame = Frame(refillWin)
            refillFrame.pack()
            Label(refillFrame, text="Please refill the dough to the ?? level.").pack()
            Label(refillFrame, text="Press Done when the dough is refilled.").pack()
        
            def done():
                refillWin.destroy()
                print 9999992


            doneButton = Button(refillFrame, text="Done", command=done)
            doneButton.pack(padx=5, pady=5)

            refillWin.protocol("WM_DELETE_WINDOW",done)

        def secret():
            secretWin = Toplevel()
            secretWin.protocol("WM_DELETE_WINDOW", secretWin.withdraw)
            secretFrame = Frame(secretWin)
            secretFrame.pack()

            Label(secretFrame, text="What?! How did you find this place? LEAVE, AND NEVER RETURN!").pack()


        buttonFrame = Frame(trayWin, width=400, height=565)
        buttonFrame.pack()

        Label(buttonFrame, text="Please make sure the dough is up to the ?? level before making cookies.").pack()

        sendButton = Button(buttonFrame, text = "Make Cookies!", command=send)
        sendButton.pack(side=LEFT, padx=5, pady=5)

        preset1Button = Button(buttonFrame, text = "3x4", command=preset1)
        preset1Button.pack(side=LEFT, padx=5, pady=5)

        preset2Button = Button(buttonFrame, text = "2x4", command=preset2)
        preset2Button.pack(side=LEFT,padx=5, pady=5)

        preset3Button = Button(buttonFrame, text = "3x3", command=preset3)
        preset3Button.pack(side=LEFT,padx=5, pady=5)

        clearButton = Button(buttonFrame, text = "Clear", command=clearTray)
        clearButton.pack(side=LEFT,padx=5,pady=5)

        refillButton = Button(buttonFrame, text="Refill", command=refill)
        refillButton.pack(padx=5, pady=5)

        quitButton = Button(buttonFrame, text="Quit", command=trayFrame.quit)
        quitButton.pack(padx=5, pady=5)

        okayWin = Toplevel()
        okayWin.protocol("WM_DELETE_WINDOW", okayWin.withdraw)
        okayFrame = Frame(okayWin)
        okayFrame.pack()

        Label(okayFrame, text="When using Automatic Mode, please make sure that").pack()
        Label(okayFrame, text="the dough is filled up to the ?? level before making.").pack()
        okayButton = Button(okayFrame, text="Okay", command=okayWin.withdraw)
        okayButton.pack(padx=5, pady=5)    
        okayWin.lift()
        trayWin.lower(belowThis=okayWin)

    
    def exit():
        root.update()
        root.destroy()


    
root = Tk()

app = App(root)

root.mainloop()