import requests as rq
from bs4 import BeautifulSoup
import pandas as pd

#reutnrs table of players from link
def scraper(link):

   response = rq.get(link)
   html = response.content
   soup = BeautifulSoup(html, features="html.parser")
   roster = soup.find("table", attrs={"class": "global_table"})
   
   return pd.read_html(str(roster), skiprows = 0)

def scrape_one_year(link):
   
   df = pd.DataFrame()
   response = rq.get(link)
   html = response.content
   soup = BeautifulSoup(html, features="html.parser")
   roster = soup.find("table", attrs={"class": "global_table"})
   for page in roster.find_all('a', href=True):
      if(str(page['href'])[0] == 'j'):
         continue
      else:
         df = df.append(scraper("https://play.usaultimate.org" + str(page['href'])), ignore_index=True)
   
   return df


if __name__ == "__main__":
   print(scrape_one_year("https://play.usaultimate.org/teams/events/team_rankings/?RankSet=Club-Mixed"))