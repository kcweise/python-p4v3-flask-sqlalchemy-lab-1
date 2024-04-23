# server/app.py
#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate

from models import db, Earthquake
#instance of Flask api
app = Flask(__name__)
#connstion to SQLALCHEMY ORM database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)


@app.route('/')
def index():
    body = {'message': 'Flask SQLAlchemy Lab 1'}
    return make_response(body, 200)

@app.route('/earthquakes/<int:id>')
def eq_by_id(id):
    eq = Earthquake.query.filter_by(id = id).first()
    if eq:
        body = { 'id':eq.id,
                'location':eq.location,
                'magnitude': eq.magnitude,
                'year': eq.year}
        status = 200
    else:
        body = {'message': f'Earthquake {id} not found.'}
        status = 404
        
    return make_response(body, status)

@app.route('/earthquakes/magnitude/<float:magnitude>')
def by_magnitude(magnitude):
    eq_list = []
    for eq in Earthquake.query.filter(Earthquake.magnitude >= magnitude).all():
        
        eq_dict = {
            "id": eq.id,
            "location": eq.location,
            "magnitude": eq.magnitude,
            "year": eq.year}
        eq_list.append(eq_dict)
        
    body = {'count': len(eq_list),
            'quakes': eq_list}         
        
    status = 200
    return make_response(jsonify(body), status)
    


if __name__ == '__main__':
    app.run(port=5555, debug=True)
