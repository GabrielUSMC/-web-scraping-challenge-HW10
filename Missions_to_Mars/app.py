# import necessary libraries
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# create instance of Flask app
app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

# # Create connection variable
# conn = 'mongodb://localhost:27017'

# # Pass connection to the pymongo instance.
# client = pymongo.MongoClient(conn)

# # Connect to a database. Will create one if not already available.
# db = client.mars_db

# # Drops collection if available to remove duplicates
# db.mars_data.drop()
# create route that scrapes
@app.route("/scrape")
def scraper():
    # return render_template("index.html", text="Serving up cool text from the Flask server!!")
    mongo.db.mars.drop()
    listings = mongo.db.mars
    mars_data = scrape_mars.scrape()
    listings.update({}, mars_data, upsert=True)
    return redirect("/", code=302)
    # db.mars_data.insert(scrape())


# create route that renders index.html template
@app.route("/")
def index():
    listings = mongo.db.mars.find_one()
    return render_template("index.html", listings = listings)

if __name__ == "__main__":
    app.run(debug=True)
