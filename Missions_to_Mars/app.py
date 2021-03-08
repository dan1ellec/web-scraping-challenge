from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
# importing scrape.py
import scrape

# Create an instance of Flask
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
#mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")

app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

# Route to render index.html template using data from Mongo
@app.route("/")
def home():

    # Find one record of data from the mongo database
    mar_data = mongo.db.mar_data.find_one()

    # Return template and data
    return render_template("index.html", data_mars = mar_data)


# Route that will trigger the scrape function
@app.route("/scrape")
def scrape_all():

    # Calling the file (scrape) and the scrape function in that file (scrape_all)
    mars_data = scrape.scrape_all()

    # Update the Mongo database using update and upsert=True
    mongo.db.mar_data.update({}, mars_data, upsert=True)

    # Redirect back to home page
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
