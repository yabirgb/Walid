# How to configure this project

## Technical

### Software

Please install all in the file `requirements.txt`.

### What are you running?

Always use python 3. I run python 3.6.

(Documentation)[https://docs.python.org/3/library/venv.html] for VE on python.

To call telegram's API I use (pyTelegramBotAPI)[https://github.com/eternnoir/pyTelegramBotAPI].

As a database `PostgreSQL` (this project **can only live** with `MySql` or `PostgreSQL` due the use of db_evolve). In the server also `Flask` over `Gunicorn`.

## Variables of the environment

Complete list of variables in the environment. Currently running on prod.

#### TOKEN

A valid token for the telegram bot **Needed**

#### POCKET

A valid pocket app token **Needed in the bot**

#### DEBUG

`True` if the state of the app is debug, `False` otherwise **Needed, True by default**

#### DB

DB name **Needed in production**

#### DBUSER

DB user **Needed in production**

#### DBPASS

DB password for user selected **Needed in production**

#### DBHOST

DB host **Needed in production**

#### BASE_URL

The base url to appear in messages.

#### PORT

Port in which Flask should run. By default `8000`

#### OTP

One time password secret key for [pyotp](https://github.com/pyotp/pyotp) **Change in production**

## Manage project

There are some useful functions to manage the project.

To call them use `python file command`

In `telegram_bot/manage_database.py` we have:

* `start` - Create database tables
* `users` - Number of users in database
* `codes` - Change code to all users
* `send`  - Send message to user. Take args `telegram_id` and `message`
* `bulk`  - Send message to all the users. *Should be used hardly never*

In `manage_dev.py`:

This was tought to be used during dev

* `fake`  - Create fake user with name yabir
* `start` - Create database tables
* `me`    - Secret url for yabir
* `save`  - Store an url

## How to run

Once all is configured.

1. Crete DB tables
2. run `telegram_bot/heart.py`. This will start the bot
3. run `server.py` or `server_dev.py` to start the Flask server.
4. All should be running ok.
