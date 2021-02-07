import requests
import praw
import config
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import ssl
import sys
import requests.auth
import time
import sqlite3
from datetime import datetime

now = datetime.now()

#Tests and gathers token data
#client_auth = requests.auth.HTTPBasicAuth('IKKm5-L5h9IQOg', 'Nw27s3AW0Pi0tB6WyewYu13LWPZdVQ')
#post_data = {"grant_type": "password", "username": "fleegz2007", "password": config.frompassword}
#headers = {"User-Agent": "hwsscraper/0.1 by fleegz2007"}
#response = requests.post("https://www.reddit.com/api/v1/access_token", auth=client_auth, data=post_data, headers=headers)
#sessiontoken = response.json()['access_token']
#tokentype = response.json()['token_type']
#headers = {"Authorization": tokentype + ' ' + sessiontoken, "User-Agent": "hwsscraper/0.1 by fleegz2007"}
#response = requests.get("https://oauth.reddit.com/api/v1/me", headers=headers)'''

reddit = praw.Reddit(
    client_id=config.clientid,
    client_secret=config.clientsecret,
    user_agent=config.useragent,
    )

submissions = {"submission_id": [], "created_date": [], "flair": [], "title": [], "url": []}

for submission in reddit.subreddit(config.subreddit).search(config.searchname, sort = 'new', limit = 50):
    submissions["submission_id"].append(submission.id)

for submission in reddit.subreddit(config.subreddit).search(config.searchname, sort = 'new', limit = 50):
    submissions["created_date"].append((datetime.fromtimestamp(int(submission.created))))

for submission in reddit.subreddit(config.subreddit).search(config.searchname, sort = 'new', limit = 50):
    submissions["flair"].append(submission.link_flair_text)

for submission in reddit.subreddit(config.subreddit).search(config.searchname, sort = 'new', limit = 50):
    submissions["title"].append(submission.title)

for submission in reddit.subreddit(config.subreddit).search(config.searchname, sort = 'new', limit = 50):
    submissions["url"].append(submission.url)

#print(submissions["submission_id"][0])
#print(submissions["created_date"][0].strftime('%Y-%m-%d'))
#print(submissions["flair"][0])
#print(submissions["title"][0])
#print(submissions["url"][0])
#print(now.strftime('%Y-%m-%d'))

connection = sqlite3.connect("redditswaps.db",
                            detect_types=sqlite3.PARSE_DECLTYPES |
                            sqlite3.PARSE_COLNAMES )
cursor = connection.cursor()

tableCheck = cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name = ?;", ('swapdata',)).fetchall()
if tableCheck == []:
    cursor.execute("CREATE TABLE swapdata (id TEXT PRIMARY KEY, createddate TIMESTAMP, flair TEXT, title TEXT, url TEXT, tmstmp TIMESTAMP);")


sendlist = {"submission_id": [], "created_date": [], "flair": [], "title": [], "url": []}

#cursor.execute("DELETE FROM swapdata WHERE id LIKE 'kfhebe'")

for i in range(len(submissions["submission_id"])):
    id = submissions["submission_id"][i]
    idcheck = cursor.execute("SELECT id FROM swapdata WHERE id LIKE ?;", (id,)).fetchall()
    if idcheck == []:
        sendlist["submission_id"].append(submissions["submission_id"][i])
        sendlist["created_date"].append(submissions["created_date"][i])
        sendlist["flair"].append(submissions["flair"][i])
        sendlist["title"].append(submissions["title"][i])
        sendlist["url"].append(submissions["url"][i])
        cursor.execute("INSERT INTO swapdata ('id', createddate, 'flair', 'title', 'url', 'tmstmp') VALUES (?, ?, ?, ?, ?, ?);", (submissions["submission_id"][i], submissions["created_date"][i], submissions["flair"][i], submissions["title"][i], submissions["url"][i], now))
        connection.commit()
    else:
        continue


#For now adding to check the number of items added to ensure above loop works correctly
rows = cursor.execute("SELECT COUNT(*) FROM swapdata").fetchall()

if sendlist["submission_id"] == []:
    print("No new posts found. Exiting...")
    sys.exit()
else:
#Email Message
    message = MIMEMultipart("alternative")
    message["Subject"] = "Hey dude, sexy new " + config.searchname + "\'s local in your area!"
    message["From"] = config.fromemail
    message["To"] = config.toemail

    links = ''
    for i in range(len(sendlist["submission_id"])):
        links += '''<li><b><a href={}>{}</a></b></li>\n'''.format(sendlist["url"][i], sendlist["title"][i])

    html = '''\
    <html>
    <body>
            <p>Hey dude,<br>
            Check out these links for new {} postings on {}!<br>
            {}
            </p>
        </body>
    </html>
    '''.format(config.searchname, config.subreddit, links)   
    content = MIMEText(html, "html")
    message.attach(content)


    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(config.fromemail, config.frompassword)
        server.sendmail(config.fromemail, config.toemail, message.as_string())
