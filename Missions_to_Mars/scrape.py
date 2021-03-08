# imports 
import pymongo
from bs4 import BeautifulSoup
import requests
from splinter import Browser
import pandas as pd


# Setting executable path and activating chrome browser
from webdriver_manager.chrome import ChromeDriverManager
#executable_path = {"executable_path": ChromeDriverManager().install()}

# opening a chrome browser
#browser = Browser("chrome", **executable_path, headless=False)

def scrape_all():
    executable_path = {"executable_path": ChromeDriverManager().install()}
    # opening a chrome browser
    browser = Browser("chrome", **executable_path, headless=False)

    news_title, news_p = mars_news(browser)
    featured_image_url = featured_mars_image(browser)
    mars_facts_html = mars_facts()
    hemisphere_image_urls = mars_hemispheres(browser)

    all_data = {
    "news_title": news_title,
    "news_p": news_p,
    "featured_image_url" : featured_image_url,
    "mars_facts_html": mars_facts_html,
    "hemisphere_image_urls": hemisphere_image_urls
    }
    
    browser.quit()
    return all_data



def mars_news(browser):
    # URL of page to be scraped
    url = "https://mars.nasa.gov/news/" 
    # Opening the website specified by the URL in chrome
    browser.visit(url)
    # obtaining the html code of the browser
    html = browser.html
    # Using BeautifulSoup to parse html
    soup = BeautifulSoup(html, 'html.parser')
    # first identifying the main parent section
    item_list = soup.find('ul', class_ = 'item_list')
    # now looking within for the title
    news_title = item_list.find('div', class_='content_title').text
    # now obtaining the paragraph
    # paragraph is within div class = "article_teaser_body" of item_list obtained above
    news_p = item_list.find('div', class_='article_teaser_body').text

    return news_title, news_p


def featured_mars_image(browser):
    
    url = "https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html"
    # Opening the website specified by the URL in chrome
    browser.visit(url)
    # need to navigate to the full size image begore obtaining the html
    full_image_button = browser.links.find_by_partial_text('FULL IMAGE')
    full_image_button.click()
    # obtaining the html code of the browser with the full size image
    html = browser.html
    # Using BeautifulSoup to parse html
    soup = BeautifulSoup(html, 'html.parser')
    # within this webpage the image is found at img class='fancybox-image'
    image = soup.find('img', class_='fancybox-image').attrs["src"]
    # image link needs to be added to the end of the link for the whole webpage
    featured_image_url = f"https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{image}"

    return featured_image_url


def mars_facts():
    
    # setting the url
    url = "https://space-facts.com/mars/"
    # Using read_html function in Pandas to automatically scrape any tabular data from the webpage
    table_info = pd.read_html(url)
    # Want the mars planet profile which is the first table
    mars_table = table_info[0]
    # setting column headings
    mars_table.columns = ['Description', 'Mars']
    # converting to table to html
    mars_facts_html = mars_table.to_html(index= False)

    return mars_facts_html

def mars_hemispheres(browser):
    
    # URL of page to be scraped
    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars" 
    # Opening the website specified by the URL in chrome
    browser.visit(url)
    # setting empty dictionary
    hemisphere_image_urls = []
    # navigating browser with splinter
    # the link to move to the full image is attached to both the thumbnail and the title
    # the links are within 'a' class_ = "product-item". Then the title is identified with h3
    title_links = browser.find_by_css("a.product-item h3")

    for x in range(len(title_links)):
        
        hemisphere_info = {}
        #clicking on the link
        browser.find_by_css("a.product-item h3")[x].click()
        #obtaining the html code of the browser
        html = browser.html
        #Using BeautifulSoup to parse html
        soup = BeautifulSoup(html, 'html.parser')
        # finding the section where the title is
        section = soup.find('section', class_ = "block metadata")    
        #obtaining the title
        title = section.find('h2', class_='title').text
        # setting as key value pair
        hemisphere_info["title"] = title
        # A reference to the image is contained with the 'Sample' text
        # find its section using the following
        li = soup.find('li')
        #obtaining the image link
        image_url = li.find('a').attrs['href']
        # setting as key value pair
        hemisphere_info["img_url"] = image_url
        # appending the information
        hemisphere_image_urls.append(hemisphere_info)
        # moving back to the previous browser page
        browser.visit(url)
    
    return hemisphere_image_urls



#if __name__ == "__main__":
    #scrape_all()