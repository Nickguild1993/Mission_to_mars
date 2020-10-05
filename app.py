from flask import Flask, render_template
from flask_pymongo import PyMongo 
import scraping

# first line: says we'll use Flask to render a template
# second line: says we'll use PyMongo to interact w/ mongo database
# third line: says that to use the scraping code, we will convert from jupyter notebook to python

app = Flask(__name__)

# Need to tell Python how to connect to Mongo use PyMongo. 

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

# app.config["MONGO_URI"] -> tells Python that our app will connect to MONGO using a URI (uniform resource identifier)
# that is similiar to a URL.

# mongodb://localhost:27017/mars_app is the URI we'll be using to connect our app to MONGO.
# This URI is saying that the app can reach Mongo through our localhost server, using port 27017
# using a database we created -> mars_app

# SET UP APP ROUTES

# REWIND
# Flask routes bind URLS to functions. For example, the URL "ourpage.com/" 
# brings us to the homepage of our web app.
# the URL "ourpage.com/scrape" will activate our scraping code.


# DEFINE THE ROUTE FOR THE HTML PAGE.

@app.route("/")
def index():
   mars = mongo.db.mars.find_one()
   return render_template("index.html", mars=mars)

# This route: @app.route("/")   tells Flask what to display when we're looking at the 
# home page, index.html(index.html is the default HTML file that we'll use to display
# content we've scraped). 
# This means that when we visit our web app's HTML page, we will see the home page.

# within the ** def index(): ** function the following is accomplished:

# mars = mongo.db.mars.find_one() ->
#      uses PyMongo to find the "mars" collection in our database, which we will create
#      when we convert our JUPYTER scaping code to Python Script. We will also assign that
#      path to the * mars * variable for use later.

# return render_template("index.html") : tells FLASK to return an HTML template using an index.html file.

# we'll create this file after we build the FLASK routes.

#   , mars=mars) : tells Python to use the "mars" collection in MongoDB

# This function is what links our visual representation of our work, our web app, to the code that powers it.


# This next function wll set up our SCRAPING ROUTE.  This route will be the "button" of the web application-
# the one that will srape updated data when we tell it from the HOMEPAGE of our web app.  It'll be tied to a button that will
# run the code when it's clicked.

@app.route("/scrape")
def scrape():
   mars = mongo.db.mars
   mars_data = scraping.scrape_all()
   mars.update({}, mars_data, upsert=True)
   return "Scraping Successful!"

# What the above ROUTE is doing.

# The 1st line: @app.route("/scrape") -> defines the route that FLASK will be using. 
# this route, "/scrape" will run the function that we create just below it.

# the next lines allow us to access the database, scrape new data using our SCRAPING.PY script, update the database,
# and return a message when successful.

# more detail:
# we assign a new VARIABLE that points to our Mongo Database: mars = mongo.db.mars

# next, we created a new variable to hold the newly scraped data: mars_data = scraping.scrape_all()
# *** here we're referencing the * SCRAPE_ALL * function in the SCRAPING.PY file exported from Jupyter Notebook. ***

# Now that we've gathered new data (via scraping) we need to update the database using: .update() 
#                     Syntax for .update() -> .update(query_parameter, data, options)

# We're inserting data, so first we need to add an empty JSON object -> {} in place of the "query_parameter".

# Next, we'll use the data we have stored in * mars_data * in place of "data".

# finally, the OPTION we'll include is: upsert = True.  -> this indicates to Mongo to create a new document if one doesn't already
# exist, and new data will always be saved.

# Last line of function -> return "Scraping Successful" to let us know it worked!



# Now, the final bit of code we need to add -> tell Flask to run it.

if __name__ == "__main__":
   app.run()