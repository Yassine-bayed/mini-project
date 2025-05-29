# Steps to setup project
## Setup virtual environment
 - Install Python 3.8 or higher
 - run the following command to create a virtual environment : `python -m venv PAenv`
 - Activate the virtual environment : `PAvenv\Scripts\activate`
 - upgrade pip : `python.exe -m pip install --upgrade pip`
 - Install requirements : `pip install -r requirements.txt`
## Setup database
- Create a new connection in mongoDB Compass	
    > URI : `mongodb://localhost:27017`

    > name : `mini_catalogue`
- Create a new database:
    - launch MongoDB shell
    - run the following command : `use mini_catalogue`
- Create the collections `products` and `categories`:
    - copy the content of `colllections.txt` file
    - paste it in the MongoDB shell

