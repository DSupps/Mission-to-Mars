#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Import Splinter and BeautifulSoup and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd


# In[2]:


# Set Up Splinter

executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# In[3]:


# Visit the mars nasa news site
url = 'https://redplanetscience.com'
browser.visit(url)

# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)


# In[4]:


# Convert 

html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('div.list_text')


# In[5]:


# Let's begin our scraping

slide_elem.find('div', class_='content_title')


# In[6]:


# Use the parent element to find the first `a` tag and save it as `news_title`
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title


# In[7]:


# Use the parent element to find the paragraph text

news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p


# In[8]:


### 10.3.4 - Scrape Mars Data: Featured


# ### Featured Images

# In[9]:


# Visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)


# In[10]:


# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()


# In[11]:


# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')

# Find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel


# In[12]:


# Use the base URL to create an absolute URL
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url


# ### 10.3.5 - Scrape Mars Data: Mars Facts

# In[13]:


#import pandas as pd

df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.columns=['description', 'Mars', 'Earth']
df.set_index('description', inplace=True)
df


# In[14]:


# need to convert dataframe back to HTML so that it can put on a webapage

df.to_html()


# ## D1: Scrape High - Resolution Mars' Hemisphere Images and Titles

# ### Hemispheres

# In[15]:


# 1. Use browser to visit the URL 
url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

browser.visit(url)


# In[16]:


# 2. Create a list to hold the images and titles for each hemisphere image.
hemisphere_image_urls = []

# 3. Write code to retrieve full-resolution image urls and titles for each hemisphere.
html = browser.html
hemi_img_soup = soup(html, 'html.parser')

images_count = len(hemi_img_soup.select("div.item"))

# for loop over each sample picture and get the link
# four images of mars hemispheres
for i in range(images_count):
   
    # Create an empty dictionary to hold the search results
    hemispheres = {}
    # Find link to image and click it and get the href
    link_image = hemi_img_soup.select("div.description a")[i].get('href')
    browser.visit(f'https://astrogeology.usgs.gov/{link_image}')
   
    # Parse the new html page
    html = browser.html
    sample_image_soup = soup(html, 'html.parser')
    # Get the full image link
    img_url = sample_image_soup.select_one("div.downloads ul li a").get('href')
    # Get the full image title
    img_title = sample_image_soup.select_one("h2.title").get_text()
    # Add extracts to the hemispheres dict
    hemispheres = {
        'img_url': img_url,
        'title': img_title}
   
    # Append hemispheres dict to hemisphere image urls list
    hemisphere_image_urls.append(hemispheres)
   
    # Return to main page
    browser.back()


# In[17]:


# 4. Print the list that holds the dictionary of each full-resolution image url and title.
hemisphere_image_urls


# In[18]:


# 5. Quit the browser
browser.quit()

