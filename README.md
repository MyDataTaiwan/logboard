# mylog14-dashboard

Frontend for government employees to track custodian data, built on Django Framework with Class Views.

Dependencies can be found in requirements.txt

# Setup

```
$ python3 -m pip install Django
$ python3 -m pip install -r requirements.txt
```

Testing by development server. You need to comment-out the SSL session in `g14Dashboard/settings.py`:

```
$ python3 manage.py makemigrations
$ python3 manage.py migrate
$ python3 manage.py runserver
$ sensible-browser http://localhost:8000
```


WARNING: DASHBOARD Code will be dropped and integrated to applications/archives