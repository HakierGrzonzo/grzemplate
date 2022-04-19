from os import environ

if environ.get("GRZEMPLATE", "") == "DEBUG":
    DEBUG = True
else:
    DEBUG = False
