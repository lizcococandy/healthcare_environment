from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.models import WaterUsage
from app import db
from datetime import datetime

bp = Blueprint('water', __name__, url_prefix='/water')


@bp.route('/')
@login_required
def index():
    """List all water usage records"""
    records = WaterUsage.query.order_by(WaterUsage.measurement_date.desc()).all()
    return render_template('water/index.html', records=records)


@bp.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    """Add new water usage record"""
    if request.method == 'POST':
        try:
            facility_name = request.form.get('facility_name')
            measurement_date = datetime.strptime(request.form.get('measurement_date'), '%Y-%m-%d').date()
            water_consumption_m3 = float(request.form.get('water_consumption_m3'))
            wastewater_m3 = float(request.form.get('wastewater_m3', 0))
            notes = request.form.get('notes', '')
        except (ValueError, TypeError) as e:
            flash('輸入資料格式錯誤，請檢查日期和數值格式', 'error')
            return render_template('water/add.html')
        
        record = WaterUsage(
            facility_name=facility_name,
            measurement_date=measurement_date,
            water_consumption_m3=water_consumption_m3,
            wastewater_m3=wastewater_m3,
            notes=notes,
            created_by=current_user.id
        )
        
        db.session.add(record)
        db.session.commit()
        
        flash('用水記錄已新增', 'success')
        return redirect(url_for('water.index'))
    
    return render_template('water/add.html')


@bp.route('/delete/<int:id>')
@login_required
def delete(id):
    """Delete water usage record"""
    record = WaterUsage.query.get_or_404(id)
    db.session.delete(record)
    db.session.commit()
    flash('記錄已刪除', 'success')
    return redirect(url_for('water.index'))
