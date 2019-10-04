from tkinter import *
from tkinter.ttk import *
import datetime
from time import strftime
from tkinter import Label
from pytz import timezone
from PIL import Image, ImageOps, ImageTk

font = 'calibri'
timeColor = 'dark red'
imgWidth = 100
imgHeight = 50

#function to initialize tkinter window
def initWindow():
    root = Tk()
    root.configure(background='black')
    root.title('DSN Clock')

    #add weight to each cell in the grid so they can resize
    for row in range(4):
        Grid.rowconfigure(root, row, weight=1)

    for col in range(3):
        Grid.columnconfigure(root, col, weight=1)
    
    return root

#function to configure local times
def time():
    # UTC / GMT Formatting
    tzUTC = datetime.datetime.utcnow().strftime('%H:%M:%S')
    # PST / GDSCC Local Formatting
    tzPST = datetime.datetime.now().strftime('%H:%M:%S')
    # MDSCC Local Time / Converting and Formatting
    source_date = datetime.datetime.now()
    source_time_zone = timezone('US/Pacific')
    source_date_with_timezone = source_time_zone.localize(source_date)

    mdscc_target_time_zone = timezone('Europe/Madrid')
    mdscc_target_date_with_timezone = source_date_with_timezone.astimezone(mdscc_target_time_zone)
    tzmdscc = mdscc_target_date_with_timezone.strftime('%H:%M:%S')

    #CDSCC Local Time
    cdscc_target_time_zone = timezone('Australia/Canberra')
    cdscc_target_date_with_timezone = source_date_with_timezone.astimezone(cdscc_target_time_zone)
    tzcdscc = cdscc_target_date_with_timezone.strftime('%H:%M:%S')
    # Taking Time Zone Data and Adding to Widget Grids
    tzTimes[0].config(text=tzUTC)
    tzTimes[1].config(text=tzPST)
    tzTimes[2].config(text=tzmdscc)
    tzTimes[3].config(text=tzcdscc)
    tzTimes[1].after(1000, time)


if __name__ == "__main__":
    root = initWindow()
    #images representing each timezone
    photos = [Image.open('abstractworld.gif'), Image.open('amerFlag.png'), Image.open('spainFlag.png'), Image.open('ausFlag.png')]
    #timezone labels
    tzLabels = ["UTC Time:", "GDSCC Local:", "MDSCC Local:", "CDSCC Local:"]
    #initialize local clocks array
    tzTimes = []
    
    for i in range(len(photos)):
        #place image on grid
        image = photos[i].resize((imgWidth, imgHeight), Image.ANTIALIAS)
        photoImg =  ImageTk.PhotoImage(image)
        photoLabel = Label(root, image=photoImg, background='black')
        photoLabel.image = photoImg #create a reference of image to avoid garbage collection
        photoLabel.config(borderwidth=0)
        photoLabel.grid(row=i, column=0, padx=10, sticky=N+S+E+W)

        #place label on grid
        tzLabel = Label(root, font=(font, imgHeight, 'bold'), background='black', foreground='white', text=tzLabels[i])
        tzLabel.grid(row=i, column=1, sticky=N+S+E+W)

        #place digital clock label on grid and add to tzTimes
        tzTime = Label(root, font=(font, imgHeight, 'bold'), background='black', foreground=timeColor)
        tzTime.grid(row=i, column=2, sticky=N+S+E+W, padx=10)
        tzTimes.append(tzTime)
    
    time()
    root.mainloop()