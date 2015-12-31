#Properties defined in local_settings.py
ADMINS = ()
ALLOWED_HOSTS = [] # If DEBUG = False

DATABASES = {
    "default": {
        "ENGINE": "mysql.connector.django",
        "NAME": "", # your db name
        "USER": "", # your db username
        "PASSWORD": "", # your db password
        "HOST": ""
    },
    "sarv": {
        "ENGINE": "mysql.connector.django",
        "NAME": "", # your db name
        "USER": "", # your db username
        "PASSWORD": "", # your db password
        "HOST": ""
    }
}

NEXTIFY_DOWNLOAD_DIR = "" # File download directory

PUBLIC_STATIC_URL = "/public/"

USER_DATABASE = "users"

ACL_USERLEVELS = ("guest","user","editor","admin") # No need to change this

# Map which userlevel has which right
ACL_USERRIGHTS = [
    [False,False,False,False],
    [True,False,False,False],
    [True,True,"own","own"],
    [True,True,True,"own"],
    [True,True,True,True]
]

PROJECT_ADMINS = [] # Project admin user id list
