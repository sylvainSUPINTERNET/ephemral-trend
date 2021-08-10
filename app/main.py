from flask import Flask
app= Flask(__name__)

import urllib.request
from bs4 import BeautifulSoup


request = urllib.request.Request('https://www.zalando.fr/promo-homme/')

response = urllib.request.urlopen(request)
promo_male_soup = BeautifulSoup(response.read().decode("utf8"), 'html.parser');
articles_identifier_class = " ".join(promo_male_soup.find("article")["class"]); # Seems to be an hash generated so

print(articles_identifier_class);

# try:
# except Exception as e:
#     print(e)
#     print("something wrong")


@app.route('/')
def index():
  return "<h1>Welcome to CodingX</h1>"