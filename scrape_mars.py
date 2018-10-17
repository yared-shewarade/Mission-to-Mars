from bs4 import BeautifulSoup
import requests
import pandas as pd
from splinter import Browser
import time
import re

def scrape():
#Scrape the NASA Mars News Site and assign to variables for later reference
    url = "https://mars.nasa.gov/news/"
    page = requests.get("https://mars.nasa.gov/news/")
    soup = BeautifulSoup(page.text, "html.parser")

#formated HTML content nicely using the prettify method on the BeautifulSoup object
    print(soup.prettify())
    html = list(soup.children)[2]
#Scrape title
    news_title = html.find("title").get_text()
    paragraphs = soup.find_all("p")
    for paragraph in paragraphs:
        new_p = paragraph.text
#set up splinter and navigate to the site
    executable_path = {'executable_path':'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)
    url_jpl = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url_jpl)
    
#etracting the current featured image   
    browser.find_by_id("full_image").click()
    featured_image_url = browser.find_by_css(".fancybox-image").first["src"]
#Mars Weather
    url_mars = "https://twitter.com/marswxreport?lang=en"
    browser.visit(url_mars)
    tweet_text = browser.find_by_css(".tweet-text")
    for tweet in tweet_text:
        if tweet.text.partition(" ")[0]=="Sol":
            mars_weather = tweet.text
            break
#Mars Facts
    url_mars_fact = "https://space-facts.com/mars/"
    browser.visit(url_mars_fact)
    tables = pd.read_html(url_mars_fact)
    df = tables[0]

    mars_df=df.set_index(0).rename(columns={1:"Value"})
    mars_df.index.names = ["Planet Profile"]

# converting to html data
    mars_facts = mars_df.to_html()
# strip unwanted newlines to clean up the table.
    mars_facts.replace('\n', '')
# with print function to make readable easily
    print(mars_facts)
#Mars Hemispheres
    url_mars_hemi = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url_mars_hemi) 
    Cerberus = browser.find_by_tag("h3")[0].text
    Schiaparelli = browser.find_by_tag("h3")[1].text
    Syrtis = browser.find_by_tag("h3")[2].text
    Valles = browser.find_by_tag("h3")[3].text
    browser.find_by_css(".thumb")[0].click()
    Cerberus_img = browser.find_by_text("Sample")["href"]
    browser.back()
    browser.find_by_css(".thumb")[1].click()
    Schiaparelli_img = browser.find_by_text("Sample")["href"]
    browser.back()
    browser.find_by_css(".thumb")[2].click()
    Syrtis_img = browser.find_by_text("Sample")["href"]
    browser.back()
    browser.find_by_css(".thumb")[3].click()
    Valles_img = browser.find_by_text("Sample")["href"]
    browser.back()
    
    hemisphere_image_urls = [
    {'title': Cerberus, 'img_url': Cerberus_img},
    {'title': Schiaparelli, 'img_url': Schiaparelli_img},
    {'title': Syrtis, 'img_url': Syrtis_img},
    {'title': Valles, 'img_url': Valles_img}
]
    hemisphere_image_urls

    mars_data = {
        "news_title": news_title,
        "news_p": new_p,
        "featured_image_url":featured_image_url,
        "mars_weather": mars_weather,
        "mars_facts":mars_facts,
        "hemisphere_image_urls":hemisphere_image_urls
    }

    return mars_data

sample_data = {
  "featured_image_url": "/spaceimages/images/mediumsize/PIA19036_ip.jpg",
  "hemisphere_image_urls": [
    {
      "img_url": "",
      "title": "Cerberus Hemisphere Enhanced"
    },
    {
      "img_url": "",
      "title": "Schiaparelli Hemisphere Enhanced"
    },
    {
      "img_url": "",
      "title": "Syrtis Major Hemisphere Enhanced"
    },
    {
      "img_url": "",
      "title": "Valles Marineris Hemisphere Enhanced"
    }
  ],
  "mars_facts_table": "",
  "mars_news": [
    {
      "title": "Click the Refresh Mars data at the top Right"
    }
  ],
  "mars_weather": "Current Mars Climate is super cold"
}
