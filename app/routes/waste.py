from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.models import WasteManagement
from app import db
from datetime import datetime

bp = Blueprint('waste', __name__, url_prefix='/waste')


@bp.route('/')
@login_required
def index():
    """List all waste management records"""
    records = WasteManagement.query.order_by(WasteManagement.measurement_date.desc()).all()
    return render_template('waste/index.html', records=records)


@bp.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    """Add new waste management record"""
    if request.method == 'POST':
        try:
            facility_name = request.form.get('facility_name')
            measurement_date = datetime.strptime(request.form.get('measurement_date'), '%Y-%m-%d').date()
            medical_waste_kg = float(request.form.get('medical_waste_kg', 0))
            general_waste_kg = float(request.form.get('general_waste_kg', 0))
            recyclable_waste_kg = float(request.form.get('recyclable_waste_kg', 0))
            hazardous_waste_kg = float(request.form.get('hazardous_waste_kg', 0))
            notes = request.form.get('notes', '')
        except (ValueError, TypeError) as e:
            flash('輸入資料格式錯誤，請檢查日期和數值格式', 'error')
            return render_template('waste/add.html')
        
        record = WasteManagement(
            facility_name=facility_name,
            measurement_date=measurement_date,
            medical_waste_kg=medical_waste_kg,
            general_waste_kg=general_waste_kg,
            recyclable_waste_kg=recyclable_waste_kg,
            hazardous_waste_kg=hazardous_waste_kg,
            notes=notes,
            created_by=current_user.id
        )
        
        db.session.add(record)
        db.session.commit()
        
        flash('廢棄物管理記錄已新增', 'success')
        return redirect(url_for('waste.index'))
    
    return render_template('waste/add.html')


@bp.route('/delete/<int:id>')
@login_required
def delete(id):
    """Delete waste management record"""
    record = WasteManagement.query.get_or_404(id)
    db.session.delete(record)
    db.session.commit()
    flash('記錄已刪除', 'success')
    return redirect(url_for('waste.index'))
