import urllib
from urllib import parse
from bs4 import BeautifulSoup
from pprint import pprint
from urllib.parse import urlparse
import urllib.request
from selenium import webdriver
from bs4 import NavigableString
import sys
from selenium.webdriver.firefox.options import Options
import json 

browser = None

try:
    options = Options()
    browser = webdriver.Firefox(options=options)
except Exception as error:
    print(error)

out_file = open("oyo_rooms.json", "a")


class OyoRoomsGen:
    def __init__(self, url):
        self.url = url
        self.html_text = None
        try:
            browser.get(self.url)
            self.html_text = browser.page_source
            # self.html_text = urllib.request.urlopen(url).read().decode('utf-8')
            # self.html_text = requests.get(url).text
        except Exception as err:
            print(str(err))
            return
        else:
            print('Access successful.')

        self.soup = None
        if self.html_text is not None:
            self.soup = BeautifulSoup(self.html_text, 'lxml')

    def scrap(self):
        soup = self.soup
        for div in soup.findAll("div",attrs={"class":"oyo-row oyo-row--no-spacing listingHotelDescription"}):
            details = dict()
            details['name']=" "
            details['address']=" "
            details['rating']=" "
            details['review_count']=" "
            details['rating_summary']=" "
            details['facilities']=" "
            details['price']=" "
            details['offer']=" "
            if div.find("h3",attrs={"class":"listingHotelDescription__hotelName d-textEllipsis"}) is not None:
                details['name']=div.find("h3",attrs={"class":"listingHotelDescription__hotelName d-textEllipsis"}).text
            if div.find("span",attrs={"class":"u-line--clamp-2"}) is not None:
                details['address']=div.find("span",attrs={"class":"u-line--clamp-2"}).text
            if div.find("span",attrs={"class":"is-fontBold hotelRating__rating hotelRating__rating--fair hotelRating__rating--clickable"}) is not None:
               details['rating']=div.find("span",attrs={"class":"is-fontBold hotelRating__rating hotelRating__rating--fair hotelRating__rating--clickable"}).text
            if div.find("span",attrs={"class":"hotelRating__ratingSummary  hotelRating__rating--clickable"}):
                details['review_count']=div.find("span",attrs={"class":"hotelRating__ratingSummary  hotelRating__rating--clickable"}).text
            if div.find("span",attrs={"class":"hotelRating__ratingSummary"}) is not None:
                details['rating_summary']=div.find("span",attrs={"class":"hotelRating__ratingSummary"}).text
            for i in div.findAll("span",attrs={"class":"d-body-sm d-textEllipsis"}):
                details['facilities']+=i.text
            if div.find("span",attrs={"class":"listingPrice__finalPrice"}) is not None:
                details['price']=div.find("span",attrs={"class":"listingPrice__finalPrice"}).text
            if div.find("span",attrs={"class":"listingPrice__percentage"}) is not None:
                details['offer']=div.find("span",attrs={"class":"listingPrice__percentage"}).text
            json.dump(details,out_file)
            out_file.write(",\n")
            
if __name__ == '__main__':
    if browser is None:
        print("Selenium not opened")
        sys.exit()

    for x in range(1, 7):
        print("Accessing page: " + str(x) + '\n')
        zr = OyoRoomsGen('https://www.oyorooms.com/hotels-in-pune/?page={}'.format(x))
        zr.scrap()
    browser.close()
    out_file.close()