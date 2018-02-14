# Formula - 1 Codechef Ranklist
This is implementation of the idea to maintain a f1 type ranklist for codechef monthly contests (Long, Cook-Off, Lunch Time). <br/>
The scoring is as follow: [25, 18, 15, 12, 10, 8, 6, 4, 2, 1]<br/>

Each year is divided into two 5 month periods.<br/>
Even: {Jan, Feb, March, April, May}<br/>
Odd: {July, Aug, Sept, Oct, Nov}<br/>
Starting from Jan-2014 to current

The current app is configured for National Institute of Technology, Durgapur. Change appropriately in makeDB.views for generating data about other colleges.

## How to run it?
* Install virtualenv
* Create an environment using virtual env `virtualenv envName -p python3`
* Activate the environment and install the requirements `source envName/bin/activate; pip3 install -r req.txt`
* Migrate the database as usual
* Start the server `python manage.py runserver`
* Go to `localhost:8000/makedb/` This will create the DB with all the info, also redirect you to 14E ranklist. This will take an awful lot of time, check your terminal for completion. If any error, just refresh the page.
* For checking any contest use the following url: `localhost:8000/showTables/[0-9]{2}[OE]{1})$`

## Specific parts

### MakeDB
This app is used to create a model to store data, its a many to many mapping

### showTables
This app is used to display the data according to user specifications in the URL

![alt text](https://i.imgur.com/floBN2d.png)
