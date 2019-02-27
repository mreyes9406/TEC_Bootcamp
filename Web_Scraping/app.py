from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

@app.route("/")
def index():
    mars_info_dict = mongo.db.mars_info_dict.find_one()
    return render_template("index.html", mars_info_dict=mars_info_dict)

@app.route("/scrape")
def scrape_website():
    mars_info_dict = mongo.db.mars_info_dict
    mars_info_dict_data= scrape_mars.scrape()
    mars_info_dict.update({}, mars_info_dict_data, upsert=True)
    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)

