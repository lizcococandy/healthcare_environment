from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.models import EnergyConsumption
from app import db
from datetime import datetime

bp = Blueprint('energy', __name__, url_prefix='/energy')


@bp.route('/')
@login_required
def index():
    """List all energy consumption records"""
    records = EnergyConsumption.query.order_by(EnergyConsumption.measurement_date.desc()).all()
    return render_template('energy/index.html', records=records)


@bp.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    """Add new energy consumption record"""
    if request.method == 'POST':
        facility_name = request.form.get('facility_name')
        measurement_date = datetime.strptime(request.form.get('measurement_date'), '%Y-%m-%d').date()
        electricity_kwh = float(request.form.get('electricity_kwh', 0))
        natural_gas_m3 = float(request.form.get('natural_gas_m3', 0))
        fuel_oil_liters = float(request.form.get('fuel_oil_liters', 0))
        notes = request.form.get('notes', '')
        
        record = EnergyConsumption(
            facility_name=facility_name,
            measurement_date=measurement_date,
            electricity_kwh=electricity_kwh,
            natural_gas_m3=natural_gas_m3,
            fuel_oil_liters=fuel_oil_liters,
            notes=notes,
            created_by=current_user.id
        )
        
        db.session.add(record)
        db.session.commit()
        
        flash('能源消耗記錄已新增', 'success')
        return redirect(url_for('energy.index'))
    
    return render_template('energy/add.html')


@bp.route('/delete/<int:id>')
@login_required
def delete(id):
    """Delete energy consumption record"""
    record = EnergyConsumption.query.get_or_404(id)
    db.session.delete(record)
    db.session.commit()
    flash('記錄已刪除', 'success')
    return redirect(url_for('energy.index'))
