import sys
import datetime
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QPushButton
from pytz import timezone

def window():
    app = QApplication(sys.argv)
    win = QWidget()
    grid = QGridLayout()

    for i in range(0, 3):
        for j in range(0, 4):
            grid.addWidget(QPushButton(str(i)+str(j)),i,j)
    
    win.setLayout(grid)
    win.setWindowTitle("Hello World!")
    win.show()
    #only exits program when app's exit is pressed
    sys.exit(app.exec_())

#function to configure local times
def time(tzTimes):
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

if __name__ == '__main__':
    window()