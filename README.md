# Movie-library
In this project user can search for Movies details using OMDB API

## Hosted link : https://search4movie.herokuapp.com/

## Dependencies 

All dependencies are provided in the requirement.txt

## Steps to run the project:

1. open this project in vs Code or your preffered IDE
2. pip install all the requirements provided in requirements.txt file.
3. one thing you have to take care of whether your app is connected to the database or not
   - See there would be a database.db file which you have to connect
   - In terminal type *python* and then *form app import db* then *db.create_all()*
   -  you can exit the python using quit()
4. Using sqlite3 check whether tables are created or not
   - type *sqlite3 database.db* and then type *.tables*
   - If *user* appeared the you are good to go.
5. Run the app
6. go to the browser and type *localhost:5000*. Here the website would be running.
