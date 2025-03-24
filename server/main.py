#imports
from flask import Flask, request, session, jsonify, json
from flask_session import Session
import hashlib
import pymongo
from flaskmain.gedtojson.index import Parser
from geopy.geocoders import Nominatim


#Setup
parser = Parser()   #pull from index.py
myclient = pymongo.MongoClient("mongodb://localhost:27017/")    #start MongoDB
geolocator = Nominatim(user_agent="geocoding_app")
mydb = myclient["mydatabase"]
mycol = mydb["users"]
app = Flask(__name__)   #start Flask
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

#test user
mycol.insert_one({"avi": "8f434346648f6b96df89dda901c5176b10a6d83961dd3c1ac88b59b2dc327aa4"})


#flask:

#status
@app.route("/")
def index():
    if session.get("name"):
        return jsonify({'status': f"Logged in as {session.get('name')}"})
    return jsonify({'status': "Not logged in"})

#register
@app.route("/register/<user>/<passw>", methods=["GET"])
def register(user, passw):
    if request.method == "GET":
        if mycol.find_one({"user": user}) == None:  #if user doesent have a match in db
            hashed_passw = hashlib.sha256(passw.encode()).hexdigest()   #hash pass
            mycol.insert_one({ "user": user, "password": hashed_passw})
            usercol = mydb[user]
            return jsonify({'status': "Registration successful"})   #if succeed
    return jsonify({'status': "Registration unsuccessful"}) #if fail

#login
@app.route("/login/<user>/<passw>", methods=["GET"])
def login(user, passw):
    if request.method == "GET":
        hashed_passw = hashlib.sha256(passw.encode()).hexdigest()   #hash pass
        print(mycol.find_one({"user": user}))
        if mycol.find_one({"user": user})["password"] == hashed_passw:  #compared hashed pass to stored
            session["name"] = user
            return jsonify({'status': "Successfully logged in"})    #if succeed
    return jsonify({'status': "Login unsuccessful"})    #if fail

#logout
@app.route("/logout")
def logout():
    session["name"] = None  #break session
    return jsonify({'status': 'Logged out'})

@app.route("/parse", methods=["GET"])
def parse():
    namelist = []
    placelist = []
    responselist = []
    responselistreal = []
    coords = []

    ignorelist = [
        "HEAD:",
        "Ancestry.com",
        "Birth Mother",
        "Hypothesis",
        "Custom",
        "Research"
    ]
    textresponse = parser.parse_gedcom(f'./flaskmain/gedtojson/{session["name"]}.ged')
    for i in textresponse.split("NAME: "):
        if not any(i.startswith(prefix) for prefix in ignorelist):
            namelist.append(i.split("/\n    GIVN:")[0].replace("/","").strip())
    
    usercol = mydb[session["name"]]

    for i in textresponse.split("PLAC: "):
        if not any(i.startswith(prefix) for prefix in ignorelist):
            city = i.split("\n")[0].replace("/","")
            placelist.append(city)
            location = geolocator.geocode(city)
            if location:
                latitude = location.latitude
                longitude = location.longitude
                print(f"Latitude: {latitude}, Longitude: {longitude}")
                coords.append([latitude,latitude])
    for i in range(len(namelist)):
        responselist.append([namelist[i],placelist[i]])

    for i in range(1, len(responselist)+1):
        if i % 2 == 0:
            if usercol.find_one({responselist[i-1][0]: responselist[i-1][1]}) == None:
                usercol.insert_one({responselist[i-1][0]: {
                    "city": responselist[i-1][1],
                    "lat": coords[i][0],
                    "lng": coords[i][1]
                    
                    }
                })
    for document in usercol.find():
        responselistreal.append(document)
    
    print(responselistreal)

    with open("tohaim.json", "w") as f:
        json.dump(responselistreal, f, indent=2)
        f.close

    return responselistreal

 

#run
if __name__ == "__main__":
    app.run(debug=True)


