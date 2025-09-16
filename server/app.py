# server/app.py

from flask import Flask, jsonify
from flask_migrate import Migrate
from models import db, Earthquake

# Create Flask app
app = Flask(__name__)

# Configure database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize extensions
db.init_app(app)
migrate = Migrate(app, db)


# ----------------------
# Routes
# ----------------------

# Get earthquake by ID
@app.route("/earthquakes/<int:id>")
def get_earthquake(id):
    quake = Earthquake.query.filter_by(id=id).first()
    if quake:
        return jsonify(quake.to_dict()), 200
    else:
        return jsonify({"message": f"Earthquake {id} not found."}), 404


# Get earthquakes by minimum magnitude
@app.route("/earthquakes/magnitude/<float:magnitude>")
def get_quakes_by_magnitude(magnitude):
    quakes = Earthquake.query.filter(Earthquake.magnitude >= magnitude).all()
    return jsonify({
        "count": len(quakes),
        "quakes": [q.to_dict() for q in quakes]
    }), 200


# Run the app
if __name__ == "__main__":
    app.run(port=5555, debug=True)
