#imports
from flask import Flask, request, session, jsonify, json
from flask_session import Session
import hashlib
import pymongo
from flaskmain.gedtojson.index import Parser
from geopy.geocoders import Nominatim
from flask_cors import CORS, cross_origin
from flask import make_response

# Setup section
parser = Parser()   # Pull parser from index.py to handle GEDCOM parsing
myclient = pymongo.MongoClient("mongodb://localhost:27017/")    # Establish connection to MongoDB
geolocator = Nominatim(user_agent="geocoding_app")  # Setup geolocator to get coordinates from city names
mydb = myclient["mydatabase"]  # Select the database
mycol = mydb["users"]  # Collection to hold user data
app = Flask(__name__)   # Initialize Flask application
app.config["SESSION_PERMANENT"] = False  # Session settings to be temporary
app.config["SESSION_TYPE"] = "filesystem"  # Store sessions in the filesystem
app.secret_key = 'dfjmfbdsnhfvsfbmds'
app.config["SESSION_COOKIE_NAME"] = "session"  # Define cookie name
app.config["SESSION_COOKIE_HTTPONLY"] = True  # Ensure cookie is only sent over HTTP and not accessible via JavaScript
app.config["SESSION_COOKIE_SECURE"] = True  # Set to True if you're using HTTPS
app.config['SESSION_COOKIE_SAMESITE'] = 'None'  # Important for cross-origin

Session(app)  # Initialize session management

allowed_origins = [
    "http://localhost:3000",  # React app running locally
    "http://localhost:4000",  # Another origin you might want to allow
    "http://localhost:5000",  # Flask app running localy

]

CORS(app, supports_credentials=True, origins=allowed_origins)



# Flask routes:
@app.route('/check_session', methods=['GET'])
def check_session():
    print("Session data:", session)  # Debugging statement
    return jsonify({"user_id": session.get("user_id")})


@app.route('/test_cookie')
def test_cookie():
    resp = make_response("Setting cookie")
    resp.set_cookie('test_cookie', 'test_value', samesite='None', secure=True)
    return resp

# Home route to check user status
@app.route("/")
def index():
    # Check if the user is logged in based on session
    if session.get("name"):
        return jsonify({'status': "Logged in"})
    return jsonify({'status': "Not logged in"})  # If no session, show not logged in message

# User registration route
@app.route("/register/<user>/<passw>", methods=["GET"])
def register(user, passw):
    if request.method == "GET":
        # Check if user already exists
        if mycol.find_one({"user": user}) == None:
            hashed_passw = hashlib.sha256(passw.encode()).hexdigest()   # Hash password before storing
            mycol.insert_one({"user": user, "password": hashed_passw})  # Insert new user into DB
            usercol = mydb[user]  # Create a user-specific collection
            return jsonify({'status': "Registration successful"})  # Return success message
    return jsonify({'status': "Registration unsuccessful"})  # Return failure message if user exists

# User login route
@app.route("/login/<user>/<passw>", methods=["GET"])
def login(user, passw):
    if request.method == "GET":
        hashed_passw = hashlib.sha256(passw.encode()).hexdigest()   # Hash the provided password for comparison
        user_data = mycol.find_one({"user": user})
        if user_data and user_data["password"] == hashed_passw:
            session["name"] = user  # Store user info in session
            return jsonify({'status': "Successfully logged in"})  # Success message
    return jsonify({'status': "Login unsuccessful"})  # Return failure message if login fails

# User logout route
@app.route("/logout")
def logout():
    session["name"] = None  # Clear session to log the user out
    return jsonify({'status': 'Logged out'})  # Return logout status

# Route to parse GEDCOM file and store data
@app.route("/parse", methods=["GET"])
def parse():
    namelist = []  # List to store parsed names
    placelist = []  # List to store parsed places
    responselist = []  # List to associate names and places
    responselistreal = []  # List to store the final results with coordinates
    coords = []  # List to store coordinates (latitude, longitude)

    # Ignore list to exclude unwanted prefixes from parsing
    ignorelist = [
        "HEAD:",
        "Ancestry.com",
        "Birth Mother",
        "Hypothesis",
        "Custom",
        "Research"
    ]
    
    # Parse the GEDCOM file using the parser
    textresponse = parser.parse_gedcom(f'server/flaskmain/gedtojson/arsonson.ged')
    
    # Extract names from the parsed text, ignoring the ones in the ignore list
    for i in textresponse.split("NAME: "):
        if not any(i.startswith(prefix) for prefix in ignorelist):
            namelist.append(i.split("/\n    GIVN:")[0].replace("/","").strip())
    
    # Get the user's collection in MongoDB
    usercol = mydb[session["name"]]

    # Extract places and find their coordinates using geolocator
    # Extract places and find their coordinates using geolocator
    for i in textresponse.split("PLAC: "):
        if not any(i.startswith(prefix) for prefix in ignorelist):
            city = i.split("\n")[0].replace("/", "")
            placelist.append(city)
            location = geolocator.geocode(city)  # Get geolocation of the city
            print(location)
            if location:
                latitude = location.latitude
                longitude = location.longitude
                # Check if the coordinates are already added to avoid duplicates
                if [latitude, longitude] not in coords:
                    coords.append([latitude, longitude, city])  # Store latitude and longitude only if new


    # Combine names and places into a response list
    for i in range(len(namelist)):
        responselist.append([namelist[i], placelist[i]])

    # Insert data into MongoDB if it doesn't already exist
    for i in range(1, len(responselist) + 1):
        if i % 2 == 0:
            if usercol.find_one({responselist[i-1][0]: responselist[i-1][1]}) == None:
                try:
                    usercol.insert_one({responselist[i-1][0]: {
                        "lat": coords[i-1][0],  # Fixing the index here
                        "lng": coords[i-1][1],  # Fixing the index here
                        "altitude": 0.2,  # Set some default altitude value
                        "color": "#00ff33",  # Set a default color for the location
                        "label": coords[i-1][2]
                    }})
                    print("hihi")
                except:
                    print("ohs nos")
                    pass

    
    # Gather all documents in the user's collection and return as the final response
    for document in usercol.find():
        responselistreal.append(document)
    
    # Save the parsed data into a JSON file
    with open("parceddata.json", "w") as f:
        json.dump(responselistreal, f, indent=2)  # Save with indentation for readability
        f.close()

    return responselistreal  # Return the parsed and stored data

# Route to fetch data (coordinates) from MongoDB
@app.route("/getdata", methods=["GET"])
def getdata():
    # Check if the session "name" exists
    if "name" not in session:
        return jsonify({"error": "Session name not found"}), 400  # Return error if session is missing
    else:
        # Continue with processing if the session is valid
        usercol = mydb[session["name"]]
        lat_lng_list = []

        # Iterate over documents and check for lat/lng values in nested dictionaries
        for document in usercol.find({}, {"_id": 0}):  # Exclude _id for cleaner output
            for value in document.values():  # Dynamically check each dictionary value
                if isinstance(value, dict) and "lat" in value and "lng" in value:
                    lat_lng_list.append({
                        "lat": value["lat"],
                        "lng": value["lng"],
                        "altitude": "0.2",  # Default altitude
                        "color": "#ffff00",  # Default color
                        "label": value["label"],
                    })

        return jsonify(lat_lng_list)  # Return the collected lat/lng data


# Start Flask application
if __name__ == "__main__":
    app.run(debug=True)  # Run the app in debug mode

