Welcome to my project made for diploma!

Steps to launch my project fully:

IN TERMINAL:

1) CREATE VIRTUAL ENVIRONMENT: py -m venv venv
2) ACTIVATE IT: venv\Scripts\activate
3) CREATE/SET LOCAL INTERPRETER IN SETTINGS
3) INSTALL RELEVANT PACKAGES: pip install -r requirements.txt
4) CREATE DATABASE IF DOES NOT EXISTS:
   1.py manage.py makemigrations
   2. py manage.py migrate
5) CREATE SUPER USER (TO MANAGE PROJECT FROM DJANGO ADMIN PANEL): py manage.py createsuperuser
6) INPUT username, email (optional), password
7) IN BROWSER: localhost:8000/admin
8) LOG INTO YOUR ADMIN ACCOUNT
9) TO RESOLVE EXCEPTION YOU GET: FILL IN stardard settings, promo, logo MODELS
    ENGOY!!! :)
