#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# 10.3.3 SCRAPE MARS DATA 


# In[ ]:


##### VERY IMPORTANT #####

# always remember to close your automated browser when you're done scraping!!!!!

# browser.quit()


# In[21]:


# import pandas for 10.3.5 

import pandas as pd


# In[ ]:


# Understanding HTML Elements and Tags 

# Most HTML elements are written with a start tag (or opening tag) and an end tag (or closing tag), 
# with content in between. 

# Elements can also contain ATTRITUBES that defines its additional properties. 
# For example, a paragraph, which is represented by the p element, would be written as:

# <p class="foo">This is a paragraph </p>

# the <p is the START TAG

# the class is the ATTRIBUTE

# the "foo" is the VALUE

# the text: This is a paragraph is the CONTENT

# </p> is the END TAG

       


# In[1]:


# Import Splinter and Beautiful Soup
from splinter import Browser
from bs4 import BeautifulSoup as soup


# In[2]:


# Path to chromedriver
get_ipython().system('which chromedriver')


# In[4]:


# Setting executable path (for MAC), then set up URL for scraping

executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
browser = Browser("chrome", **executable_path)

# recall that the ** does UNPACKING. -> passes KEYS & VALUES into browser class.


# In[5]:


# Assign the URL and instruct the browser to visit it.

url = "https://mars.nasa.gov/news/"
browser.visit(url)

# Optional delay for loading the page so we don't get locked out.
browser.is_element_present_by_css("ul.item_list li.slide", wait_time = 1)


# In[ ]:


# What the above code: browser.is_element_present_by_css("ul.item_list li.slide", wait_time = 1) DOES.

# Accomplishes two things.

# 1st -> searching ELEMENTS with a specific combination of TAG(ul & li), ATTRIBUTE(item_list & slide, respectively)
# For example: * ul.item_list * would be found in HTML as:  <ul class="item_list">

# 2nd -> telling our browser to WAIT 1 SECOND before searching for components.


# In[7]:


# SETUP the HTML parser

html = browser.html
news_soup = soup(html, "html.parser")
slide_elem = news_soup.select_one("ul.item_list li.slide")

# Assigned slide_elem as the VARIABLE to look for the <ul/> TAG and...
# its descedent (meaning: the other TAGS within the <ul /> element) the <li /> TAGS.
# this serves as our PARENT ELEMENT.  This means thatthis ELEMENT holds all the other elements within it,
# and we'll reference it when we want to FILTER search results even further.

# the "." is used for SELECTING CLASSES, such as * item_list * 
# so the code: "ul.item_list li.slide" pinpoints the <li > TAG with the CLASS of * slide * 
# and the < ul /> TAG with the CLASS of item_list

# CSS works from right to left, such as returnig the last item on the listead of the first.
# Because of this, when using * SELECT_ONE * the 1st matching element returned will be a <li />
# element with a class of SLIDE (and all nested elements within it)


# In[8]:


slide_elem

# output is the html matching what we're searching for.  begins with <li. class="slide">


# In[ ]:


# What HTML Attribute to use to scrape articles title?

# Answer: class = "content_title"

# <div class="content_title" is what the HTML ELEMENT that corresponds to TITLE for the 1st article on webpage.

# Looking for a <div /> with a CLASS of "content_title"


# In[9]:


# We'll want to assign the TITLE and SUMMARy text to variables we'll reference later.

# Begin the scraping.

slide_elem.find("div", class_= "content_title")

# what this does:

# chained .find to previously assigned variable: slide_elem
# what we say when we're doing that: " This variable holds a ton of info, so look inside of that info
# to find THIS SPECIFIC data"  Which in this case is: <div /> with a CLASS of "content_title"

# output includes the TITLE we're looking for, but it also contains extra HTML that we don't need. Need to wittle it.


# In[10]:


# Use the PARENT ELEMENT to find the first "a" tag and save it as "news_title"

# <a> tag- what is it?
# The <a> tag defines a hyperlink, which is used to link from one page to another.

# The most important attribute of the <a> element is the href attribute, which indicates the link's destination.

news_title = slide_elem.find("div", class_="content_title").get_text()
news_title

# output is simply the TITLE: "NASA's New Mars Rover Is Ready for Space Lasers"


# In[11]:


slide_elem.find("div", class_="content_title").text

# output: "NASA's New Mars Rover Is Ready for Space Lasers" 

# it's the same if you use .text or .get_text ?


# In[ ]:


# the element for the SUMMARY (on webpage)

# Element = <div class = "article_teaser_body"> 

# QUESTION: What changes to make to: slide_elem.find(“div”, class_=‘content_title’).get_text()
# in order to scrape teh SUMMARY instead of the TITLE?

# ANSWER: change the class to "article_teaser_body" 

# should look like:      slide_elem.find(“div”, class_=‘article_teaser_body’).get_text()

# REMEMBER: search for class name (in this case: "article_teaser_body") b/c
# IF THERE IS MORE THAN 1 RESULT, we have to further specify so we SCRAPE WHAT WE WANT.

# in this case however, because we want the FIRST article that populates, we don't have to specify further.
# the .find() will find the FIRST class and attribute we've specified, which works in this case.


# In[ ]:


# The two methods used to find TAGS and ATTRIBUTES with Beautiful Soup.

# 1. ) .find() -> used when we want ONLY the 1st class and attribute we've specified.

# 2. ) .find_all() -> used when we to retrieve ALL of the tags and attributes that match what we're asking for.


# In[12]:


# Use the PARENT ELEMENT to find the paragraph text

news_p = slide_elem.find("div", class_="article_teaser_body").get_text()
news_p

# output = 'Perseverance is one of a few Mars spacecraft carrying laser retroreflectors. 
#           The devices could provide new science and safer Mars landings in the future.'


# In[ ]:





# In[ ]:


#### 10.3.4 #### SCRAPE MARS DATA: FEATURED IMAGE #####


# ### Featured Images 

# In[ ]:


# Steps we need to tell Splinter to take in order to get to the full screen image

# 1. Visit webpage and click "Full Image" button

# 2. Click "more info" Button

# 3. Click on Image.


# In[13]:


# VISIT URL

url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
browser.visit(url)


# In[ ]:


# Next, want to click "Full Image" Button. This button will direct our browser to an image slideshow.

# <a /> tag - alot going on. near the end of the ATTRIBUTES in the <a /> tag is: id="full_image"

# significant b/c * id * is a UNIQUE IDENTIFIER. Means that a specific * id * can only be used 1 time per page.

# searched to confirm, yes -> full_image is UNIQUE 


# In[14]:


# find and click the "full image" button

full_image_elem = browser.find_by_id('full_image')
full_image_elem.click()

# full_image_elem -> new VARIABLE to hold the scraping result.

# full_image_elem.click() -> Splinter will "click" the image to view its full size.

# browser.find_by_id("full_image") -> the browser finds an element by its ID.


# In[ ]:


# the element for "more info" button doesn't have any unique classes and no ids at all.

# to get around this, use another useful SPLINTER functionality-> 
## the ability to search for HTML elements by text.


# In[15]:


# Find the "more info" button and click it

browser.is_element_present_by_text("more info", wait_time=1)

more_info_elem = browser.links.find_by_partial_text("more info")
more_info_elem.click()


# In[ ]:


# Breakdown of the above code to find "more info" button and click it

# 1st, code uses the:      is_element_present_by_text()     method to search for an element that has
# the PROVIDED TEXT, which in this case is "more info".  Also added the wait_time = 1 argument to allow
# the browser to fully load before we search for the element.

# that line of code will return a BOOLEAN to let us know if element is present (TRUE) or not (FALSE)

# Next, create new VARIABLE: more_info_elem 
# which we employ the browser.links.find_by_partial_text() method.
# this method will take our string: "more info" to find the link associated with the "more info" text.

# Finally, tell Splinter to click that link by chaining the .click() funciton onto our more_info_elem VARIABLE.


## ALL TOGETHER: those 3 lines check for the "more info" link using ONLY text, store a reference to the link
## to a variable, then CLICK the link.


# In[16]:


# With new page loaded in our automated browser, needs to be parsed so we can continue and scrape
# the full-size image URL.

# Prase the resulting html with soup

html = browser.html
img_soup = soup(html, "html.parser")


# In[17]:


img_soup


# In[ ]:


# Because the image will change everytime it's updated, can't just use the "src" value b/c it'll be different.

# in order to scrape the image, we need the IMAGE LINK.  -->
# The <figure /> and <a /> tags have the image link nested within them.  (stored in the <a /> tag)

#### We'll use all three of these tags (<figure />, <a />,  <img />) to build the URL to the full-size image. ####


# In[18]:


# Find the relative image URL

img_url_rel = img_soup.select_one("figure.lede a img").get("src")
img_url_rel

# Break down whats happening.

# figure.lede references the <figure /> tag and its class, lede.

# a is the next tag nested inside the <figure /> tag.

# An img tag is also nested within this HTML, so we've included that as well.

# .get("src") pulls the link to the image.

# What we've done here is tell BeautifulSoup to look 
# inside the <figure class=”lede” /> tag for an <a /> tag
# and then look within that <a /> tag for an <img /> tag. 
# Basically we're saying, "This is where the image we want lives—use the link that's inside these tags."

# output -> '/spaceimages/images/largesize/PIA19808_hires.jpg'

### THATS GREAT, BUT

### it's only a partial link- the BASE URL isn't included here. Need to add BASE URL to the code.


# In[19]:


# Add the base URL to to the partial link created from img_url_rel to make an absolute URL.

img_url = f'https://www.jpl.nasa.gove{img_url_rel}'
img_url

# output -> 'https://www.jpl.nasa.gove/spaceimages/images/largesize/PIA19808_hires.jpg'
# yay!


# In[ ]:





# In[20]:


#### 10.3.5 ##### SCRAPE MARS DATA FACTS #### 10.3.5 #####

# looking to scrape the table on the page and then import it to her webpage as is.


# In[ ]:


# All of the data we want is in a <table /> tag. HTML code used to create a table looks fairly complex, 
# but it's really just breaking down and naming each component.

#                    Tables in HTML are basically just made up of many smaller containers.

# the main container is the <table /> TAG. Inside the table is <tbody />,
# which is the BODY of the table, comprised of: headers, columns, and rows.

# <tr /> is the TAG for each table row. WITHIN that tag,
# the table data is stored in <td /> TAGS. this is where the columsn are established.

# example from webpage -> # <tr class="row-1 odd"><  


# WHAT WE"RE GONNA DO: 
#                            Instead of scraping each row, or the data in each <td />, 
#                      we're going to scrape the ** ENTIRE TABLE ** with Pandas' .read_html() function.


# In[22]:


# using .read_html() function.

df = pd.read_html("http://space-facts.com/mars/")[0]
df.columns=["description", "value"]
df.set_index("description",inplace=True)
df

# Breakdown of the above code.

# df = pd.read_html('http://space-facts.com/mars/')[0] 

# With this line, we're creating a new DataFrame from the HTML table. 
# The Pandas function ** read_html() ** specifically searches for and returns
# a list of tables found in the HTML. By specifying an index of 0, 
# we're telling Pandas to pull only the first table it encounters, 
# or the first item in the list. Then, it turns the table into a DataFrame.


# df.columns=['description', 'value'] 

# Here, we assign columns to the new DataFrame for additional clarity.


# df.set_index('description', inplace=True) 

# By using the .set_index() function, we're turning the "Description" column into the DataFrame's index. 
# inplace=True means that the updated index will remain in place, 
# WITHOUT having to reassign the DataFrame to a new variable.

# output is VERY CLEAN, VERY SLICK dataframe!


# In[23]:


# Converting the DataFrame back into HTML so we can put it on the webpage.

# USING THE .to_html() function. 

df.to_html()

# we'll be able to add this exact block of code to the website and it'll populate with what we want.


# In[24]:


##### VERY IMPORTANT #####

# always remember to close your automated browser when you're done scraping!!!!!

browser.quit()


# In[ ]:





# In[ ]:


# EXPORT TO PYTHON # 10.3.6 # 10.3.6 # 10.3.6 #

# Jupyter is great, but to fully automate the scraping process, need to convert it into a .py file!

# scroll to file -> Download as -> "Python(.py)"-> (If you get warning, click "keep" to continue download)

