# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import datetime as dt


def scrape_all():
    
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

    news_title, news_paragraph = mars_news(browser)

    
    data = {
      "news_title": news_title,
      "news_paragraph": news_paragraph,
      "featured_image": featured_image(browser),
      "facts": mars_facts(),
      "last_modified": dt.datetime.now(),
      "hemisphere_image_info": hemisphere_image(browser)
    }

    # Stop browser and return data
    browser.quit()
    return data


def mars_news(browser):

    # Visit the mars nasa news site
    url = 'https://redplanetscience.com'
    browser.visit(url)
    # Optional delay
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        slide_elem = news_soup.select_one('div.list_text')

        # Use the parent element to find the first `a` tag and save it as `news_title`
        news_title = slide_elem.find('div', class_='content_title').get_text()

        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
    
    except AttributeError:
        return None, None

    # return news_title and news_p from the function so they can be used outside of it
    return news_title, news_p


def featured_image(browser):
    # Scrape Featured Images JPL Space Images Featured Image
    # Visit URL
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')

    except AttributeError:
        return None

    # Use the base URL to create an absolute URL
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'
    
    return img_url


def mars_facts():
    # Add try/except for error handling
    try:
        
        # Scrape Mars Table Data: Mars Facts
        df = pd.read_html('https://galaxyfacts-mars.com')[0]
    
    except BaseException:
        return None
    
    # Assign columns and set index of dataframe
    df.columns=['description', 'Mars', 'Earth']
    df.set_index('description', inplace=True)

    # Convert dataframe into HTML format, add bootstrap
    return df.to_html(classes="table table-striped")


def hemisphere_image(browser):

    # Use browser to visit the URL
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)

    # Create a list to hold the images and titles for each hemisphere image
    hemisphere_image_urls = []

    # code to retrieve full-resolution image urls and titles for each hemisphere
    html = browser.html
    hemi_img_soup = soup(html, 'html.parser')

    # try/except for error handling
    try:
        # Find the number of pictures to scan
        images_count = len(hemi_img_soup.select("div.item"))

        # for loop over each sample picture and get the link
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
            # add extracts to the hemispheres dictionary
            hemispheres = {
                'img_url': img_url,
                'title': img_title}

            # Append hemispheres dictionary to hemisphere image urls list
            hemisphere_image_urls.append(hemispheres)

            # Return to main page
            browser.back()

    except BaseException:
        return None

    # Return the list that holds the dictionary of each image url and title
    return hemisphere_image_urls


# tell Flask that our script is complete and ready for action
if __name__ == "__main__":

    # If running as script, print scraped data
    print(scrape_all())
