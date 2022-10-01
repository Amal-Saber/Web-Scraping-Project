

from bs4 import BeautifulSoup
import requests
import csv


csv_file = open("home_scraping.csv", "w")
csv_writear = csv.writer(csv_file)
csv_writear.writerow(["address", "price", "area_in_m2", "num_of_rooms", "features"])

url = "https://www.pararius.com/apartments/amsterdam"


def scraping_page(url):

  respons = requests.get(url).text
  soup = BeautifulSoup(respons,"lxml")


  for post in soup.find_all("section"):
    address = post.find("div", class_="listing-search-item__sub-title" ).text.strip()
    price = post.find("div" , class_="listing-search-item__price").text.strip()

    area_in_m2 = int(post.find("li", 
    class_="illustrated-features__item illustrated-features__item--surface-area").text.split(" ")[0])

    num_of_rooms = int(post.find("li", 
    class_="illustrated-features__item illustrated-features__item--number-of-rooms").text.split(" ")[0])

    try:
        features = post.find("li" , class_="illustrated-features__item illustrated-features__item--interior").text
    except:
        features =None
    csv_writear.writerow([address, price, area_in_m2, num_of_rooms, features])
    
  return soup

def next_page(soup):
  next = soup.find("ul", class_= "pagination__list")
  if  next.find("li", class_= "pagination__item pagination__item--next" ):
    url= "https://www.pararius.com" + str(next.find("li", class_= "pagination__item pagination__item--next").find("a")["href"])
    return url
  else:
    return    

while True:
  soup = scraping_page(url)
  url = next_page(soup)
  if not url :
    break

csv_file.close()    