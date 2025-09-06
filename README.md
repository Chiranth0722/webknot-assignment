# Campus Event Reporting Prototype

# Features
1. Add students and events
2. Register students to events
3. Record attendance
4. Collect feedback with rating and comments
5. Reports:
        Attendance percentage per event
        Average feedback per event
        Total registrations per event

# Detailed Explaination of Campus Event Reporting Prototype

This project is a simple web application built using FastAPI with SQLite as the database. The aim was to design a system that simulates how a college can manage events and track student participation. The application provides endpoints to add students and events, register students to those events, mark their attendance, and collect feedback. Along with these core operations, the system also generates basic reports such as attendance percentage, average feedback ratings, and total registrations for each event.

During the workflow, a student can first be added to the system and an event can be created by the admin. Once the event exists, the student can register for it. On the day of the event, the student’s attendance can be marked. After attending, the student has the option to submit feedback with a rating and an optional comment.

The reports give useful insights based on the collected information. For example, I’ve implemented a way to check the percentage of registered students who attended a particular event, view the average feedback rating provided by students, and see how many students registered in total. These reports demonstrate how I’ve helped the system show the engagement and effectiveness of the events. Overall, I’ve built this project to showcase a complete cycle from event creation to reporting in a lightweight prototype form.
