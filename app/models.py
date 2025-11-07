from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db, login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(UserMixin, db.Model):
    """User model for authentication"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(120))
    role = db.Column(db.String(20), default='user')  # user, admin
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class EnergyConsumption(db.Model):
    """Energy consumption tracking"""
    __tablename__ = 'energy_consumption'
    
    id = db.Column(db.Integer, primary_key=True)
    facility_name = db.Column(db.String(200), nullable=False)
    measurement_date = db.Column(db.Date, nullable=False)
    electricity_kwh = db.Column(db.Float, default=0)
    natural_gas_m3 = db.Column(db.Float, default=0)
    fuel_oil_liters = db.Column(db.Float, default=0)
    notes = db.Column(db.Text)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    creator = db.relationship('User', backref='energy_records')


class WaterUsage(db.Model):
    """Water usage monitoring"""
    __tablename__ = 'water_usage'
    
    id = db.Column(db.Integer, primary_key=True)
    facility_name = db.Column(db.String(200), nullable=False)
    measurement_date = db.Column(db.Date, nullable=False)
    water_consumption_m3 = db.Column(db.Float, nullable=False)
    wastewater_m3 = db.Column(db.Float, default=0)
    notes = db.Column(db.Text)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    creator = db.relationship('User', backref='water_records')


class WasteManagement(db.Model):
    """Waste management records"""
    __tablename__ = 'waste_management'
    
    id = db.Column(db.Integer, primary_key=True)
    facility_name = db.Column(db.String(200), nullable=False)
    measurement_date = db.Column(db.Date, nullable=False)
    medical_waste_kg = db.Column(db.Float, default=0)
    general_waste_kg = db.Column(db.Float, default=0)
    recyclable_waste_kg = db.Column(db.Float, default=0)
    hazardous_waste_kg = db.Column(db.Float, default=0)
    notes = db.Column(db.Text)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    creator = db.relationship('User', backref='waste_records')


class CarbonEmissions(db.Model):
    """Carbon emissions calculation"""
    __tablename__ = 'carbon_emissions'
    
    id = db.Column(db.Integer, primary_key=True)
    facility_name = db.Column(db.String(200), nullable=False)
    measurement_date = db.Column(db.Date, nullable=False)
    scope1_emissions_kg = db.Column(db.Float, default=0)  # Direct emissions
    scope2_emissions_kg = db.Column(db.Float, default=0)  # Indirect emissions from energy
    scope3_emissions_kg = db.Column(db.Float, default=0)  # Other indirect emissions
    total_emissions_kg = db.Column(db.Float, default=0)
    notes = db.Column(db.Text)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    creator = db.relationship('User', backref='emission_records')
