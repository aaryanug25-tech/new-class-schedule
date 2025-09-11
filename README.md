# Class Scheduler Web Application

A web-based platform for automated class scheduling in higher education institutions. It allows authorized users to input classrooms, courses, teachers, and class groups, and generates an optimized, color-coded timetable. Teachers can also find available rooms for extra classes and suggest rescheduling options.

---

## Features
- Add and manage classrooms, courses, teachers, and class groups
- Assign one teacher per course per class group
- Generate a weekly timetable (8am–6pm, Mon–Fri) with no conflicts
- Color-coded, tabular timetable display for each class group
- Find available rooms for extra classes
- Suggest rescheduling options for classes
- Data stored in a local SQLite database

## Tech Stack
- Python 3
- Flask (web framework)
- SQLAlchemy (ORM)
- Jinja2 (templating)
- HTML/CSS (modern, animated dark UI)

## Getting Started

### 1. Clone the repository
```sh
git clone https://github.com/<your-username>/<repo-name>.git
cd <repo-name>
```

### 2. Install dependencies
```sh
python3 -m pip install flask sqlalchemy markupsafe
```

### 3. Run the application
```sh
cd PROJECT
python3 webapp/app.py
```

- If you see a `ModuleNotFoundError: No module named 'scheduler'`, make sure you are running the command from the `PROJECT` directory.

### 4. Open in your browser
Go to [http://localhost:5000](http://localhost:5000)

## Usage
1. Add classrooms, courses, teachers, and class groups using the forms.
2. Assign each course in a class group to a teacher.
3. Click "Generate Timetable" to create the schedule.
4. View, print, or share the color-coded timetable.
5. Use the "Find Available Rooms" and "Reschedule" features as needed.

## Project Structure
```
PROJECT/
├── scheduler.py           # Core scheduling logic and database models
├── webapp/
│   ├── app.py             # Flask web application
│   ├── templates/         # HTML templates
│   └── static/            # CSS and static files (dark theme)
├── scheduler.db           # SQLite database (auto-created)
└── README.md
```

## Notes
- All data is stored locally in `scheduler.db`. To start fresh, delete this file.
- To collaborate, push your code to GitHub and share the repo link with your team.
- For deployment instructions (cloud, public access), see the main app or ask for help.
- The UI is now a modern dark theme inspired by the BASIC® Culture Manual.

## License
MIT License
