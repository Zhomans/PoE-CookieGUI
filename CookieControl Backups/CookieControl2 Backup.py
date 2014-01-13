#Setup
import serial
import math
from datetime import datetime
import time
from Tkinter import *
import tkFont
import Image #This is the PIL Image library
import ImageTk

#Connect to Serial Monitor
#try:
#	ser=serial.Serial('COM6', 9600)
#except:
#	print "Failed to connect to COM6"

#Prompts user for mode.
# modeInput = raw_input("\"Manual\" or \"Automatic\"?")
# if modeInput == "Manual":
# 	manual = 1
# 	#ser.write(1)
# elif modeInput == "Automatic":
# 	manual = 0
# 	#ser.write(0)
# else:
# 	print("Incorrect Manual/Automatic Input")

class App:

    def __init__(self, master):

        frame = Frame(master, width=200, height=100)
        frame.pack()

        self.manualButton = Button(frame, text="Manual", command=self.manual)
        self.manualButton.pack(side=LEFT)

        self.automaticButton = Button(frame, text="Automatic", command=self.automatic)
        self.automaticButton.pack(side=LEFT)

    def manual(self):
        manual = 1
        print manual #Replace with sending data to Serial
        self.openTray()

    def automatic(self):
    	manual = 0
    	print manual #Replace with sending data to Serial
    	self.openTray()

    def openTray(self):
    	trayWin = Toplevel()
    	trayFrame = Frame(trayWin, width=400, height=565)
    	trayFrame.pack()
        root.withdraw()
        def onObjectClick(event):
       		cookiePic = Image.open('Cookie.gif')
        	cookiePic = cookiePic.resize((cookieScale.get()*20, cookieScale.get()*20), Image.ANTIALIAS)
        	self.cookiePic = ImageTk.PhotoImage(cookiePic)
    		Cookie = trayCanvas.create_image(event.x,event.y, image = self.cookiePic, anchor = NW)
    		#Send event.x and event.y data to Serial
        trayCanvas = Canvas(trayFrame, width = 400, height = 565, bg = "blue")
        self.sheetPic = PhotoImage(file = "Sheet.gif")#'C:\Users\zhomans\Documents\PoE\Project\Sheet.jpg')
        Sheet = trayCanvas.create_image(0, 0, image = self.sheetPic, anchor = NW)
        trayCanvas.tag_bind(Sheet,'<Button-1>', onObjectClick)
        trayCanvas.pack()

        cookieScale = Scale(trayFrame, from_=1, to=10, orient = HORIZONTAL)
        cookieScale.pack()

        quitButton = Button(trayFrame, text="QUIT", command=trayFrame.quit)
        quitButton.pack()






root = Tk()

app = App(root)

root.mainloop()

#Data setup.
#automaticCounter = 0
#junk=ser.readline() #First piece of data in the Serial Monitor is 1 or 0 this script sends. 
					#This makes sure that it is not taken in as data.

# while True:
# 	if manual: #Manual Mode
		
# 		#Make GUI for this.
# 		#nextLocation = raw_input("Where would you like to place the next cookie?")
# 		#try:
# 		#	nextLocation = float(nextLocation)
# 		#except TypeError:
# 		#	print "Incorrect Location Input Type"
# 		#nextdish -= 1
# 		#if ((nextdish > 3) & (nextdish < -1)):
# 		#	print "Value Out of Range"


# 		if (nextdish!=currentdish):
# 			timeBetweenData += (abs(nextdish-currentdish)-1)*.7+.2
# 		ser.write(nextdish)
# 		if nextdish == -1:
# 			break #Break out if user input is 0.
# 		time.sleep(timeBetweenData)
# 		timeData.append(datetime.now())
# 		dishData.append(nextdish + 1)
# 		rawsensorData = ser.readline()
# 		resistor = 10000*5/(rawsensorData*5/1023)-10000	#Data Scaling
# 		lum = math.exp((80-math.log(rawsensorData))/.74)
# 		sensorData.append(lum)
# 		currentdish = nextdish
# 		timeBetweenData = 5.25

# 	else: #Automatic Mode
# 		time.sleep(timeBetweenData)
# 		timeData.append(datetime.now())
# 		dishData.append(automaticCounter % 4 + 1)
# 		#rawsensorData = ser.readline()
# 		#resistor = 10000*5/(rawsensorData*5/1023)-10000
# 		#lum = math.exp((80-math.log(rawsensorData))/.74)
# 		sensorData.append(ser.readline())
		
# 		automaticCounter += 1
# 		#Prompts for user input every 4 moves.
# 		if automaticCounter >= (4): #Make sure that this number is consistent with Arduino
# 			goOn = raw_input("Do you wish to continue collecting data (\"Yes\"/\"No\")?:")
# 			if goOn == "Yes":
# 				automaticCounter = 0
# 				timeBetweenData = 5.5
# 				ser.write("G") #Sends a "G" if told to continue.
# 			elif goOn == "No":
# 				break 	#Break otherwise.
# 			else:
# 				print "Unknown Request. Breaking."
# 				break

