This program provides a mean of scanning open markets on reddit to provide you email updates when a new posts hits your desired subreddit with your search criteria.

In scanning subreddits for used gear, I would always have an issue with people beating me to the punch and locking in a deal before I even had a chance to reach out to the seller. This application ensures I am always first in line.

How it works

------------------------------

This program connects to Reddit's API via the PRAW module and scans the database intermittently for your search criteria. Once an new item is found, it sores that item's ID in a sqlLite database and sends the user an email with the link. The database ensures you do not recieve mutliple emails for the same post. 


How to use this program

------------------------------


- All necessary update data is stored in configtemplate.py
- Once the repository is cloned, rename the configtemplate.py to config.py
- Open the newly named config.py file 
- Register your application with reddit:

    - Login to reddit and go to https://www.reddit.com/prefs/apps/
    - At the bottom of the page select "create another app"
        - Give the application a name
        - Select "Script"
        - Give your application a description
        - input a redirect uri. This is not really relevant for the program - I used the following: http://www.example.com/unused/redirect/uri
        - Once complete, a new developed application will generate.
            - Under "personal use script" is an ID. Input this ID as the clientid variable in the config.py
            - The "secret" is your personal token. Input this ID as the clientsecret variable in the config.py
        - User agent is the way reddit can recognize you as you are using your app. Typically it would be something like "appname by u/{your user name}"

- Input the subreddit you would like to access as the subreddit variable in config.py. The subreddit name should be the same as the subreddit in the URL

    - Example: https://www.reddit.com/r/EDCexchange --in this example, the subreddit would be 'EDCexchange'


- Input the name of the product you would like to search for in the searchname variable in config.py. This would be the exact, case sensitive search you would use in the subreddit.
- Input the email address that the email would be coming from in the fromemail variable, it would be recommended to set up a bot gmail account and allow less secure apps.
- Input the password that the email would be coming from in the from password variable.
- Input the email address the email will be going to in the toemail variable

- Youre all set! Enjoy your new products.
