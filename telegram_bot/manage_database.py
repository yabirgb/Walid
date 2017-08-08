from peewee import *
from models import *

def start():
    print("Starting creation of tables in " + str(DATABASE))
    db.create_tables([User, Link, Map, Message], safe=True)
    print("Tables created")

def users_count():
    print(len(User.select()))

def clean_auth():
    query = User.update(authCode=0).where()

if __name__ == '__main__':
    import sys
    if sys.argv[1] == "start":
        start()
    elif sys.argv[1] == "users":
        users_count()
