#  import all packages
import os
import time
import zipfile
from twill.commands import *
from twill import browser

# import the sangis_credentials script to login to the SanGIS website
import sangis_credentials


# create a sangis_parcels Class Object
class sangis_parcels():
    """encapsulate all methods and variables into a Class object"""

    # assign class variables
    directory = None
    filename = None
    current_month_folder = None

    # create constructor and set parameters
    def __init__(self, directory, filename):
        """constructor creates class variables and methods
        :param self: pass 'self' to access variables coming from the constructor
        :param directory: a file path for all output files
        :param filename: the name of output files
        :param current_month_folder: a file path to the time-stamped folder
        """

        # initialize class variables
        self.directory = directory
        self.filename = filename

    def changeDirectory(self):
        """Description:"""

        directoryPath = self.directory

        # store the current year and date into a variable
        currentMonth = time.strftime("%Y_%m")

        # create a time-stamped folder and in the directory location
        if os.path.isdir(directoryPath + currentMonth):
            print("Directory already exists")
        else:
            print("Creating directory for you")
            os.mkdir(directoryPath + currentMonth)

        # change the current working directory to the time-stamped folder
        os.chdir(directoryPath + currentMonth)

        # assign the current working directory to the time-stamped folder
        directory = os.getcwd()

        self.current_month_folder = directory

        print(directory)

    def login(self):
        """Description:"""

        # talk to the web browser directly
        go('https://rdw.sandag.org/Account/Login')
        showforms()

        # input login credentials
        fv("1", "ctl00$MainContent$Email", sangis_credentials.username)
        fv("1", "ctl00$MainContent$Password", sangis_credentials.password)
        submit('0')

    def downloadZippedFile(self):
        """Description:"""

        # navigate to the parcels download page and initiate the download process
        go("gisdtview.aspx?dir=Parcel")
        go("GetFSFile.aspx?dir=Parcel&Name=" + self.filename)

        # open file for writing in binary format
        # overwrite the file if it exists
        # if the file does not exist, create new file for writing
        with open(self.filename, "wb") as bf:
            bf.write(browser.dump)

    def extractZippedFile(self):
        """Description:"""

        myzip = zipfile.ZipFile(
            self.current_month_folder + "\\" + self.filename, 'r')

        myzip.extractall(self.directory + "Current")

        # close the ZIP file
        myzip.close()

    def process_sangis(self):
        """Description:"""

        # call each method within each try, catch and exception
        try:
            self.changeDirectory()
        except Exception as e:
            print("Exception when trying to change directory")
            print(print(str(e)))
            return

        try:
            self.login()
        except Exception as e:
            print("Exception when trying to go to the specified URL")
            print(print(str(e)))
            return

        try:
            self.downloadZippedFile()
        except Exception as e:
            print("Exception when trying to download zipped file")
            print(print(str(e)))
            return

        try:
            self.extractZippedFile()
        except Exception as e:
            print("Exception when trying to extract zipped file")
            print(print(str(e)))
            return


# define main method
def main():
    """Description:"""
    directory1 = 'C:\\Users\\cchar\\OneDrive\\Desktop\\download\\package\\output\\Roads\\'
    download1 = sangis_parcels(directory1, "Assessor_Book.zip")
    download1.process_sangis()

    directory2 = 'C:\\Users\\cchar\\OneDrive\\Desktop\\download\\package\\output\\Roads\\'
    download2 = sangis_parcels(directory2, "PARCELS_EAST.zip")
    download2.process_sangis()


if __name__ == '__main__':
    main()
