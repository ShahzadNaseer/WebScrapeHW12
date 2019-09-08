import pandas as pd
from bs4 import BeautifulSoup as bs
import os 
import time
from splinter import Browser
from urllib.parse import urlsplit
import requests
import lxml
import html5lib


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "chromedriver"}
    return Browser("chrome", **executable_path, headless=False)


def scrape_info():
	browser = init_browser()

    # Visit visitcostarica.herokuapp.com
	news_url = 'https://mars.nasa.gov/news/'
	browser.visit(news_url)

	time.sleep(3)

    # Scrape page into Soup
	html = browser.html
	soup = bs(html,'html.parser')


	# save the latest article from nasa about mars
	news_title = soup.find('div',class_='content_title').text
	news_text = soup.find('div', class_='article_teaser_body').text
	# print(f'news_title: {news_title}')


	# print(f'news_text: {news_text}')

	img_url_featured = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
	browser.visit(img_url_featured)

	time.sleep(3)
	# https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars

	html_image = browser.html
	soup = bs(html_image, 'html.parser')

	featured_img_url = soup.find('article')['style'].replace('background-image: url(','').replace(');', '')[1:-1]
	main_url = 'https://www.jpl.nasa.gov'
	featured_image_url = main_url + featured_img_url
	featured_image_url

	# visit url to collect Mars weather
	weather_url = 'https://twitter.com/marswxreport?lang=en'
	browser.visit(weather_url)

	time.sleep(3)

	# scrape the latest weather with bs
	weather_html = browser.html
	soup = bs(weather_html, 'html.parser')
	# mars_weather = soup.find("p", class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text
	# mars_weather_all = soup.find_all("p", class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text
	mars_weather_all = soup.find_all("div", class_="js-tweet-text-container")
	# print(mars_weather_all)

	# since weather updates are unavailable, hence get whatever is last
	for tweet in mars_weather_all:
	    mars_tw = tweet.find("p", class_="TweetTextSize").text
	    if "InSight sol" in mars_tw:
	        # print(mars_tw)
	        break

	# set url where we will scrape Mars facts


	facts_url = 'http://space-facts.com/mars/'

	scrape_table = pd.read_html(facts_url)
	# scrape_table[0]
	# scrape_table[1]
	fact_table = scrape_table[1]
	fact_table.columns=['Mars-Fact','Value']
	fact_table


	html_fact_table= fact_table.to_html() 
	html_fact_table
	# print(html_fact_table)
	
	# hemispheres images
	# executable_path = {'executable_path': 'chromedriver'}
	# browser = Browser('chrome', **executable_path, headless=False)
	# set url where we will scrape hemispheres images
	base_url = 'https://astrogeology.usgs.gov'
	HemiUrl = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

	# Retrieve page with the requests module
	response = requests.get(HemiUrl)

	# create bs object and visit url
	soup = bs(response.text, 'html.parser')
	browser.visit(HemiUrl)

	# parse html with bs
	html = browser.html
	soup = bs(html, 'html.parser')

	hemi_results = soup.find_all('div', class_='item')

	# Loop through returned results
	hemi_image_urls = []


	for himage in hemi_results:
	    title = himage.find('h3').text
	    
	    # image link
	    partial_link = himage.find('a', class_='itemLink product-item')['href']
	    full_link = base_url + partial_link
	    
	    browser.visit(full_link)

	    # parse html with bsbase_url
	    html = browser.html
	    soup = bs(html, 'html.parser')
	    
	    hemi_url = base_url+soup.find('img', class_='wide-image')['src']
	    
	    hemi_image_urls.append({'title' : title,
	                            'hemi_img_url' : hemi_url })
    
	# hemi_image_urls

    # Store data in a dictionary
	mars_data = {
        "title": news_title,
        "text": news_text,
        "feature_image": featured_image_url,
        "temprature": mars_tw,
        "fact_html": html_fact_table,
        "hemi_igames": hemi_image_urls
    }

	# Close the browser after scraping
	browser.quit()

	# Return results
	return mars_data