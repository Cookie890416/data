from flask import Flask, render_template,jsonify
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
import json
app = Flask(__name__)
app.config['DEBUG'] = True  # 開啟 debug
app.config["JSON_AS_ASCII"] = False
mongo = PyMongo(app, uri="mongodb://localhost:27017/current")  # 開啟database
@app.route('/query/<string:event_id>')
def query_user(event_id):
    if event_id:
        users = mongo.db.current_collection.find({'event_id': event_id})
        x=[]
        if users:
            for i in users:
                i.pop("_id")
                x.append(i)
            return jsonify(x)
    else:
        return 'No user found!'
@app.route('/poster/<string:person>')
def post_data(person):
    personobj=json.loads(str(person))
    mongo.db.current_collection.insert_one(personobj)
    return str(person)

# @app.route('/insert/<string:event_id>')
# def insert_docs(event_id):
    
#     eventobj=json.loads(str(event_id))
#     print(eventobj)
#     mongo.db.current_collection.insert(eventobj)
#     return str(event_id)
    # mongo.db.current_collection.insert({
    #     "event_id": "001",
    #     "event_name":"金瓜石特快車",
    #     "status": "red",
    #     "driver_id": "ABC",
    #     "passenger_id": "XYZ",
    #     "acceptble_time_interval": ["2020/10/16 13:00", "2020/10/16 15:00"],
    #     "acceptble_start_point": ["海大校門口","新豐街","祥豐街"],
    #     "acceptble_end_point": ["九份金瓜石","九份老街","金瓜石博物館"],
    #     "acceptable_sex": "true",
    #     "max_weight": 100,
    #     "price": 50,
    #     "is_self_helmet": "true",
    #     "repeat": ["true", "true", "true", "true", "true", "true", "true"],

    #     "actual_time": "2020/10/16 13:30",
    #     "actual_start_point":"海大校門口",
    #     "actual_end_point":"九份老街",
    #     "extra_needed": "山路請慢慢騎，我不想晚七天回家QQ"})
    # return "Insert success"
@app.route('/delete/<string:event_id>')
def delete_docs(event_id):
    mongo.db.current_collection.remove({"event_id":event_id})
    return "Delete success"
@app.route('/update/<string:event_id>')
def update_docs(event_id):
    doc=mongo.db.current_collection.update(
        {"event_id" : event_id},
        {"$set":
            {"status": "green"}
        },upsert=True)
    return "Update success"
if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8080)