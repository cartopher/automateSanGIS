# Automate SanGIS Downloads using Python

## Workflow
The steps below explain how Python can automate the download process from the SanGIS/SANDAG GIS Data Warehouse website. In this demonstration, the 'Parcels_East.zip' and ‘Assessor_Book.zip’ files are downloaded, stored, and extracted to our operating system.

The Python package "twill," based on requests and lxml packages, is a simplified scripting language developed for programmatic or automated website navigation through a command-line interface. You may use twill to navigate websites that employ forms, cookies, and other common Web features. Support for both MySQL and PostgreSQL databases.

## Installation

Note: If you prefer to use an existing virtual environment, all you need to do is run the ‘pip install twill’ command.

### Create a Virtual Environment using Anaconda
````
conda create -n dlgisdata python=3
conda activate sangisdownload
pip install twill
conda list
````
#### Instructions

Open the Anaconda Command Prompt and input the follow line of code to create a new virtual environment: 
````
conda create --n sangisdownload python=3
````
Input the following command to activate the environment:
````
conda activate sangisdownload
````
Install the 'twill' package using pip by inputting the following command:
````
pip install twill
````
Return a list of packages and ensure the package twill was installed:
````
conda list
````
