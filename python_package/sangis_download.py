#  Import packages,
import os
import time
import zipfile
from twill.commands import *
from twill import browser

# Import the sangis_credentials.py module,
import sangis_credentials


# Create a SanGISDownload Class Object & encapsulate all methods and variables,
class SanGISDownload:

    # Create SanGISDownload Class Constructor, with two arguments, and initialize class variables,
    def __init__(self, directory, filename):
        """SanGISDownload  Class Constructor,
             :param self: pass 'self' to access variables coming from the constructor,
             :param directory: output file path (string),
             :param filename: output filename(s) (string), """
        # Initialize Class Variables,
        self.directory = directory
        self.filename = filename
        self.current_month_folder = None

    # Class Method for creating and structuring output subdirectories,
    def buildDirectory(self):
        """Creates "date-stamped" subdirectories,
             Changes the current working directory to output file path,
            :current_month_folder: a Class Variable containing the file path to the date-stamped subdirectories"""
        # Modify attribute properties,
        directoryPath = self.directory

        # Store the current year and month to a variable,
        currentMonth = time.strftime("%Y_%m")

        # Create a new directory (folder) if it does not already exist,
        if os.path.isdir(directoryPath + currentMonth):
            print("Directory already exists")
        else:
            print("Creating directory for you")
            os.mkdir(directoryPath + currentMonth)

        # Change the current working directory to the date-stamped subdirectory,
        os.chdir(directoryPath + currentMonth)

        # Assign the current working directory,
        directory = os.getcwd()

        # Reassign the current working directory to a Class Variable,
        self.current_month_folder = directory

        # Print the new current working directory,
        print(directory)

    # Class Method for accessing the SanGIS/SANDAG GIS Data Warehouse website,
    def loginCredentials(self):
        """Browses to data source website,
             Call the 'sangis_credentials' module to input login credentials,"""
        # Talk to the web browser directly,
        go('https://rdw.sandag.org/Account/Login')
        showforms()

        # Input login credentials,
        fv("1", "ctl00$MainContent$Email", sangis_credentials.username)
        fv("1", "ctl00$MainContent$Password", sangis_credentials.password)
        submit('0')

    # Class Method downloading ZIP file(s),
    def downloadZipFile(self):
        """Browsing while logged in,
              Initiatize the download process,"""
        # Navigate to the parcels download page
        go("gisdtview.aspx?dir=Parcel")
        go("GetFSFile.aspx?dir=Parcel&Name=" + self.filename)

        # Create a file object,
        # Open file for writing in binary format,
        # Overwrite the file if it exists,
        # If the file does not exist, create new file for writing,
        with open(self.filename, "wb") as bf:
            bf.write(browser.dump)

# Class Method to extract zip file(s),
    def extractZipFile(self):
        """Creates a new folder directory specifically for extraction,
              Extracts ZIP file contents to new directory """
        # Pass filename with path to extract,
        # Open file using read permission that we want to extract it,
        myzip = zipfile.ZipFile(
            self.current_month_folder + "\\" + self.filename, 'r')

        # Extract ZIP file contents to a new folder,
        myzip.extractall(self.directory + "Current")

        # Close the ZIP file,
        myzip.close()

        # Display the filename,
        print(self.filename)

# When an error occurs, this Class Method catches and handles the exception,
    def processSanGIS(self):
        """ try block: contains the code that may cause the exception.
              except block: returns the exception that may be caused by the try block."""
        try:
            self.buildDirectory()
        except Exception as e:
            print("Exception when trying to change directory.")
            print(print(str(e)))
            return

        try:
            self.loginCredentials()
        except Exception as e:
            print("Exception when trying to go to the specified URL.")
            print(print(str(e)))
            return

        try:
            self.downloadZipFile()
        except Exception as e:
            print("Exception when trying to download zipped file.")
            print(print(str(e)))
            return

        try:
            self.extractZipFile()
        except Exception as e:
            print("Exception when trying to extract zipped file.")
            print(print(str(e)))
            return


# Define the main method so it runs each line serially from the top of the entire module,
def main():

    # Get the current working directory,
    getcurrent = os.getcwd()
    print(getcurrent)

    # Join absolute and relative paths,
    directory1 = os.path.join(os.path.sep, getcurrent, 'output', 'Roads', '')
    # Execute the first download,
    download1 = SanGISDownload(directory1, "Assessor_Book.zip")
    # Process each Class Method for exception handling,
    download1.processSanGIS()

    # Display the first directory,
    print(directory1)
    print('Download 1: Complete')

    # Join absolute and relative paths,
    directory2 = os.path.join(os.path.sep, getcurrent, 'output', 'Parcels', '')
    # Execute the first download,
    download2 = SanGISDownload(directory2, "PARCELS_EAST.zip")
    # Process each Class Method for exception handling,
    download2.processSanGIS()

    # Display the second directory,
    print(directory2)
    print("Download 2: Complete")

    if __name__ == '__main__':
        main()
    print("Program Complete!")
