#Import dependencies and setup
from bs4 import BeautifulSoup as bs
from splinter import Browser
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager



def scrape():
    
    #Chrome driver setup
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    #======= Mars News =======#
    #Visit the Mars News Site
    url = "https://redplanetscience.com/"
    browser.visit(url)

    #Scrape page into Soup
    html = browser.html
    news_soup = bs(html, "html.parser")
    slide_element = news_soup.select_one("div.list_text")

    news_title = slide_element.find("div", class_="content_title").get_text()
    news_p = slide_element.find("div", class_="article_teaser_body").get_text()

    #======= Featured Space Images =======#
    #Visit Featured Space Images
    url = "https://spaceimages-mars.com/"
    browser.visit(url)

    #Splinter to find image url
    featured_image_url = browser.find_by_tag('img[class="headerimage fade-in"]')._element.get_attribute('src')

    #======= Mars Facts =======#
    #Mars facts HTML to Table
    mars_facts = pd.read_html("https://galaxyfacts-mars.com/")[0]
    mars_facts.columns=["Description", "Mars", "Earth"]
    mars_facts = mars_facts.set_index('Description')
    mars_facts = mars_facts.to_html(header=False, index=False)

    #======= Hemisphere of Mars =======#
    #Visit astrogeology site
    url = "https://marshemispheres.com/"
    browser.visit(url)
    hemisphere_image_urls = []

    # Get a list of all the Hemispheres
    html = browser.html
    soup = bs(html, 'html.parser')
    links = browser.find_by_css('.item h3')

    for item in range(len(links)):
        hemisphere = {}
        
        # Find css element on each loop
        browser.find_by_css(".item h3")[item].click()
        
        # Find sample & extract href
        sample_element = browser.find_link_by_text("Sample").first
        hemisphere["img_url"] = sample_element["href"]
        
        # Get hemisphere title
        hemisphere["title"] = browser.find_by_css("h2.title").text
        
        # Append hemisphere dict to List
        hemisphere_image_urls.append(hemisphere)
        
        # Navigate Backwards
        browser.back()
        
    #======= Mars Data Dictionary =======#
    # Store data in dictionary
    mars_data = {
        'news_title': news_title,
        'news_p': news_p,
        'featured_image_url': featured_image_url,
        'mars_facts': mars_facts,
        'hemisphere_image_urls' : hemisphere_image_urls
    }


    # Close the browser after scraping
    browser.quit()

    # Return results
    return mars_data
