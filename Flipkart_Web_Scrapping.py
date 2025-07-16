#===============================================================================================#
# Author:       Siddhesh Parwade
#
# Motive:       To practice and demonstrate web scraping skills by building a script
#               that collects real-world e-commerce data (5G phone listings) from
#               Flipkart, handles errors gracefully, and saves structured output.
#
# Description : Scrapes 5G phone listings from Flipkart across multiple pages,
#               extracting product name, price, and rating. Handles request headers
#               to mimic browsers, retries failed pages, and saves data to a CSV.
#
# Capability  : It can easily retrive 100 pages of flipkart within 1 hour (without proxies) , 
#               if you uses rotating proxies then it works better.
# ==============================================================================================#

import requests
from bs4 import BeautifulSoup
import time
import random
import csv

## URL without page to increment it pages!
url="https://www.flipkart.com/search?q=5g+phones&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off&page="

products=[]
unfetchedPages=[]

## Diffrent agents for use each in diffrent request!

user_agents = [
    # Windows browsers
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:115.0) Gecko/20100101 Firefox/115.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Edg/123.0 Safari/537.36",

    # Linux browsers
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/122.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64; rv:115.0) Gecko/20100101 Firefox/115.0",

    # Mac browsers
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_5) AppleWebKit/605.1.15 Version/16 Safari/605.1.15",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_5) AppleWebKit/537.36 Chrome/124.0 Safari/537.36",

]

session = requests.Session()

def pageScraper(i, j):
    for page in range(i, j):
        main_url = url + str(page)
        
        ## This headers will work better for flipkart!
        
        headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "accept-encoding": "gzip, deflate, br, zstd",
            "accept-language": "en-IN,en-US;q=0.9,en-GB;q=0.8,en;q=0.7,hi;q=0.6,mr;q=0.5",
            "connection": "keep-alive",
            "host": "www.flipkart.com",
            "sec-ch-ua": '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
            "sec-ch-ua-arch": '"x86"',
            "sec-ch-ua-full-version": '"138.0.7204.98"',
            "sec-ch-ua-full-version-list": '"Not)A;Brand";v="8.0.0.0", "Chromium";v="138.0.7204.98", "Google Chrome";v="138.0.7204.98"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-model": '""',
            "sec-ch-ua-platform": '"Windows"',
            "sec-ch-ua-platform-version": '"19.0.0"',
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "none",
            "sec-fetch-user": "?1",
            "upgrade-insecure-requests": "1",
            "user-agent": random.choice(user_agents)
        }
        
        print("\n\n\n")
        print("User-Agent :  ", headers["user-agent"])
        print("Target-Url :  ",main_url)

        wait_time = random.randint(10, 15)
        print(f"Waiting for {wait_time} seconds before request...")
        time.sleep(wait_time)

        r = session.get(main_url, headers=headers)
        print(r.status_code)

        if r.status_code != 200:
            print(f"Request failed: {r.status_code}")
            unfetchedPages.append(page)
            continue

        soup = BeautifulSoup(r.text, 'html.parser')

        try:
            cards = soup.find_all('div', class_='yKfJKb row') ## If code does not work please check the class name of div that contain info
        except AttributeError:
            print(f"⚠️ Page {page} structure not found. Skipping.")
            continue
        
        for card in cards:
            names = card.find("div", class_="KzDlHZ") ## If code does not work please check the class name of div that contain info
            ratings = card.find("div", class_="XQDdHH") ## If code does not work please check the class name of div that contain info
            prices = card.find("div", class_="Nx9bqj _4b5DiR") ## If code does not work please check the class name of div that contain info

            name = names.text.strip() if names else "None"
            rating = ratings.text.strip() if ratings else "None"
            price = prices.text.strip() if prices else "None"

            products.append([page, name, price, rating])

        print(f"✅ Products collected: {len(products)} till Page {page}")

## Define the number of pages you want to retrive, more pages takes more time!

pageScraper(1,21) # Retrives 20 pages

while unfetchedPages:
    pages_to_retry = unfetchedPages.copy()
    unfetchedPages.clear()
    print("\n\nUnfetched Pages Going To Fetch Again:", pages_to_retry, "\n\n")
    for i in pages_to_retry:
        pageScraper(i, i+1)
    

    
print("\n\n\n----------------------------------------Final Products----------------------------------------------------")

print("   Page_No    :    Name    :    Price    :    Rating    ")
for i in products:
    print(i[0]," : ",i[1]," : ",i[2]," : ",i[3])
    
with open('flipkart_products.csv', mode='w', newline='', encoding='utf-8-sig') as file:
    writer = csv.writer(file)
    writer.writerow(['Page_No','Name', 'Price', 'Rating'])
    writer.writerows(products)

print("\n\n*****CSV file written: flipkart_products.csv*****")
