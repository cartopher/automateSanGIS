# Automate SanGIS Downloads using Python

## Workflow
The steps below explain how Python can automate the ZIP file download process from the SanGIS/SANDAG GIS Data Warehouse website. In this demonstration, the 'Parcels_East.zip' and ‘Assessor_Book.zip’ ZIP files are: 

Downloaded to our operating system, stored into a newly created year a month time stamped folder directory.

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

Open the Command Prompt and install the package 'twill' by inputting the following lines of code into the command line:

pip install twill
