# Design Document — Campus Event Reporting Prototype

1. Purpose

The goal of this prototype is to simulate how a college can track event participation. 

It covers:

    Creating events
    Adding students
    Managing registrations
    Recording attendance
    Collecting feedback
    Generating simple reports

2. Data Model

Database: SQLite

Tables:

    students → (id, name, email)
    events → (id, name, type, date)
    registrations → (id, student_id, event_id)
    attendance → (id, student_id, event_id, present)
    feedback → (id, student_id, event_id, rating, comment)

3. API Endpoints

    'POST /students' → add a student
   
    'POST /events' → create an event
   
    'POST /registrations' → register student to event
   
    'POST /attendance' → mark attendance
   
    'POST /feedback' → submit feedback
   
    'GET /report/attendance/{event_id}' → attendance percentage
   
    'GET /report/feedback/{event_id}' → average feedback per event
   
    'GET /report/registrations/{event_id}' → total registrations
   

5. Workflow

    Admin creates an event.
   
    Students are added to the system.
   
    Students register for events.
   
    Attendance is marked on event day.
   
    Students provide feedback.
   
    Reports are generated from the collected data.
   

7. Constraints and Rules

    Email must be unique per student.
   
    Student cannot register more than once for the same event.
   
    Attendance only allowed for registered students.
   
    Only one feedback entry per student per event.
   

9. Edge Cases

    If a student tries to register twice → system blocks it.
   
    If attendance is marked without registration → blocked.
   
    If feedback is submitted without registration → blocked.
   

11. Scalability

    Prototype uses SQLite (works for demo and small datasets).
    
    For production: use PostgreSQL/MySQL, add authentication, and possibly split data per college.
    
    Reports can be extended for most active students or popular event types.
    

