# Wikipedia-Infobox-Scraping-By-Python
---
Scraping the infobox information of people's profiles on Wikipedia.  This utilizes only the python language.

(As of 5/29/2017) This is only picking up the person's name, birth place, birth date, death date, and death place from Wikipedia.  The strings are being refined for output.

(Please note: this is using Python 2.7 and is tested on MacOS Sierra)

## Installation Guide
----
1. Install Python Package - mwparserfromhell
    1. Using PIP 
        ```
        pip install mwparserfromhell
    2. Using the Package & Git
        ```
        git clone https://github.com/earwig/mwparserfromhell.git
        cd mwparserfromhell
        python setup.py install
    (Here is the link to the Python Package - https://github.com/earwig/mwparserfromhell)
    
## Usage
---
1. Grab each individual file or Download the Package (Using Git)
    ```
    git clone https://github.com/JLDevOps/Wikipedia-Infobox-Scraping-By-Python.git
    cd Wikipedia-Infobox-Scraping-By-Python
    ```
2. To run the Python file with the attached names.csv 
    ```sh
    python unit-csv.py
    ```
    Running this command will result in (As of 5/29/2017):
    ![](https://github.com/JLDevOps/Wikipedia-Infobox-Scraping-By-Python/blob/master/image/result.png?raw=true)
