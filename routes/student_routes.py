from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from models.student_model import StudentModel
from bson.objectid import ObjectId

student_bp = Blueprint('student', __name__)

@student_bp.route('/students')
@login_required
def list_students():
    student_model = StudentModel()
    students = student_model.get_all_students()
    return render_template('students.html', students=students)

@student_bp.route('/student/edit/<student_id>', methods=['GET', 'POST'])
@login_required
def edit_student(student_id):
    student_model = StudentModel()
    
    if request.method == 'POST':
        data = request.form.to_dict()
        if student_id == 'new':
            # Create new student
            result, error = student_model.create_student(data)
            if error:
                flash(error)
                return render_template('edit_student.html', student=data)
        else:
            # Update existing student
            result, error = student_model.update_student(student_id, data)
            if error:
                flash(error)
                student = student_model.get_student_by_id(student_id)
                return render_template('edit_student.html', student=student)
        
        return redirect(url_for('student.list_students'))
    
    # For GET request
    if student_id == 'new':
        student = None  # No student data for new student
    else:
        student = student_model.get_student_by_id(student_id)
    
    return render_template('edit_student.html', student=student)

@student_bp.route('/student/delete/<student_id>')
@login_required
def delete_student(student_id):
    student_model = StudentModel()
    student_model.delete_student(student_id)
    return redirect(url_for('student.list_students'))

def get_student_by_id(self, student_id):
    try:
        return self.db.students.find_one({'_id': ObjectId(student_id)})
    except Exception as e:
        print(f"Error fetching student: {str(e)}")
        return None