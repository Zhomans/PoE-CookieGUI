#Author: Zachary Homans
#Principles of Engineering, Fall 2012
#Franklin W. Olin College of Engineering
#GUI for cookie dough placing machine, Cookie Monster
#This is a "No Arduino" version. The GUI will print out to the command line as if it is printing to the Serial Monitor (where the Arduino would normally pick it up).

#Setup modules
#import serial, 
import math
from datetime import datetime
import time
from Tkinter import *
import tkFont
import Image
import ImageTk
from random import randint

##Connect to Serial Monitor
# try:
# 	ser=serial.Serial('COM3', 9600)
# except:
# 	print "Failed to connect to COM3"

class App:

    def __init__(self, master):

        #Create initial frame
        frame = Frame(master, width=200, height=100)
        frame.pack()

        #Create Header Picture for initial frame
        startHeaderImg = Image.open('StartHeader.gif')
        startHeaderImg = ImageTk.PhotoImage(startHeaderImg)
        startHeader = Label(frame, image = startHeaderImg, width = 115)
        startHeader.image = startHeaderImg
        startHeader.pack()

        #Create Scale for initial piston placement
        Label(frame, text="Where is the piston?").pack()
        fullScale = Scale(frame, from_=0, to=20, orient = VERTICAL,length=400)
        fullScale.pack()

        #Manual Mode
        def manual():
            self.fill = fullScale.get()
            if self.fill < 10:
                print 0         #Arduino needs two digits to represent a piston location. If it's less than 10, there needs to be a leading 0.
            print(self.fill)
            self.openManTray()

        #Automatic Mode
        def automatic():
            self.fill = fullScale.get()
            if self.fill < 10:
                print(0)
            print(self.fill)
            self.openAutoTray()

        #Manual and Automatic Buttons
        self.manualButton = Button(frame, text="Manual", command=manual)
        self.manualButton.pack(side=LEFT)

        self.automaticButton = Button(frame, text="Automatic", command=automatic)
        self.automaticButton.pack(side=LEFT)



    #Manual Mode Main Function
    def openManTray(self):

        #Creates Manual Window
    	trayWin = Toplevel()
        trayWin.protocol("WM_DELETE_WINDOW", exit)
    	trayFrame = Frame(trayWin, width=400, height=565)
    	trayFrame.pack()
        root.withdraw()

        #Creates Manual Window Header Picture
        mainHeaderImg = Image.open('mainHeader.gif')
        mainHeaderImg = ImageTk.PhotoImage(mainHeaderImg)
        mainHeader = Label(trayFrame, image = mainHeaderImg)
        mainHeader.image = mainHeaderImg
        mainHeader.pack()

        #Setup various trackers
        self.newAmount = 0  #Tracks the amount of cookies placed since last "Send".
        self.cookieCount = 0    #Tracks the total amount of cookies on the sheet.
        self.cookieMaxAmount = 100  #Total amount of cookies allowed on the sheet. For author convinence.
        self.cookiePic = [PhotoImage() for _ in range(self.cookieMaxAmount)]    #Stores the different pictures used for each cookie.
        self.cookie = [int for _ in range(self.cookieMaxAmount)]       #Stores the cookie objects, which contains the pictures and location.
        self.cookieScaleSize = [int for _ in range(self.cookieMaxAmount)]   #Stores the size of each cookie object. Index-to-index correlation.
        self.randTurn = [int for _ in range(self.cookieMaxAmount)]  #Stores of the rotation of each cookie object. Index-to-index correlation.
        self.trayMargin = 50    #Margin of the tray where you can't place cookies.
        self.outputBuffer = []  #Stores cookies that haven't been sent in case dough runs out.
        self.refillOption = 0   #Automatic refill or manual refill.
        self.secret = 0 #For fun.

        #Occurs when mouse click on tray.
        def onObjectClick(event):
            if (event.x > self.trayMargin and event.x<(400 - self.trayMargin)) and (event.y > self.trayMargin and event.y < (565 - self.trayMargin)):   #If the clickable locations are clicked.
                if self.cookieCount < self.cookieMaxAmount:
                    self.randTurn[self.cookieCount] = randint(0,360)    #Turns cookies.
                    cookieScaleConstant = 20    #Changable cookie size constant.
                    self.cookieScaleSize[self.cookieCount] = cookieScale.get()*cookieScaleConstant  #Changes cookie size based on constant and current scale value.
                    cookiePic = Image.open('RedCookie.gif').convert('RGBA').rotate(self.randTurn[self.cookieCount]) #Opens cookie picture in correct format.
                    cookiePic = cookiePic.resize((self.cookieScaleSize[self.cookieCount], self.cookieScaleSize[self.cookieCount]))  #Resizes cookie picture.
                    self.cookiePic[self.cookieCount] = ImageTk.PhotoImage(cookiePic)
                    self.cookie[self.cookieCount] = trayCanvas.create_image(event.x-self.cookieScaleSize[self.cookieCount]*.5,event.y-self.cookieScaleSize[self.cookieCount]*.5, image = self.cookiePic[self.cookieCount], anchor = NW) #Places cookie on sheet.
                    self.cookieCount += 1   #Increment counter.

                    #Ensures that 6 digits are used to represent location (includes leading zeroes) and one digit is used to represent size. Added to output buffer.
                    if event.x < 100:
                        self.outputBuffer.append(0)
                    self.outputBuffer.append(event.x)
                    if event.y < 100:
                        self.outputBuffer.append(0)
                    self.outputBuffer.append(event.y)
                    self.outputBuffer.append(cookieScale.get())

                    self.newAmount += 1 #Increment counter.
                    #print(self.outputBuffer)   #Enable if you wish to see output buffer after every cookie.

        #Setup tray canvas.
        trayCanvas = Canvas(trayFrame, width = 400, height = 565, bg = "blue")
        self.sheetPic = PhotoImage(file = "Sheet.gif")
        Sheet = trayCanvas.create_image(0, 0, image = self.sheetPic, anchor = NW)
        trayCanvas.tag_bind(Sheet,'<Button-1>', onObjectClick)
        trayCanvas.pack()

        #Add text.
        Label(trayFrame, text="Size:").pack()

        #Add cookie size scale for changing cookie size.
        cookieScale = Scale(trayFrame, from_=1, to=9, orient = HORIZONTAL,length=300)
        cookieScale.set(3)
        cookieScale.pack()

        #Clear all cookies on the sheet. Essentially resets all variables.
        def clearTray():
            for i in range(self.cookieMaxAmount):
                trayCanvas.delete(self.cookie[i])
            self.cookieCount = 0
            self.cookiePic = [PhotoImage() for _ in range(self.cookieMaxAmount)]
            self.cookie = [int for _ in range(self.cookieMaxAmount)]
            self.cookieScaleSize = [int for _ in range(self.cookieMaxAmount)]
            self.outputBuffer = []
            self.newAmount = 0
        
        #Clear only new cookies. Essentially empties output buffer.
        def clearNew():
            for i in range(self.cookieCount-self.newAmount, self.cookieCount):
                trayCanvas.delete(self.cookie[i])
            self.cookieCount = self.cookieCount - self.newAmount
            self.outputBuffer = []
            self.newAmount = 0
            self.secret += 1
            if self.secret == 20:
                secret()

        #For fun.
        def secret():
            secretWin = Toplevel()
            secretWin.protocol("WM_DELETE_WINDOW", secretWin.withdraw)
            secretFrame = Frame(secretWin)
            secretFrame.pack()

            Label(secretFrame, text="Make up your mind and place some damn cookies already!").pack()

        #Clears the in the output buffer. Complexity is required to ensure that all 7 digits of a cookie request are deleted from the buffer.
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

        #Send all new cookies. If a cookie will cause the dough to empty, it and all proceeding cookies are not sent and refill function is called.
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
                if (self.fill > 20):
                     self.refillOption = 1
                     refill()
                     break
                for i in range(sizeLocation+1):
                    print(self.outputBuffer[0])
                    del self.outputBuffer[0]

                #Changes all cookies from their red picture to a normal colored cookie to indicate that the cookie has been sent.
                cookieScaleConstant = 20
                current = self.cookieCount-self.newAmount
                cookiePic = Image.open('Cookie.gif').convert('RGBA').rotate(self.randTurn[current])
                cookiePic = cookiePic.resize((self.cookieScaleSize[current], self.cookieScaleSize[current]))
                self.cookiePic[current] = ImageTk.PhotoImage(cookiePic)
                trayCanvas.itemconfigure(self.cookie[current], image = self.cookiePic[current])

                self.newAmount -= 1

        #Refill command. Send special sequence to indicate first part of refill. Then send a digit based on refill type.
        def refill():
            print(9999990)
            refillWin = Toplevel()
            refillFrame = Frame(refillWin)
            refillFrame.pack()

            if self.refillOption == 1:
                #Let's user know that not all cookies may have been sent.
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
                print(1)
                print(self.fill)

            doneButton = Button(refillFrame, text="Done", command=done)
            doneButton.pack(padx=5, pady=5)

            refillWin.protocol("WM_DELETE_WINDOW",done)

        #Button Setup
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

    #Automatic Mode Main Function
    def openAutoTray(self):

        #Automatic Mode Main Window
        trayWin = Toplevel()
        trayWin.protocol("WM_DELETE_WINDOW", exit)
        trayFrame = Frame(trayWin, width=400, height=565)
        trayFrame.pack()
        root.withdraw()

        #Main Window Header Image
        mainHeaderImg = Image.open('mainHeader.gif')#.convert('RGBA')
        mainHeaderImg = ImageTk.PhotoImage(mainHeaderImg)
        mainHeader = Label(trayFrame, image = mainHeaderImg)
        mainHeader.image = mainHeaderImg
        mainHeader.pack()

        #Setup various trackers.
        self.refillAmount = 0
        self.outputBuffer = []
        self.sent = 0
        self.cookiePic = [PhotoImage() for _ in range(12)]
        self.cookie = [int for _ in range(12)]
        self.secret = []
           
        #Tray Canvas.
        trayCanvas = Canvas(trayFrame, width = 400, height = 565, bg = "blue")
        self.sheetPic = PhotoImage(file = "Sheet.gif")
        Sheet = trayCanvas.create_image(0, 0, image = self.sheetPic, anchor = NW)
        trayCanvas.pack()

        #Clear Tray.
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

        #First preset. 3x4. Places cookies in a similar way as manual mode.
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

        #Preset 2. 2x4.
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

        #Preset 3. 3x3.
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

        #Send cookies.
        def send():
            self.secret = []
            if self.outputBuffer != []:
                sendButton.config(relief=SUNKEN)
                self.sent = 1
            for i in range(len(self.outputBuffer)):
                print(self.outputBuffer[i])
            self.outputBuffer = []

        #Refill Cookies.
        def refill():
            print 9999990
            refillWin = Toplevel()
            refillFrame = Frame(refillWin)
            refillFrame.pack()
            Label(refillFrame, text="Please refill the dough to the ?? level.").pack()
            Label(refillFrame, text="Press Done when the dough is refilled.").pack()
        
            def done():
                refillWin.destroy()
                print(2)

            doneButton = Button(refillFrame, text="Done", command=done)
            doneButton.pack(padx=5, pady=5)

            refillWin.protocol("WM_DELETE_WINDOW",done)

        #For fun.
        def secret():
            secretWin = Toplevel()
            secretWin.protocol("WM_DELETE_WINDOW", secretWin.withdraw)
            secretFrame = Frame(secretWin)
            secretFrame.pack()

            Label(secretFrame, text="What?! How did you find this place? LEAVE, AND NEVER RETURN!").pack()


        #Button Setup
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


#Used to start GUI
root = Tk()

app = App(root)

root.mainloop()