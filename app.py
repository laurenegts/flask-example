#from sqlalchemy.orm import sessionmaker
#from sqlalchemy import create_engine, text

#from database.SetupDB import Rat

import jinja2

from flask import Flask, request, redirect, url_for, render_template
from flask_sqlalchemy import SQLAlchemy
# Initialize Flask
app = Flask(__name__)

db = SQLAlchemy()

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://lauren:laurenpwd@capstone6.cs.kent.edu/test1?charset=utf8mb4"

db.init_app(app)

class Rat(db.Model):
    __tablename__ = 'rats'
    rat_number = db.Column(db.Integer, primary_key=True) 
    rat_name = db.Column(db.String)
    alive = db.Column(db.Boolean)
    
# routing for creating new records (the 'C' in CRUD)
@app.route("/create")
def create():
    return render_template("create.html")

@app.route("/createrat", methods = ["POST", "GET"])
def createRat():
    
    if request.method == "POST":
        # Get the data from the form and placed into a variable. 
        input_data = request.form
        
        # create a new rat and enter it into the database
        new_rat = Rat(rat_number = input_data["rat_number"], rat_name = input_data["rat_name"], alive = True)
        db.session.add(new_rat)
        db.session.commit()

        return redirect(url_for("read"))
    else:
        return redirect(url_for("create"))

# Routing for simply reading the database (the 'R' in CRUD)
@app.route("/read")
def read():
       
    # Query all results from the database
    query = db.session.execute(db.select(Rat).order_by(Rat.rat_number)).scalars()

    #print(query.all())
    # Whatever you do, do NOT run print(query.all()) before the return statement
    # that'll clear out the query variable or something, because then read.html 
    # will be blank
   
    # # render the template and pass the query into the html
    return render_template("read.html", query = query)

# Routing for editing a rat, including deletion (the 'U' and 'D' in CRUD)
#USER SEES/INTERACTS WITH THIS
@app.route("/rat/<rat_number>")
def edit(rat_number):
    
    # Query the rat based on the id
    query = db.session.query(Rat).filter(Rat.rat_number == rat_number).one()    
        
    # Render the html with the query passed through it
    return render_template("edit.html", query = query)

# Routing to actually update the rat
@app.route("/editrat/<rat_number>", methods = ["POST", "GET"])
def editRat(rat_number):
    
    if request.method == "POST":
        # Get the data from the form and placed into a variable. 
        input_data = request.form

        # Search for the rat to change based on the rat id
        query = db.session.query(Rat).filter(Rat.rat_number == rat_number).one()  
        
        # Write the changes to the database
        query.rat_number = input_data["rat_number"]
        query.rat_name = input_data["rat_name"]
        db.session.commit()
        #db.session.close()
        return redirect(url_for("read")) 
    else:
        return redirect(url_for("read"))
    
# Routing for deleting a rat
@app.route("/deleterat/<rat_number>", methods = ["POST", "GET"])
def deleteRat(rat_number):
    if request.method == "POST":
        # Search for the rat to delete based on the rat id
        query = db.session.query(Rat).filter(Rat.rat_number == rat_number).one()
        
        # Delete the row
        db.session.delete(query)
        db.session.commit()        
        return redirect(url_for("read"))
        
    else:
        return redirect(url_for("read"))

if __name__ == '__main__':
    app.run()
    
