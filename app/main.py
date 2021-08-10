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
              
              # Create soup for each article and save it
              request = urllib.request.Request(link_val);
              response = urllib.request.urlopen(request);
              article_soup = BeautifulSoup(response.read().decode("utf8"), 'html.parser');

              htmls_articles_pages.append(article_soup);


print(len(htmls_articles_pages))






# print(len(articles_div));
# scrapped_articles = [];
# for article in articles_div:
#       scrapped_articles.append(
#         {
#           "span_text": ""
#         }
#       )
#       span_text.append({"span_text" : article.find_all("span") })
#       h3_text = article.find_all("h3")
#       h3_text.append({""})


# try:
# except Exception as e:
#     print(e)
#     print("something wrong")


@app.route('/')
def index():
  return "<h1>Welcome to CodingX</h1>"