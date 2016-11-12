#Link saver Telegram bot

##About

This was a little project to train me with node and mongo. It is a simple telegram 
bot that accepts all the url you send to him and store it in a database. 

Also you can set timezones using flags. The idea was to make a scheudle and give urls
at a certain time every day. Not continuing with it cause didn't saw anything interesting in it.

Also added a flask website that reads the mongo database and shows the link in a website looking for user's secret code.

##How to interact with the bot

* On every link sended it will store in the database.
* If you add a lockpad or `!private` to the message the link is not showed on website but is on database
