# travel_planner.py
import os
import datetime
import pytz
from fpdf import FPDF
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
from flask_mail import Mail, Message
from flask_apscheduler import APScheduler
from travel_api import TravelAPI
from local_api import LocalAPI
from pdf_generator import PDFGenerator

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///travel_planner.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'super-secret'  # Change this!
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'your-email@gmail.com'
app.config['MAIL_PASSWORD'] = 'your-password'

db = SQLAlchemy(app)
ma = Marshmallow(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)
mail = Mail(app)
scheduler = APScheduler()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    itineraries = db.relationship('Itinerary', backref='user', lazy=True)

class Itinerary(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    destinations = db.relationship('Destination', backref='itinerary', lazy=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class Destination(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    flights = db.relationship('Flight', backref='destination', lazy=True)
    hotels = db.relationship('Hotel', backref='destination', lazy=True)
    activities = db.relationship('Activity', backref='destination', lazy=True)
    itinerary_id = db.Column(db.Integer, db.ForeignKey('itinerary.id'), nullable=False)

class Flight(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    departure = db.Column(db.DateTime, nullable=False)
    arrival = db.Column(db.DateTime, nullable=False)
    destination_id = db.Column(db.Integer, db.ForeignKey('destination.id'), nullable=False)

class Hotel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(100), nullable=False)
    destination_id = db.Column(db.Integer, db.ForeignKey('destination.id'), nullable=False)

class Activity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(100), nullable=False)
    destination_id = db.Column(db.Integer, db.ForeignKey('destination.id'), nullable=False)

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User

class ItinerarySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Itinerary

class DestinationSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Destination

class FlightSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Flight

class HotelSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Hotel

class ActivitySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Activity

user_schema = UserSchema()
itinerary_schema = ItinerarySchema()
destination_schema = DestinationSchema()
flight_schema = FlightSchema()
hotel_schema = HotelSchema()
activity_schema = ActivitySchema()

def create_tables():
    with app.app_context():
        db.create_all()

def add_user(username, password):
    user = User(username=username, password=bcrypt.generate_password_hash(password).decode('utf-8'))
    db.session.add(user)
    db.session.commit()

def add_itinerary(name, user_id):
    itinerary = Itinerary(name=name, user_id=user_id)
    db.session.add(itinerary)
    db.session.commit()

def add_destination(name, itinerary_id):
    destination = Destination(name=name, itinerary_id=itinerary_id)
    db.session.add(destination)
    db.session.commit()

def add_flight(departure, arrival, destination_id):
    flight = Flight(departure=departure, arrival=arrival, destination_id=destination_id)
    db.session.add(flight)
    db.session.commit()

def add_hotel(name, address, destination_id):
    hotel = Hotel(name=name, address=address, destination_id=destination_id)
    db.session.add(hotel)
    db.session.commit()

def add_activity(name, description, destination_id):
    activity = Activity(name=name, description=description, destination_id=destination_id)
    db.session.add(activity)
    db.session.commit()

def generate_pdf(itinerary_id):
    itinerary = Itinerary.query.get(itinerary_id)
    pdf = PDFGenerator()
    pdf.add_page()
    pdf.set_font('Arial', '', 12)
    pdf.cell(0, 10, 'Itinerary for ' + itinerary.name, 0, 1, 'L')
    for destination in itinerary.destinations:
        pdf.cell(0, 10, 'Destination: ' + destination.name, 0, 1, 'L')
        for flight in destination.flights:
            pdf.cell(0, 10, 'Flight: ' + str(flight.departure) + ' - ' + str(flight.arrival), 0, 1, 'L')
        for hotel in destination.hotels:
            pdf.cell(0, 10, 'Hotel: ' + hotel.name + ' - ' + hotel.address, 0, 1, 'L')
        for activity in destination.activities:
            pdf.cell(0, 10, 'Activity: ' + activity.name + ' - ' + activity.description, 0, 1, 'L')
    pdf.output('itinerary.pdf')

def send_notification(subject, message):
    msg = Message(subject, sender='your-email@gmail.com', recipients=['recipient-email@gmail.com'])
    msg.body = message
    mail.send(msg)

def update_flight_status(flight_id, status):
    flight = Flight.query.get(flight_id)
    flight.status = status
    db.session.commit()

def update_weather(weather):
    weather_data = WeatherData.query.get(1)
    weather_data.weather = weather
    db.session.commit()

def update_local_events(events):
    local_events_data = LocalEventsData.query.get(1)
    local_events_data.events = events
    db.session.commit()

class TravelAPI:
    def __init__(self):
        self.api_key = 'your-api-key'

    def get_flight_info(self, departure, arrival):
        url = 'https://api.example.com/flights'
        params = {'departure': departure, 'arrival': arrival}
        response = requests.get(url, params=params, headers={'Authorization': 'Bearer ' + self.api_key})
        return response.json()

class LocalAPI:
    def __init__(self):
        self.api_key = 'your-api-key'

    def get_weather(self, location):
        url = 'https://api.example.com/weather'
        params = {'location': location}
        response = requests.get(url, params=params, headers={'Authorization': 'Bearer ' + self.api_key})
        return response.json()

class PDFGenerator:
    def __init__(self):
        self.pdf = FPDF()

    def add_page(self):
        self.pdf.add_page()

    def set_font(self, font, style, size):
        self.pdf.set_font(font, style, size)

    def cell(self, width, height, text, border=0, ln=True, align='L', fill=False):
        self.pdf.cell(width, height, text, border, ln, align, fill)

    def output(self, filename):
        self.pdf.output(filename)

class WeatherData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    weather = db.Column(db.String(100), nullable=False)

class LocalEventsData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    events = db.Column(db.String(100), nullable=False)

def create_travel_api():
    api = TravelAPI()
    return api

def create_local_api():
    api = LocalAPI()
    return api

def create_pdf_generator():
    generator = PDFGenerator()
    return generator

def create_weather_data():
    data = WeatherData(weather='Sunny')
    db.session.add(data)
    db.session.commit()

def create_local_events_data():
    data = LocalEventsData(events='Concert')
    db.session.add(data)
    db.session.commit()

def update_travel_api(api):
    api.get_flight_info('New York', 'Los Angeles')

def update_local_api(api):
    api.get_weather('New York')

def update_pdf_generator(generator):
    generator.add_page()
    generator.set_font('Arial', '', 12)
    generator.cell(0, 10, 'Itinerary', 0, 1, 'L')

def update_weather_data(data):
    data.weather = 'Rainy'
    db.session.commit()

def update_local_events_data(data):
    data.events = 'Festival'
    db.session.commit()

def run_scheduler():
    scheduler.add_job(update_travel_api, 'interval', minutes=1, args=[create_travel_api()])
    scheduler.add_job(update_local_api, 'interval', minutes=1, args=[create_local_api()])
    scheduler.add_job(update_pdf_generator, 'interval', minutes=1, args=[create_pdf_generator()])
    scheduler.add_job(update_weather_data, 'interval', minutes=1, args=[create_weather_data()])
    scheduler.add_job(update_local_events_data, 'interval', minutes=1, args=[create_local_events_data()])
    scheduler.start()

if __name__ == '__main__':
    create_tables()
    add_user('admin', 'password')
    add_itinerary('Test Itinerary', 1)
    add_destination('Test Destination', 1)
    add_flight(datetime.datetime.now(pytz.utc), datetime.datetime.now(pytz.utc) + datetime.timedelta(hours=1), 1)
    add_hotel('Test Hotel', 'Test Address', 1)
    add_activity('Test Activity', 'Test Description', 1)
    generate_pdf(1)
    send_notification('Test Notification', 'Test Message')
    update_flight_status(1, 'Delayed')
    update_weather('Rainy')
    update_local_events('Festival')
    run_scheduler()
    app.run(debug=True)