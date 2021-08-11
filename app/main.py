from flask import Flask
app= Flask(__name__)

import urllib.request
from bs4 import BeautifulSoup


# TODO => remove it out of testing context 
LIMIT_ITEM = 2

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

article_scrapped = [];
for soup_article in htmls_articles_pages:
      base_article = soup_article.find_all("x-wrapper-re-1-3")[0];

      article_name = base_article.find_all("h1")[0].text;
      article_brand_name = base_article.find_all("h3")[0].text;
      article_prices = [i.text for i in base_article.find_all("span") if i.text.find("€") != -1]; # 0 promo 1 real price
      article_promo = [i.text for i in base_article.find_all("span") if i.text.find("%") != -1]; # promo


      # Price need to be formatted due to shit character
      promo_splitted = article_prices[0].split(",")
      real_price_splitted = article_prices[1].split(",")

      formatted_promo = f"{promo_splitted[0]}.{promo_splitted[1][:2]}" 
      formatted_real_price = f"{real_price_splitted[0]}.{real_price_splitted[1][:2]}" 

      article_scrapped.append({
        "article_name": article_name,
        "article_brand_name": article_brand_name,
        "article_promo_percent": article_promo[0].split("%")[0],
        "article_promo_price": formatted_promo,
        "article_real_price": formatted_real_price
      });
      
      #print(article_span);

# TEST
for a in article_scrapped:
      print(str(a))


@app.route('/')
def index():
  return "<h1>Welcome to CodingX</h1>"