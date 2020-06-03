from splinter import Browser
from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
import time


def scrape():
    py_dict = {}
# %%
# URL of page to be scraped
    url = 'https://mars.nasa.gov/news/'


# %%
# Retrieve page with the requests module
    response = requests.get(url)


# %%
# Create a Beautiful Soup object
    soup = bs(response.text, 'html.parser')
# type(soup)


# %%
# Print formatted version of the soup
# print(soup.prettify())


# %%
# Extract the title of the HTML document
    news_title = soup.title.text.strip()
    py_dict['news_title'] = news_title
    # print(news_title)


# %%
# Extract the text of the title
    news_p = soup.body.find('p').text
    py_dict['news_p'] = news_p
    # print(news_p)


# %%
    executable_path = {'executable_path': 'chromedriver.exe'}
    with Browser('chrome', **executable_path, headless=False) as browser:
        url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
        browser.visit(url)
        browser.links.find_by_partial_text('FULL IMAGE').click()
        time.sleep(1)
        html = browser.html
        soup = bs(html, 'html.parser')
        featured_image_url = 'http://www.jpl.nasa.gov' + soup.find(class_='fancybox-image')['src']
        py_dict['featured_image_url'] = featured_image_url


# %%
    # executable_path = {'executable_path': 'chromedriver.exe'}
    with Browser('chrome', **executable_path, headless=False) as browser:
        # browser = Browser('chrome', **executable_path, headless=False)
        url = 'https://twitter.com/marswxreport?lang=en'
        browser.visit(url)
        time.sleep(1)
        html = browser.html
        soup = bs(html, 'html.parser')
        divs = soup.select('div.css-901oao.r-jwli3a.r-1qd0xha.r-a023e6.r-16dba41.r-ad9z0x.r-bcqeeo.r-bnwqim.r-qvutc0')
        mars_weather = divs[0].text
        py_dict['mars_weather'] = mars_weather
        # print(mars_weather)


# %%
    url = 'https://space-facts.com/mars/'
    tables = pd.read_html(url)
    # tables


# %%
    table = tables[0]
    table = table.set_index(0, inplace=True)
    table = tables[0]
    # table


# %%
    html_table = table.to_html(header = False, index_names = False)
    # html_table


# %%
    html_table = html_table.replace('\n', '')
    py_dict['html_table'] = html_table
    # html_table


# %%
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    with Browser('chrome', **executable_path, headless=False) as browser:
        # browser = Browser('chrome', **executable_path, headless=False)
        browser.visit(url)
        hemisphere_image_urls = []
        
        for i in range(4):
            links = browser.find_by_css('img.thumb')
            links[i].click()
            title_arr = browser.title.split(' ')
            title = ""
            for word in title_arr:
                if word == "Hemisphere":
                    title = title + word
                    break
                else:
                    title = title + word + " "
            browser.links.find_by_partial_text('Sample').click()
            time.sleep(3)
            browser.windows.current = browser.windows[1]
            html = browser.html
            soup = bs(html, 'html.parser')
            img_url = soup.img['src']
            browser.windows.current = browser.windows[0]
            browser.windows[1].close()
            browser.back()
            hemisphere_image_urls.append({"title": title, "img_url": img_url})

        py_dict['hemisphere_image_urls'] = hemisphere_image_urls
    return py_dict
# %%
    # hemisphere_image_urls

# print(scrape())