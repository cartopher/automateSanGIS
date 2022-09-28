#  import all of the commands in commands.py and use them directly from Python:
from twill.commands import *
# to talk to the web browser directly, import the browser object:
from twill import browser
# import operating system and time packages to create a time-stamped folder
import os
import time
# import the zipfile package to to extract the ZIP file contents
import zipfile

# import the sangis_credentials script to login to the SanGIS website
import sangis_credentials

# assign a directory path
# adjust the front end of the path to your preference
# ensure '\\sangis_package\\output\\Parcels\\'  is the end-point of the directory
directoryPath = 'C:\\Users\\cchar\\PycharmProjects\\pythonProject\\sangis_package\\output\\Parcels\\'

# store the current year and date into a variable
currentMonth = time.strftime("%Y_%m")

# create a time-stamped folder and in the directory location
if os.path.isdir(directoryPath + currentMonth):
    print("Directory already exists")
else:
    print("Creating directory for you")
    os.mkdir(directoryPath + currentMonth)

# change the working directory to the time-stamped folder
os.chdir(directoryPath + currentMonth)

# assign a the new directory to the time-stamped folder
directory = os.getcwd()

# talk to the web browser directly
go('https://rdw.sandag.org/Account/Login')
showforms()

# input login credentials
fv("1", "ctl00$MainContent$Email", sangis_credentials.username)
fv("1", "ctl00$MainContent$Password", sangis_credentials.password)
submit('0')

# list of the all the ZIP files needed for download from Data Warehouse
"""
Assessor_Book.zip
LANDBASE_BOUNDARIES.zip
Lots.zip
Parcels.zip
PARCELS_EAST.zip
Parcels_North.zip
PARCELS_SOUTH.zip
"""

# navigate to the parcels download page and initiate the download process
go("gisdtview.aspx?dir=Parcel")
go("GetFSFile.aspx?dir=Parcel&Name=PARCELS_SOUTH.zip.zip")

# open file for writing in binary format
# overwrite the file if it exists
# if the file does not exist, create new file for writing
with open('PARCELS_SOUTH.zip', "wb") as bf:
    bf.write(browser.dump)

# navigate to the ZIP file location
myzip = zipfile.ZipFile(
    'C:/Users/cchar/PycharmProjects/pythonProject/sangis_package/output/Parcels/2022_08/PARCELS_SOUTH.zip', 'r')

# extract ZIP file into a new folder directory, called 'Current', inside the 'Parcels" folder, called ' by specifying the folder name at the path end-point
myzip.extractall('C:/Users/cchar/PycharmProjects/pythonProject/sangis_package/output/Parcels/Current')

# close the ZIP file
myzip.close()

def main():
    pass

if __name__ == '__main__':
    main()
