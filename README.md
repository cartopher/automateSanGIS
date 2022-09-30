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

__Note__: *If you prefer to use an existing virtual environment, all you need to do is run the ‘pip install twill’ command.*

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
- the main module containing the entire executable script,

sangis_credentials.py
- for security purposes, this module contains statements that store login credentials to string variables,
- importing this module into the main module allows these variables to be used during the login process,
- in this way, we prevent sensitive information from being visible in the main module.

__init__.py
- used to mark directories on a disk as Python package directories,  

'output' folder
- the parent folder directory that contains multiple subdirectories where ZIP files are downloaded and extracted,  

'Parcels' and 'Roads' folders
- subdirectories of the output folder and the parent folders of two additional subdirectories:
       1. 'YYYY_MM' folder ("date-stamped", ex. 2022_09)
          - the working directory where ZIP files are downloaded and unextracted  
       2. 'Current' folder 
          - the working directory where ZIP files are downloaded and extracted  
````  

*__Note__: The time-stamped folder is created and named after the year and month in which the main module is executed (ex. 2022_09).  
If the main module is executed more than once a month, all downloaded files with the same name in both the 'YYYY_MM' and 'Current' folder directories will be overwritten.*  

## Getting Set Up  

1. Download and extract the entire repository to your operating system in a prefered working directory.
2. Using your IDE of choice, open the 'Python_Package' as a new project.
3. Open the 'sangis_credentials.py' Python file and input your username and password used to log in to the SanGIS/SANDAG GIS Data Warehouse website.
4. Open the 'sangis_download.py' and use the following information below to help guide your understanding of the logic of the main module.  

### Important Imports
Notice the bottom import is called 'sangis_credentials'; this is the name of the Python file that contains our login credentials for accessing the SanGIS/SANDAG GIS Data Warehouse website. Importing the module allows us to access those variables and use them in our main module. We carryout this process in the loginCredentials() Class Method below.
````
import os
import time
import zipfile
from twill.commands import *
from twill import browser

import sangis_credentials
````

### Class Object & Constructor Method  
Description:
````
# Create a SanGISDownload Class Object & encapsulate all methods and variables.
class SanGISDownload:

    # Create constructor, set the parameters, and initialize class variables.
    def __init__(self, directory, filename):
        """Constructor initializes some class variables.
           :param self: pass 'self' to access variables coming from the constructor
           :param directory: a complete path of directory to be changed to new directory path.
           :param filename: the name of downloaded file(s)."""
           
        # Initialize class variables
        self.directory = directory
        self.filename = filename
        self. current_month_folder = None
````

### changeDirectory() Method  
Now that we have created our Class and Constructor, we are free to access or modify our objects attributes in our Methods.  
For our first Class Method, we will create and change directories to ensure all ZIP files are downloaded and extracted in an organized workflow each month.  
````
    def changeDirectory(self):
        """Creates a "date-stamped" subdirectory (folder).
           Changes the current working directory to specified path.
           :param current_month_folder: a file path to the date-stamped folder(s)"""

        # Modify attribute properties
        directoryPath = self.directory

        # Store the current year and month to a variable.
        currentMonth = time.strftime("%Y_%m")

        # Create a new directory (folder) if it does not already exist.
        if os.path.isdir(directoryPath + currentMonth):
            print("Directory already exists")
        else:
            print("Creating directory for you")
            os.mkdir(directoryPath + currentMonth)

        # Change the current working directory to the date-stamped folder.
        os.chdir(directoryPath + currentMonth)

        # Fetch and assign the current directory
        directory = os.getcwd()

        # Reassign the current directory
        self.current_month_folder = directory

        # Print the new current working directory
        print(directory)
````
 ### loginCredentials() Method  
 Description:    
```` 
     def loginCredentials(self):

        go('https://rdw.sandag.org/Account/Login')
        showforms()

        fv("1", "ctl00$MainContent$Email", sangis_credentials.username)
        fv("1", "ctl00$MainContent$Password", sangis_credentials.password)
        submit('0')
````     
### downloadZippedFile() Method  
Description:  
````
     def downloadZippedFile(self):

        go("gisdtview.aspx?dir=Parcel")
        go("GetFSFile.aspx?dir=Parcel&Name=" + self.filename)

        with open(self.filename, "wb") as bf:
            bf.write(browser.dump)
````            
### extractZippedFile() Method  
Description:  
````            
     def extractZippedFile(self):

        myzip = zipfile.ZipFile(
            self.current_month_folder + "\\" + self.filename, 'r')

        myzip.extractall(self.directory + "Current")

        # close the ZIP file
        myzip.close()
````        
### processSanGIS() Method  
Here, we build a Class Method to handle exceptions (errors) that occur during our runtime (execution) of the program.  
We handle these expections gracefully using try and exception statements.  
For example, if the try block raises an exception, the except block will return the exception that may be caused by the try block.  
````           
    def processSanGIS(self):
        """ try block: contains the code that may cause the exception.
             except block: returns the exception that may be caused by the try block."""
        try:
            self.changeDirectory()
        except Exception as e:
            print("Exception when trying to change directory")
            print(print(str(e)))
            return

        try:
            self.loginTo()
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
````            
### main() Method  
Description:  
````
def main():
    directory1 = 'INPUT FOLDER DIRECTORY\\Python_Package\\output\\roads\\'
    download1 = SanGISDownload(directory1, "Assessor_Book.zip")
    download1.processSanGIS()

    directory2 = 'INPUT FOLDER DIRECTORY\\Python_Package\\output\\parcels\\'
    download2 = SanGISDownload(directory2, "PARCELS_EAST.zip")
    download2.processSanGIS()


if __name__ == '__main__':
    main()
````
