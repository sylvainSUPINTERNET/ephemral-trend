# Run 

```` shell
$ python wsgi.py
````

# Goal 

Provide a way to access trendy products to push them to ephemral API 

# Migrate DB 
# https://flask-migrate.readthedocs.io/en/latest/
python -m flask db init ( only once )

flask db migrate -m "Initial migration."

flask db upgrade

Don't forget first to set env variable : 

$env:FLASK_APP="app/wsgi.py" ( else you face error with import )

# Interessting 

https://towardsdatascience.com/using-google-trends-at-scale-1c8b902b6bfa

# document.querySelectorAll("x-wrapper-re-1-3 > div.okmnKS > div.w5w9i_ > div > div")
# document.querySelectorAll("body > div > div > div.VaE1kV > div > div.VHXqc_ > x-wrapper-re-1-2 div > div.JT3_zV > ul")
