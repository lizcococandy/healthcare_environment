from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from app.models import EnergyConsumption, WaterUsage, WasteManagement, CarbonEmissions
from app import db
from sqlalchemy import func

bp = Blueprint('main', __name__)


@bp.route('/')
def index():
    """Landing page"""
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    return render_template('index.html')


@bp.route('/dashboard')
@login_required
def dashboard():
    """Main dashboard with sustainability metrics"""
    # Get summary statistics
    total_energy = db.session.query(func.sum(EnergyConsumption.electricity_kwh)).scalar() or 0
    total_water = db.session.query(func.sum(WaterUsage.water_consumption_m3)).scalar() or 0
    total_waste = db.session.query(
        func.sum(WasteManagement.medical_waste_kg + 
                WasteManagement.general_waste_kg + 
                WasteManagement.recyclable_waste_kg + 
                WasteManagement.hazardous_waste_kg)
    ).scalar() or 0
    total_emissions = db.session.query(func.sum(CarbonEmissions.total_emissions_kg)).scalar() or 0
    
    # Get recent records
    recent_energy = EnergyConsumption.query.order_by(EnergyConsumption.measurement_date.desc()).limit(5).all()
    recent_water = WaterUsage.query.order_by(WaterUsage.measurement_date.desc()).limit(5).all()
    recent_waste = WasteManagement.query.order_by(WasteManagement.measurement_date.desc()).limit(5).all()
    recent_emissions = CarbonEmissions.query.order_by(CarbonEmissions.measurement_date.desc()).limit(5).all()
    
    return render_template('dashboard.html',
                         total_energy=total_energy,
                         total_water=total_water,
                         total_waste=total_waste,
                         total_emissions=total_emissions,
                         recent_energy=recent_energy,
                         recent_water=recent_water,
                         recent_waste=recent_waste,
                         recent_emissions=recent_emissions)
