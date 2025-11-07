from flask import Blueprint, render_template
from flask_login import login_required
from app.models import EnergyConsumption, WaterUsage, WasteManagement, CarbonEmissions
from app import db
from sqlalchemy import func, extract
from datetime import datetime, timedelta

bp = Blueprint('reports', __name__, url_prefix='/reports')


@bp.route('/')
@login_required
def index():
    """Reports and analytics page"""
    # Monthly trends for the past 6 months
    six_months_ago = datetime.now() - timedelta(days=180)
    
    # Energy trends by month
    energy_trends = db.session.query(
        extract('year', EnergyConsumption.measurement_date).label('year'),
        extract('month', EnergyConsumption.measurement_date).label('month'),
        func.sum(EnergyConsumption.electricity_kwh).label('total_electricity')
    ).filter(
        EnergyConsumption.measurement_date >= six_months_ago
    ).group_by('year', 'month').order_by('year', 'month').all()
    
    # Water trends by month
    water_trends = db.session.query(
        extract('year', WaterUsage.measurement_date).label('year'),
        extract('month', WaterUsage.measurement_date).label('month'),
        func.sum(WaterUsage.water_consumption_m3).label('total_water')
    ).filter(
        WaterUsage.measurement_date >= six_months_ago
    ).group_by('year', 'month').order_by('year', 'month').all()
    
    # Waste trends by month
    waste_trends = db.session.query(
        extract('year', WasteManagement.measurement_date).label('year'),
        extract('month', WasteManagement.measurement_date).label('month'),
        func.sum(WasteManagement.medical_waste_kg + 
                WasteManagement.general_waste_kg + 
                WasteManagement.recyclable_waste_kg + 
                WasteManagement.hazardous_waste_kg).label('total_waste')
    ).filter(
        WasteManagement.measurement_date >= six_months_ago
    ).group_by('year', 'month').order_by('year', 'month').all()
    
    # Emissions trends by month
    emissions_trends = db.session.query(
        extract('year', CarbonEmissions.measurement_date).label('year'),
        extract('month', CarbonEmissions.measurement_date).label('month'),
        func.sum(CarbonEmissions.total_emissions_kg).label('total_emissions')
    ).filter(
        CarbonEmissions.measurement_date >= six_months_ago
    ).group_by('year', 'month').order_by('year', 'month').all()
    
    return render_template('reports/index.html',
                         energy_trends=energy_trends,
                         water_trends=water_trends,
                         waste_trends=waste_trends,
                         emissions_trends=emissions_trends)
