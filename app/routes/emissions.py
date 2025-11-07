from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.models import CarbonEmissions
from app import db
from datetime import datetime

bp = Blueprint('emissions', __name__, url_prefix='/emissions')


@bp.route('/')
@login_required
def index():
    """List all carbon emissions records"""
    records = CarbonEmissions.query.order_by(CarbonEmissions.measurement_date.desc()).all()
    return render_template('emissions/index.html', records=records)


@bp.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    """Add new carbon emissions record"""
    if request.method == 'POST':
        try:
            facility_name = request.form.get('facility_name')
            measurement_date = datetime.strptime(request.form.get('measurement_date'), '%Y-%m-%d').date()
            scope1_emissions_kg = float(request.form.get('scope1_emissions_kg', 0))
            scope2_emissions_kg = float(request.form.get('scope2_emissions_kg', 0))
            scope3_emissions_kg = float(request.form.get('scope3_emissions_kg', 0))
            total_emissions_kg = scope1_emissions_kg + scope2_emissions_kg + scope3_emissions_kg
            notes = request.form.get('notes', '')
        except (ValueError, TypeError) as e:
            flash('輸入資料格式錯誤，請檢查日期和數值格式', 'error')
            return render_template('emissions/add.html')
        
        record = CarbonEmissions(
            facility_name=facility_name,
            measurement_date=measurement_date,
            scope1_emissions_kg=scope1_emissions_kg,
            scope2_emissions_kg=scope2_emissions_kg,
            scope3_emissions_kg=scope3_emissions_kg,
            total_emissions_kg=total_emissions_kg,
            notes=notes,
            created_by=current_user.id
        )
        
        db.session.add(record)
        db.session.commit()
        
        flash('碳排放記錄已新增', 'success')
        return redirect(url_for('emissions.index'))
    
    return render_template('emissions/add.html')


@bp.route('/delete/<int:id>')
@login_required
def delete(id):
    """Delete carbon emissions record"""
    record = CarbonEmissions.query.get_or_404(id)
    db.session.delete(record)
    db.session.commit()
    flash('記錄已刪除', 'success')
    return redirect(url_for('emissions.index'))
