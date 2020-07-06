from flask import Flask
from flask_pymongo import PyMongo
import simplejson as json
from flask import request, jsonify

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://127.0.0.1:27017/firstdb"
mongo = PyMongo(app)

@app.route("/", methods=['GET'])
def home_page():
    online_users = mongo.db.books.find({})
    user_list = list(online_users)
    for user in user_list:
        try:
            del user["_id"]
        except KeyError:
            print("user 'testing' not found")
    print(user_list)
    j  = json.dumps(user_list)
    return j

@app.route('/books', methods=['GET'])
def api_id():

    if 'id' in request.args:
        id = int(request.args['id'])
    else:
        return "Error: No id field provided. Please specify an id."


    online_users = mongo.db.books.find({"id": {"$in":[ id ]}})
    user_list = list(online_users)
    for user in user_list:
        try:
            del user["_id"]
        except KeyError:
            print("user 'testing' not found")
    print(user_list)
    j1 = []
		
    # Loop through the data and match results that fit the requested ID.
    # IDs are unique, but other fields might return many results
    for book in user_list:
        if book['id'] == id:
            j1.append(book)

    # Use the jsonify function from Flask to convert our list of
    # Python dictionaries to the JSON format.
    return jsonify(j1)

app.run()
