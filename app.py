from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
import sqlite3
from datetime import datetime

app = FastAPI(title="Campus Event Reporting Prototype")

# --------------------------
# Database setup
# --------------------------
def init_db():
    conn = sqlite3.connect("events.db")
    cur = conn.cursor()
    # Create tables if they don't exist
    cur.execute("""CREATE TABLE IF NOT EXISTS events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        type TEXT,
        date TEXT
    )""")
    cur.execute("""CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT UNIQUE
    )""")
    cur.execute("""CREATE TABLE IF NOT EXISTS registrations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER,
        event_id INTEGER,
        UNIQUE(student_id, event_id)
    )""")
    cur.execute("""CREATE TABLE IF NOT EXISTS attendance (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER,
        event_id INTEGER,
        present INTEGER
    )""")
    cur.execute("""CREATE TABLE IF NOT EXISTS feedback (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER,
        event_id INTEGER,
        rating INTEGER,
        comment TEXT
    )""")
    conn.commit()
    conn.close()

init_db()

# --------------------------
# Pydantic Schemas
# --------------------------
class Event(BaseModel):
    name: str
    type: str
    date: str   # "YYYY-MM-DD"

class Student(BaseModel):
    name: str
    email: str

class Registration(BaseModel):
    student_id: int
    event_id: int

class Attendance(BaseModel):
    student_id: int
    event_id: int
    present: bool

class Feedback(BaseModel):
    student_id: int
    event_id: int
    rating: int
    comment: Optional[str] = None

# --------------------------
# Routes
# --------------------------
@app.post("/events")
def create_event(event: Event):
    conn = sqlite3.connect("events.db")
    cur = conn.cursor()
    cur.execute("INSERT INTO events (name, type, date) VALUES (?, ?, ?)", 
                (event.name, event.type, event.date))
    conn.commit()
    event_id = cur.lastrowid
    conn.close()
    return {"id": event_id, "message": "Event created"}

@app.post("/students")
def create_student(student: Student):
    conn = sqlite3.connect("events.db")
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO students (name, email) VALUES (?, ?)", 
                    (student.name, student.email))
        conn.commit()
        student_id = cur.lastrowid
    except sqlite3.IntegrityError:
        return {"error": "Email already exists"}
    conn.close()
    return {"id": student_id, "message": "Student created"}

@app.post("/registrations")
def register(reg: Registration):
    conn = sqlite3.connect("events.db")
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO registrations (student_id, event_id) VALUES (?, ?)", 
                    (reg.student_id, reg.event_id))
        conn.commit()
        reg_id = cur.lastrowid
    except sqlite3.IntegrityError:
        return {"error": "Already registered"}
    conn.close()
    return {"id": reg_id, "message": "Registered"}

@app.post("/attendance")
def mark_attendance(att: Attendance):
    conn = sqlite3.connect("events.db")
    cur = conn.cursor()
    cur.execute("INSERT INTO attendance (student_id, event_id, present) VALUES (?, ?, ?)", 
                (att.student_id, att.event_id, int(att.present)))
    conn.commit()
    att_id = cur.lastrowid
    conn.close()
    return {"id": att_id, "message": "Attendance recorded"}

@app.post("/feedback")
def give_feedback(fb: Feedback):
    conn = sqlite3.connect("events.db")
    cur = conn.cursor()
    cur.execute("INSERT INTO feedback (student_id, event_id, rating, comment) VALUES (?, ?, ?, ?)", 
                (fb.student_id, fb.event_id, fb.rating, fb.comment))
    conn.commit()
    fb_id = cur.lastrowid
    conn.close()
    return {"id": fb_id, "message": "Feedback submitted"}
@app.get("/report/attendance/{event_id}")
def report_attendance(event_id: int):
    conn = sqlite3.connect("events.db")
    cur = conn.cursor()

    # total registrations
    cur.execute("SELECT COUNT(*) FROM registrations WHERE event_id = ?", (event_id,))
    total_regs = cur.fetchone()[0]

    # present count
    cur.execute("SELECT COUNT(*) FROM attendance WHERE event_id = ? AND present = 1", (event_id,))
    present_count = cur.fetchone()[0]

    conn.close()

    percentage = (present_count / total_regs * 100) if total_regs > 0 else 0.0

    return {
        "event_id": event_id,
        "registrations": total_regs,
        "present": present_count,
        "attendance_percentage": round(percentage, 2)
    }
@app.get("/report/feedback/{event_id}")
def report_feedback(event_id: int):
    conn = sqlite3.connect("events.db")
    cur = conn.cursor()

    # average rating & count
    cur.execute("SELECT AVG(rating), COUNT(*) FROM feedback WHERE event_id = ?", (event_id,))
    row = cur.fetchone()
    avg_rating, responses = row[0], row[1]

    conn.close()

    return {
        "event_id": event_id,
        "avg_rating": round(avg_rating, 2) if avg_rating is not None else None,
        "responses": responses
    }
@app.get("/report/registrations/{event_id}")
def report_registrations(event_id: int):
    conn = sqlite3.connect("events.db")
    cur = conn.cursor()

    # total registrations
    cur.execute("SELECT COUNT(*) FROM registrations WHERE event_id = ?", (event_id,))
    total_regs = cur.fetchone()[0]

    conn.close()

    return {
        "event_id": event_id,
        "registrations": total_regs
    }

@app.get("/")
def root():
    return {"status": "ok", "message": "Campus Event Reporting API is running"}
