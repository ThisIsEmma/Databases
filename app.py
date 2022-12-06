from flask import Flask, request, redirect, render_template, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

############################################################
# SETUP
############################################################

app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://localhost:27017/plantsDatabase"
mongo = PyMongo(app)

############################################################
# ROUTES
############################################################

@app.route('/')
def plants_list():
    """Display the plants list page."""

    # TODO: Replace the following line with a database call to retrieve *all*
    # plants from the Mongo database's `plants` collection.
    plants_data = mongo.db.plants.find()
    '''
    R - read:

    result = mongo.db.[collections name].find()  <= return an array of the result. When the parentheses are empty it will return everything 
    for item in result:
        print(item.['first_name'])
    '''
    context = {
        'plants': plants_data,
    }
    return render_template('plants_list.html', **context)

@app.route('/about')
def about():
    """Display the about page."""
    return render_template('about.html')

@app.route('/create', methods=['GET', 'POST'])
def create():
    """Display the plant creation page & process data from the creation form."""
    if request.method == 'POST':
        # TODO: Get the new plant's name, variety, photo, & date planted, and 
        # store them in the object below.
        new_plant = {
            'name': request.form.get('plant_name'),
            'variety': request.form.get('variety'),
            'photo_url': request.form.get('photo'),
            'date_planted': request.form.get('date_planted')
        }
        # TODO: Make an `insert_one` database call to insert the object into the
        # database's `plants` collection, and get its inserted id. Pass the 
        # inserted id into the redirect call below.
        mongo.db.plants.insert_one(new_plant)
        return redirect(url_for('detail', plant_id= new_plant['_id']))

    else:
        return render_template('create.html')

@app.route('/plant/<plant_id>')
def detail(plant_id):
    """Display the plant detail page & process data from the harvest form."""

    # TODO: Replace the following line with a database call to retrieve *one*
    # plant from the database, whose id matches the id passed in via the URL.
   
    search_param = { '_id' : ObjectId(plant_id) }
    plant_to_show = mongo.db.plants.find_one(search_param)

    # TODO: Use the `find` database operation to find all harvests for the
    # plant's id.
    # HINT: This query should be on the `harvests` collection, not the `plants`
    # collection.
    harvests = mongo.db.harvests.find()
 
    context = {
        'plant' : plant_to_show,
        'harvests': harvests,
        'id': plant_id,
    }
    return render_template('detail.html', **context)

@app.route('/harvest/<plant_id>', methods=['POST'])
def harvest(plant_id):
    """
    Accepts a POST request with data for 1 harvest and inserts into database.
    """

    # TODO: Create a new harvest object by passing in the form data from the
    # detail page form.
    new_harvest = {
        'quantity': request.form.get('harvested_amount'), # e.g. '3 tomatoes'
        'date': request.form.get('date_planted'),
        'plant_id': plant_id,
    }

    # TODO: Make an `insert_one` database call to insert the object into the 
    # `harvests` collection of the database.
    mongo.db.harvests.insert_one(new_harvest) 
    return redirect(url_for('detail', plant_id=plant_id))

@app.route('/edit/<plant_id>', methods=['GET', 'POST'])
def edit(plant_id):
    """Shows the edit page and accepts a POST request with edited data."""
    if request.method == 'POST':
        # TODO: Make an `update_one` database call to update the plant with the
        # given id. Make sure to put the updated fields in the `$set` object.
        
        plant_name = request.form.get('plant_name')
        variety = request.form.get('variety')
        photo = request.form.get('photo')
        date_planted = request.form.get('date_planted')
        
        search_params = {'_id' : ObjectId(plant_id)}
        change_param = {'$set': {
            'name' : plant_name,
            'variety' : variety,
            'photo_url' : photo,
            'date_planted' : date_planted,
        }}

        mongo.db.plants.update_one(search_params, change_param)
        return redirect(url_for('detail', plant_id=plant_id))
    else:
        # TODO: Make a `find_one` database call to get the plant object with the
        # passed-in _id.
        search_param = { '_id':ObjectId(plant_id) }
        plant_to_show = mongo.db.plants.find_one(search_param)

        context = {
            'plant': plant_to_show
        }

        return render_template('edit.html', **context)

@app.route('/delete/<plant_id>', methods=['POST'])
def delete(plant_id):
    # TODO: Make a `delete_one` database call to delete the plant with the given
    # id.

    search_param = { '_id':ObjectId(plant_id) }
    mongo.db.plants.delete_one(search_param)

    # TODO: Also, make a `delete_many` database call to delete all harvests with
    # the given plant id.
    mongo.db.plants.delete_many(search_param)

    return redirect(url_for('plants_list'))

if __name__ == '__main__':
    app.run(debug=True)
