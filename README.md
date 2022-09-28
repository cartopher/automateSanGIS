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

### Create a Virtual Environment using Anaconda
The list of commands used:
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
