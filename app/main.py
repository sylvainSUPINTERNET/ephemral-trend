from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
import os
import json
from dotenv import load_dotenv
from flask_cors import CORS
from flask_migrate import Migrate

load_dotenv()

app= Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

app.config['DEBUG'] = True
POSTGRES = {
    'user': os.getenv('PG_USER'),
    'pw': os.getenv('PG_PASSWORD'),
    'db': os.getenv('PG_DB_NAME'),
    'host': os.getenv('PG_DB_HOST'),
    'port': os.getenv('PG_DB_PORT'),
}
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:\
%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from model.Article import Article;
# https://flask-sqlalchemy.palletsprojects.com/en/2.x/quickstart/
db.create_all();


import urllib.request
from bs4 import BeautifulSoup


# TODO => remove it out of testing context 
LIMIT_ITEM = 40

request = urllib.request.Request('https://www.zalando.fr/promo-homme/')
response = urllib.request.urlopen(request)

# create soup
promo_male_soup = BeautifulSoup(response.read().decode("utf8"), 'html.parser');

# Seems to be an hash generated so
articles_identifier_class = " ".join(promo_male_soup.find("article")["class"]); 

# 32 items since we CAN't scroll with bs4 ( should use puppeteer for it but idc)
articles_div = promo_male_soup.find_all("article", {"class": articles_identifier_class})



htmls_articles_pages = [];

# Call for each promo items the HTML page to get interessting value ( size available / price before and after promo / name / rating etc)

for article in articles_div[:LIMIT_ITEM]:
      link_val = article.find_all("a", href=True)[0]["href"];
      le = len(link_val.split("."))
      if le != 0:
        if link_val.split(".")[len(link_val.split(".")) - 1] == "html":
              
              print(link_val)

              # Create soup for each article and save it
              request = urllib.request.Request(link_val);
              response = urllib.request.urlopen(request);
              article_soup = BeautifulSoup(response.read().decode("utf8"), 'html.parser');

              htmls_articles_pages.append(article_soup);




for soup_article in htmls_articles_pages:     
      thumbnails_urls = []
      big_picture_urls = []       

      base_article = soup_article.find_all("x-wrapper-re-1-3")[0];
      main_left = soup_article.find_all("x-wrapper-re-1-2")[0];


      # Big picture if exist
      for el in main_left.select("div > div.JT3_zV > ul > li > div > div > img"):
            if el.get("src") != None :
                  big_picture_urls.append(el.get("src"))

      # Small one on the left IF exist
      for small_pic_div in base_article.select("x-wrapper-re-1-3 > div.okmnKS > div.w5w9i_ > div > div"):
            for img in small_pic_div.find_all('img'):
                  thumbnails_urls.append(img.get("src"))

      article_name = base_article.find_all("h1")[0].text;
      article_brand_name = base_article.find_all("h3")[0].text;
      article_prices = [i.text for i in base_article.find_all("span") if i.text.find("€") != -1]; # 0 promo 1 real price
      article_promo = [i.text for i in base_article.find_all("span") if i.text.find("%") != -1]; # promo


      # Price need to be formatted due to shit character
      promo_splitted = article_prices[0].split(",")
      real_price_splitted = article_prices[1].split(",")

      formatted_promo = f"{promo_splitted[0]}.{promo_splitted[1][:2]}" 
      formatted_real_price = f"{real_price_splitted[0]}.{real_price_splitted[1][:2]}" 

      resp_t = ""
      if len(thumbnails_urls) > 0:
            resp_t = ", ".join(thumbnails_urls)
      else:
            resp_t = ""


      resp_b = ""
      if len(big_picture_urls) > 0:
            # resp_b = ", ".join(big_picture_urls)
            resp_b = big_picture_urls[0]

      article_thumbnails_url = resp_t;
      article_big_picture_urls = resp_b;


      a = Article.query.filter_by(article_name=article_name).first()
      if a == None :
            new_article = Article(article_name=article_name, article_brand_name=article_brand_name, article_promo_percent=article_promo[0].split("%")[0], article_promo_price=formatted_promo, article_real_price=formatted_real_price, article_thumbnails_url=resp_t, article_big_picture_urls=resp_b)
            db.session.add(new_article)
            db.session.commit()
      else:
            print(f"article updated : {article_name}, already exist !")
            num_rows_updated = Article.query.filter_by(article_name=article_name).update(dict(article_name=article_name, article_brand_name=article_brand_name, article_promo_percent=article_promo[0].split("%")[0], article_promo_price=formatted_promo, article_real_price=formatted_real_price, article_thumbnails_url=resp_t, article_big_picture_urls=resp_b))
            db.session.commit()



@app.route('/api/v1/ephemeral/articles')
def index():
      response_articles=[]
      articles = Article.query.all();
      for article in articles:
            response_articles.append(article.as_dict())
      return jsonify(response_articles), 200