def scrape():
    # Import dependencies
    from bs4 import BeautifulSoup as bs
    from splinter import Browser
    import pandas as pd

    # Start splinter
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)

    # Visit NASA Mars News
    nasa_url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(nasa_url)

    # Scrape NASA Latest Mars News
    html = browser.html
    soup = bs(html, 'html.parser')
    latest_news_title = soup.find_all('div', class_='content_title')[0].text
    latest_news_teaser = soup.find_all('div', class_='article_teaser_body')[0].text

    # Visit JPL Mars Space Images
    jpl_mars_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(jpl_mars_url)

    # Scrape JPL Mars Space Images
    html = browser.html
    soup = bs(html, 'html.parser')
    feat_img_path = soup.find_all('a', class_='button fancybox')[0]['data-fancybox-href']
    feat_img_url = 'https://www.jpl.nasa.gov' + feat_img_path

    # Visit Mars Weather Twitter Account
    mars_weather_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(mars_weather_url)

    # Scrape Mars Weather Twitter Account
    html = browser.html
    soup = bs(html, 'html.parser')
    mars_weather = soup.find_all('p', class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text")[0].text

    # Visit Mars Facts Website
    mars_facts_url = 'https://space-facts.com/mars/'
    browser.visit(mars_facts_url)

    # Scrape Mars Weather Twitter Account
    html = browser.html
    soup = bs(html, 'html.parser')
    facts_table = soup.find_all('table')
    facts_df = pd.read_html(str(facts_table))[0]
    facts_dict = {row[0]:row[1] for row in facts_df.itertuples(index=False)}

    # Visit USGS Astrogeology for Martian hempsphere HD pictures
    mars_hemi_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    base_url = 'https://astrogeology.usgs.gov'
    browser.visit(mars_hemi_url)

    # Get HD images
    html = browser.html
    soup = bs(html, 'html.parser')
    items = soup.find_all('div', class_='item')
    button_texts = [item.h3.text for item in items]
    hems_url = []

    for button_text in button_texts:   
        # Retrieve URL
        browser.click_link_by_partial_text(button_text)
        html = browser.html
        soup = bs(html, 'html.parser')
        img_url = soup.find_all('img', class_='wide-image')[0]['src']
        hem_url = base_url + img_url
    
        # Retrieve image title
        img_data = {}
        title = soup.find_all('h2', class_='title')[0].text
        img_data['title'] = title
        img_data['img_url'] = hem_url
        hems_url.append(img_data)
        browser.click_link_by_partial_text('Back')

    mars_info_dict = {}
    mars_info_dict['latest_news_title'] = latest_news_title
    mars_info_dict['latest_news_teaser'] = latest_news_teaser
    mars_info_dict['feat_img_url'] = feat_img_url
    mars_info_dict['mars_weather'] = mars_weather
    mars_info_dict['mars_facts'] = facts_dict
    mars_info_dict['hemispheres_url'] = hems_url


    return mars_info_dict

    