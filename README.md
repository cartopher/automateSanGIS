# Automate SanGIS Downloads using Python

## Workflow
The instructions listed below describe how we can use Python to automate download procesess from the SanGIS/SANDAG GIS Data Warehouse website. In this demonstration, we use the "twill" package to access and download multiple ZIP files from San Diego's Regional GIS Data Source, then store and extract their contents to specific folder directories on our operating system.

***twill Package***  
The Python package "twill," based on requests and lxml packages, is a simplified scripting language developed for programmatic or automated website navigation through a command-line interface. You may use twill to navigate websites that employ forms, cookies, and other common Web features. Moreover, twill provides excellent support for both MySQL and PostgreSQL databases management tasks.

For more about the 'twill' package, see:  
twill Project Description (https://pypi.org/project/twill/)  
twill Overview (https://twill-tools.github.io/twill/overview.html)  
twill’s Python API (https://twill-tools.github.io/twill/python-api.html#python-api)  

## Installation

Note: If you prefer to use an existing virtual environment, all you need to do is run the ‘pip install twill’ command.

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
## Getting Set Up
The Python_Package contains:  
````
sangis_download.py
- the main module containing the entire executable script,

sangis_credentials.py
- this module contains statements that store login credentials to string variables
- to prevent the visiibilty of sensetive information in the main module, this module is imported into the main module so the string variables can be used,

__init__.py
- used to mark directories on a disk as Python package directories,  

'output' folder
- the parent folder directory that contains multiple subdirectories where ZIP files are downloaded and extracted,  

'Parcels' and 'Roads' folders
- subdirectories of the output folder and the parent folder of two additional subdirectories:
       1) 'YYYY_MM' folder 
          - the relative path where ZIP files are downloaded and unextracted  
       2) 'Current' folder 
          - the relative path where ZIP files are downloaded and extracted  
````  

*__Note__: The time-stamped folder is created and named after the year and month (ex. 2022_09) the main module is executed. 
For any reason the main module is executed twice in one month, all downloaded files with the same name in both the 'YYYY_MM' and 'Current' folders will be overwritten.*  


1. Download entire repository to your operating system. Save and extract the contents into a prefered directory. 
2. Using your IDE of choice, open the 'Python_Package' as a new project.
3. Open the 'sangis_credentials.py' Python file and input your username and password used to login to the SanGIS/SANDAG GIS Data Warehouse website.
4. Open the 'sangis_download.py' file and view the script.

#### Important Imports
Notice the bottom import is called 'sangis_credentials', this is the name of the Python file that contains our login credentials for the SanGIS/SANDAG GIS Data Warehouse website.
````
import os
import time
import zipfile
from twill.commands import *
from twill import browser

import sangis_credentials
````

#### Creating a Class Object

````
class sangis_parcels():
    """encapsulate all methods and variables into a Class object"""

    # assign class variables
    directory = None
    filename = None
    current_month_folder = None
````

#### Create Constructor and Set Parameters

````
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
````

#### Create Directory Function

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
        
 #### Create Login Function
 
     def login(self):
        """Description:"""

        # talk to the web browser directly
        go('https://rdw.sandag.org/Account/Login')
        showforms()

        # input login credentials
        fv("1", "ctl00$MainContent$Email", sangis_credentials.username)
        fv("1", "ctl00$MainContent$Password", sangis_credentials.password)
        submit('0')
        
#### Create Download Function
 
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
            
#### Create Zip File Extraction Function
            
     def extractZippedFile(self):
        """Description:"""

        myzip = zipfile.ZipFile(
            self.current_month_folder + "\\" + self.filename, 'r')

        myzip.extractall(self.directory + "Current")

        # close the ZIP file
        myzip.close()
        
#### Create a Function for Exception and Handling
            
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
            
#### Define the Main Method
````
def main():
    """Description:"""
    directory1 = 'INPUT FOLDER DIRECTORY\\Python_Package\\output\\roads\\'
    download1 = sangis_parcels(directory1, "Assessor_Book.zip")
    download1.process_sangis()

    directory2 = 'INPUT FOLDER DIRECTORY\\Python_Package\\output\\parcels\\'
    download2 = sangis_parcels(directory2, "PARCELS_EAST.zip")
    download2.process_sangis()


if __name__ == '__main__':
    main()
````
