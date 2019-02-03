import requests as rq
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd

#reutnrs table of players from link
def scraper(link):

   response = rq.get(link)
   html = response.content
   soup = BeautifulSoup(html, features="html.parser")
   roster = soup.find("table", attrs={"class": "global_table"})
   
   df = pd.read_html(str(roster), skiprows = 0)
   name = soup.find("div", class_="profile_info").h4.find(text=True)
   name = name.strip()
   df[0]['Team'] = name
   return df

def scrape_one_division(link):
   
   df = pd.DataFrame()
   #driver = webdriver.Firefox()
   #driver.get("https://play.usaultimate.org/teams/events/team_rankings/?RankSet=Club-Mixed")
   #print (driver)
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

def scrape_one_year(link, year):
   df = pd.DataFrame()
   divisions = ["Men", "Women", "Mixed"]
   for div in divisions:
      print(link + div)
      df = df.append(scrape_one_division(link + div))
      print (df)
      df["Division"] = div
   df["Year"] = year

   return df

if __name__ == "__main__":
   scrape_one_year("https://play.usaultimate.org/teams/events/team_rankings/?RankSet=Club-", 20018).to_csv("./data_set.csv")