# Automate SanGIS using Python  
Manually downloading countless files onto our operating systems is repetitive, inefficient, and expensive. But it doesn't have to be that way. Python offers a way to cut costs considerably by streamlining and automating these time-consuming processes. In this demonstration, I outline how to use Python's "twill" package to access and navigate the SanGIS/SANDAG GIS Data Warehouse website so we can download and extract multiple ZIP files to our operating system. While at the same time, we automate how we want our output directories structured each time we run the program, making it easy to locate the files we are looking for, lending itself nicely to code reproducibility. The script below is modularized and thoroughly explains how each process is executed so that you can quickly learn how to implement it into your project activities.

### Overview of twill's Python API ###  
The Python package "twill," is based on requests and lxml packages and is described as a simplified scripting language developed for programmatic or automated website navigation through a command-line interface. You may use twill to navigate websites that employ forms, cookies, and other standard Web features. Moreover, twill provides excellent support for both MySQL and PostgreSQL database management tasks.

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
conda create -n sangisdownload python=3
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

#### Modules ####

| Module | Description |  
| --- | --- |  
| `sangis_download.py` | The main module that runs the entire process |  
| `sangis_credentials.py` | A module used to secure sensative information from being visible |  
| `__init__.py` | A module used to mark directories on a disk as Python package directories |  

#### Directories ####

| Parent Output  | Description |  
| --- | --- |  
| `output`  | The parent directory that contains multiple subdirectories |  
| `Parcels` | A subdirectory of the output used for storing and extracting parcel files |  
| `Roads`   | A subdirectory of the output for storing and extracting road files |  

#### Subdirectories ####

| Child Output | Description |  
| --- | --- |  
| `YYYY_MM`  | A generated subdirectory, and the download working directory for unextracted zipped files |  
| `Current` | A generated subdirectory, and the download working directory for extracted zipped files |  
  
  
__Important__: There are a few instances you should keep in mind about the child output directories.  
  
  
__1.__ The "date-stamped" output directory is generated and named after the year and month in which the main module is executed (for example, __2022_09__), this means a new date-stamped output directory will be created and named after every month.

__2.__ In the case of the __'Current'__ output directory, the extracted contents from the previous download month are replaced every month; however, this occurs only if the extracted files have the same name.

__3.__ Lastly, if for any reason the main module is ran more than once a month, all downloaded files with the same name in both the __'YYYY_MM'__ and __'Current'__  output directories will be overwritten.

In short, __*every month*__, we want to __*archive*__ the previous months __*unextracted*__ zipped files in a __*YYYY_MM*__ output directory, and we want to __*overwrite*__ the __*extracted*___ contents in the __'Current'__ output directory.

This might not be very clear now, but it will make more sense after we review the entire program's functionality below. 

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
Now that we have created our Class Constructor,, we are free to accesss and modify our Class Objects Attributes in our Methods.
For out first Class Method, we will build out directories to ensure all ZIP files are downloaded and organized into specific output directories.
````
    def buildDirectory(self):
        """Creates "date-stamped" subdirectories,
           Changes the current working directory to output file path,
           :current_month_folder: a Class Variable containing the file path to the date-stamped subdirectories"""
        
        # Modify attribute properties,
        directoryPath = self.directory

        # The strftime() method converts a date object in a String
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
Here, we build a Class Method to Handle Exceptions (errors) that occur during our Runtime (execution) of the program.  
We Handle these Expections gracefully using Try and Exception Statements. For Example, if the Try Block Raises an Exception, the Except Block will Return the Exception that may be caused by the Try Block.  
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
