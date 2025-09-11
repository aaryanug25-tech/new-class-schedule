import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, render_template, request, redirect, url_for
from markupsafe import Markup
from scheduler import get_session, add_classroom, add_course, add_teacher, add_class, generate_timetable, find_available_rooms, suggest_reschedule_options, Course, Teacher, Class, Classroom, Timetable

app = Flask(__name__)
session = get_session()

# Jinja filter to assign a color class to each course
def course_color_class(cell):
    if not cell:
        return ''
    # Use the course name as a key for color assignment
    course_name = cell.split('<br>')[0] if '<br>' in cell else cell
    # Simple hash for color assignment
    idx = abs(hash(course_name)) % 10
    return f'course-color-{idx}'

app.jinja_env.filters['course_color_class'] = course_color_class

def get_courses():
    return session.query(Course).all()

def get_teachers():
    return session.query(Teacher).all()

def get_classes():
    return session.query(Class).all()

def get_classrooms():
    return session.query(Classroom).all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_classroom', methods=['GET', 'POST'])
def add_classroom_route():
    if request.method == 'POST':
        name = request.form['name']
        capacity = int(request.form['capacity'])
        add_classroom(session, name, capacity)
        return redirect(url_for('index'))
    return render_template('add_classroom.html')

@app.route('/add_course', methods=['GET', 'POST'])
def add_course_route():
    if request.method == 'POST':
        name = request.form['name']
        add_course(session, name)
        return redirect(url_for('index'))
    return render_template('add_course.html')

@app.route('/add_teacher', methods=['GET', 'POST'])
def add_teacher_route():
    if request.method == 'POST':
        name = request.form['name']
        subject = request.form['subject']
        add_teacher(session, name, subject)
        return redirect(url_for('index'))
    return render_template('add_teacher.html', courses=get_courses())

@app.route('/add_class', methods=['GET', 'POST'])
def add_class_route():
    if request.method == 'POST':
        name = request.form['name']
        course_ids = request.form.getlist('course_id')
        teacher_ids = request.form.getlist('teacher_id')
        course_teacher_map = {int(c): int(t) for c, t in zip(course_ids, teacher_ids)}
        add_class(session, name, course_teacher_map)
        return redirect(url_for('index'))
    return render_template('add_class.html', courses=get_courses(), teachers=get_teachers())

@app.route('/generate_timetable')
def generate_timetable_route():
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    # 8am to 6pm, 1 hour slots
    time_slots = [(f"{h:02d}:00", f"{h+1:02d}:00") for h in range(8, 18)]
    generate_timetable(session, days, time_slots)
    # Build timetable grid for all classes
    classes = session.query(Class).all()
    timetable_data = {}
    for class_ in classes:
        grid = {slot: {day: None for day in days} for slot in time_slots}
        entries = session.query(Timetable).filter_by(class_id=class_.id).all()
        for entry in entries:
            slot = (entry.start_time, entry.end_time)
            grid[slot][entry.day] = f"{entry.course.name}<br>{entry.teacher.name}<br>{entry.classroom.name}"
        timetable_data[class_.name] = grid
    return render_template('timetable.html', timetable_data=timetable_data, days=days, time_slots=time_slots)

@app.route('/find_rooms', methods=['GET', 'POST'])
def find_rooms_route():
    available = []
    if request.method == 'POST':
        day = request.form['day']
        start = request.form['start_time']
        end = request.form['end_time']
        available = find_available_rooms(session, day, start, end)
    return render_template('find_rooms.html', available=available)

@app.route('/reschedule', methods=['GET', 'POST'])
def reschedule_route():
    options = []
    if request.method == 'POST':
        class_id = int(request.form['class_id'])
        course_id = int(request.form['course_id'])
        options = suggest_reschedule_options(session, class_id, course_id)
    return render_template('reschedule.html', classes=get_classes(), courses=get_courses(), options=options)

if __name__ == '__main__':
    app.run(debug=True)
