# Baby Sleep Tracker
#### Video Demo:  https://youtu.be/mNka-mV02UI
#### Description:


## Overview of the baby sleep tracker:
#### Coded by: Dennis Luetz-Hawranke

My Web application allows a parent to track the sleep time of their baby. User can:

- ...register a username, password and a babyname
- ...add more babies while logged in

- ...add Entries to the Database: On what date and time did the baby fall asleep and at what time did it wake up.
- ...in case of multiple babies, the relevant child has to be selected from the select list. By default the first child entered is selected.
- ...press a button to get the current time when the child falls asleep (todays date is then added automatically)
- ...press a button to get the current time when the child wakes up

- ...view all dataentries of each child in a table
- ...in case of enough data entries, get information on
    - ... the time of each sleeping session
    - ... average time per nap
    - ... average time of sleep each night
    - ... average time spent napping per day
    - ... 3 most regular exact nap times
    - ... 3 most regular nap timeframe +- 10min

As a sepcial function just for my user I also wrote an import function with which I am able to import the chat logs with my wife. Each line of this specially formated text file can then be read and added to the database.

### Future functionalities I intend on adding after submission include:

- A way to limit the time frame while viewing the data (e.g. only include entries between August and September)
- Information on the time spent awake between naps
- A grafical representation of the data in some form or fashion

## How I chose my final project:

As a fresh parent sleep and free time is hard to come by. So one day my wife started writing done the approximate sleep and wake up time of our little baby. The idea was to log the naptimes so we could anticipate them the next day, since we kept forgetting or didn't really know if the sleep schedule was regular (since we were constantly tired ourselves). We would also know why our daughter might be moody, if it reached a certain time during the day. Since I was nearing the end of CS50x :'( it seemed fitting to use this data and analyse it via a Webapp which could be (once delpoyed) used flexbily from any device (compared to lets say an excel sheet).

### Going about development:

A few days worth of nap and sleep data existed when I started this project. After a bit of planning knew I needed the follow database tables:

- Users
    - id
    - Username
    - Password
- Babies
    - ID
    - Name
    - Parent_ID (FK users.id)
- Sleeprecords
    - baby_id
    - date
    - sleeptime
    - waketime

I wanted to use my new found knowledge from C$50 finance and enable users to register for an account. Users are considered to be one or more parents that would like to track their baby or babies sleep. To keep things simple I chose to assume parents would share an account.

Using JavaScript I was able to implement a interactive form, where users can press a button and the current time an date is entered. The idea is that the Parent has this Web App open on their Phone and can simply hit the button when their baby falls asleep. Once the baby wakes up, they can hit the "Just woke up" button and save the data entry. Of course, since this is not always possible (parents might forget, need to be quick or whatever) the data can also be added manually.

Using Python I was able to add the submitted data to the database and return a message to the user that the data entry was successful. If the data entry was unsucessful the user equally recieves a color coded message below the form, after which they can try again.

## Challenges

### Regex
Using Regex to write an import function turned out to be quite the challenge. I needed to re structure the data from the textfile (see temp folder) in a way that was uniform which the entry made by the form submission. Finally i had a lot of fun with it and it turned out to be super useful wehn analysing the sleep data (e.g. when differentiating between naps and night sleep)

### Working with times and dates
Using Date objects took a while to get right. The first challenge was getting times into a useful format. Once that was done i thought it would be easy to just subtract or average times, however one has to consider an hour is sixty minutes. This might sound funny but that realisation took a while. It took a couple of attempts to realize the easiest way to get average times is not infact to take average hours and minutes seperatly. The easiest way was to translate hours into minutes first and once averaged change them back. Late hours of working on these problems required a fresh mind and finally I wrote functions that I am quite pleased with. Although they could do with some cleaning up.

### Checks and Balances

I am proud of a couple of the checks and balances I've added. For example one parent can not simply submit the id of another child via html. One user can really only submit and therefore view babies sleeprecords that are linked to their own session id.

### Small amounts of data

I had some code in Helpers.py that didn't work if there was only a couple of data antries and therefore not anough minutes. Took me a good while to figure out it was because the type string clashed with the round() function. Getting double-digits to show up also turned out the be the basis for a couple of errors.


### THANK YOU

Thank you David, Brian, Doug and the rest of this amazing CS50 team. This really was by far one of the best courses I have ever taken.

## This was CS50!