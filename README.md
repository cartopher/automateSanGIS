# Automate SanGIS Downloads using Python

## Workflow
The instructions below describe how we can use Python to automate and streamline repetitive downloading tasks. In this demonstration, we use the "twill" package to access and navigate the SanGIS/SANDAG GIS Data Warehouse website to download and extract multiple ZIP files to specific folder directories on our operating system.

***twill Package***  
The Python package "twill," based on requests and lxml packages, is a simplified scripting language developed for programmatic or automated website navigation through a command-line interface. You may use twill to navigate websites that employ forms, cookies, and other common Web features. Moreover, twill provides excellent support for both MySQL and PostgreSQL databases management tasks.

For more about the 'twill' package, see:  
twill Project Description (https://pypi.org/project/twill/)  
twill Overview (https://twill-tools.github.io/twill/overview.html)  
twill’s Python API (https://twill-tools.github.io/twill/python-api.html#python-api)  

## Installation

*__Note__: If you prefer to use an existing virtual environment, all you need to do is run the ‘pip install twill’ command.*

The list of commands used:
````
conda create -n dlgisdata python=3
conda activate sangisdownload
pip install twill
conda list
````
### Instructions  
#### Create a Virtual Environment using Anaconda

Open the Anaconda Command Prompt and input the follow line of code to create a new virtual environment: 
````
conda create --n sangisdownload python=3
````
Input the following command to activate the environment:
````
conda activate sangisdownload
````
#### Installing twill  
Install the 'twill' package using pip by inputting the following command:
````
pip install twill
````
Return a list of packages and ensure the package twill was installed:
````
conda list
````
## Package Overview
The Python_Package contains:  
````
sangis_download.py
- The main module containing the entire executable script,

sangis_credentials.py
- For security purposes, this module contains statements that store login credentials to string variables,
- Importing this module into the main module allows these variables to be used during the login process,
- In this way, we prevent the visibilitly of sensitive information in the main module,

__init__.py
- Used to mark directories on a disk as Python package directories,  

'output' directory
- The parent directory that contains multiple subdirectories where ZIP files are downloaded and extracted,  

'Parcels' and 'Roads' subdirectories
- Child folders of the output folder and the parent folders of two subdirectories:
       1. 'YYYY_MM' directory ("date-stamped", ex. 2022_09)
          - The working directory where ZIP files are downloaded and unextracted  
       2. 'Current' directory 
          - The working directory where ZIP files are downloaded and extracted  
````  

*__Note__: The time-stamped folder is created and named after the year and month in which the main module is executed (ex. 2022_09).  
If the main module is executed more than once a month, all downloaded files with the same name in both the __'YYYY_MM'__ and __'Current'__ folder directories will be overwritten.*  

## Getting Set Up  

1. Download and extract this entire repository to your prefered working directory.
2. Using your IDE of choice, open the 'Python_Package' as a new project.
3. Open the __'sangis_credentials.py'__ Python file and input your username and password used to log in to the SanGIS/SANDAG GIS Data Warehouse website.
````
# Store credentials into string variables,
username = 'INPUT EMAIL'
password = 'INPUT PASSWORD'
````
4. Open the __'sangis_download.py'__, module and refer to the documentation below to help guide your understanding of the main module's logic.  

### Important Imports
*__Notice__: the bottom import is called 'sangis_credentials'; this is the name of the Python file that contains our login credentials for accessing the SanGIS/SANDAG GIS Data Warehouse website. Importing the module allows us to access and use those variables in our main module. We carry out this process in the loginCredentials() Class Method below.*
````
# Import packages,
import os
import time
import zipfile
from twill.commands import *
from twill import browser

# Import the sangis_credentials.py module,
import sangis_credentials
````
### Class Object & Constructor Method  
Create a SanGISDownload Class Object & Encapsulate all Methods and Variables.
````
class SanGISDownload:
    def __init__(self, directory, filename):
        """SanGISDownload  Class Constructor,
             :param self: pass 'self' to access variables coming from the constructor,
             :param directory: output file path (string),
             :param filename: output filename(s) (string), """
        
        # Initialize Class Variables,
        self.directory = directory
        self.filename = filename
        self.current_month_folder = None
````

### buildDirectory() Method  
Now that we have Created our Class and Constructor, we are Free to Access and Modify our Objects Attributes in our Methods.  
For our first Class Method, we will Build our Directories to Ensure all ZIP files are Downloaded and Organized into Specific Directories.   
````
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

````
### loginCreds() Method  
Class Method for Accessing the SanGIS/SANDAG GIS Data Warehouse Website.
```` 
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
````     
### downloadZippedFile() Method  
Class Method for Downloading ZIP File(s).
````
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
````            
### extractZippedFile() Method  
Class Method for extracting ZIP file(s).
````            
    def extractZipFile(self):
        """Creates a new folder directory specifically for extraction,
           Extracts ZIP file contents to new directory """
        
        # Pass filename with path for extraction,
        # Open file using read permission that we want to extract it,
        myzip = zipfile.ZipFile(
            self.current_month_folder + "\\" + self.filename, 'r')

        # Extract ZIP file contents to a new folder,
        myzip.extractall(self.directory + "Current")

        # Close the ZIP file,
        myzip.close()

        # Display the filename,
        print(self.filename)
````        
### processSanGIS() Method  
Here, we Build a Class Method to Handle Exceptions (errors) that Occur During our Runtime (execution) of the Program.  
We Handle these Expections Gracefully using Try and Exception Statements. For Example, if the Try Block Raises an Exception, the Except Block will Return the Exception that may be Caused by the Try Block.  
````           
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
````            
### main() Method  
We define the main method and use it to run each line serially from the top of the entire module,
````
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
````
