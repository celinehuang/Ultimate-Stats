import requests as rq
from bs4 import BeautifulSoup
import pandas as pd

#reutnrs table of players from link
def scrapper(link):

   response = rq.get(link)
   html = response.content
   soup = BeautifulSoup(html, features="html.parser")
   roster = soup.find("table", attrs={"class": "global_table"})
   
   return pd.read_html(str(roster), header = 0)
