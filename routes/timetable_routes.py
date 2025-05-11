from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required
from models.timetable_model import TimetableModel

timetable_bp = Blueprint('timetable', __name__)

@timetable_bp.route('/')
def view_timetable():
    timetable_model = TimetableModel()
    timetables = timetable_model.get_all_timetables()
    return render_template('view_timetable.html', timetables=timetables)

@timetable_bp.route('/dashboard')
@login_required
def dashboard():
    timetable_model = TimetableModel()
    timetables = timetable_model.get_all_timetables()
    return render_template('dashboard.html', timetables=timetables)

@timetable_bp.route('/timetable/edit/<timetable_id>', methods=['GET', 'POST'])
@login_required
def edit_timetable(timetable_id):
    timetable_model = TimetableModel()
    
    if request.method == 'POST':
        data = request.form.to_dict()
        if timetable_id == 'new':
            # Create new timetable
            timetable_model.create_timetable(data)
        else:
            # Update existing timetable
            timetable_model.update_timetable(timetable_id, data)
        return redirect(url_for('timetable.dashboard'))
    
    # For GET request
    if timetable_id == 'new':
        timetable = None  # No timetable data for new entry
    else:
        timetable = timetable_model.get_timetable_by_id(timetable_id)
    
    return render_template('edit_timetable.html', timetable=timetable)
