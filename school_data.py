import sqlite3, os, time, pyinputplus as pyip

connection = sqlite3.connect("schooldata.db")
cursor = connection.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS Students 
               (StudentID INTEGER PRIMARY KEY AUTOINCREMENT,Firstname TEXT, 
               Surname TEXT, DOB DATE, Gender TEXT, Mastery TEXT, 
               Yeargroup INTEGER,  Email TEXT)''')


cursor.execute('''CREATE TABLE IF NOT EXISTS Timetable 
               ( StudentID INTEGER, Day TEXT, Period1 TEXT, Period2 TEXT, 
               Period3 TEXT, Period4 TEXT, Period5 TEXT, Period6 TEXT, 
               FOREIGN KEY(StudentID) REFERENCES students(StudentID))''')


cursor.execute('''CREATE TABLE IF NOT EXISTS Student_Info 
               (StudentID INTEGER, Parentname TEXT, Parentnumber INTEGER, 
               Address TEXT, Nationality TEXT, countryofbirth TEXT, Enrollmentdate DATE, 
               FOREIGN KEY(StudentID) REFERENCES students(StudentID))''') 


cursor.execute('''CREATE TABLE IF NOT EXISTS Medical_Info 
               (StudentID INTEGER, Conditions TEXT, Medication TEXT, Allergies TEXT, 
               Needs TEXT, FOREIGN KEY(StudentID) REFERENCES students(StudentID))''')


cursor.execute('''CREATE TABLE IF NOT EXISTS Attendance 
               (AttendanceID INTEGER PRIMARY KEY AUTOINCREMENT, StudentID INTEGER, 
               Date DATE, Status TEXT, FOREIGN KEY(StudentID) REFERENCES students(StudentID))''')


cursor.execute('''CREATE TABLE IF NOT EXISTS Behaviour 
               (BehaviourID INTEGER PRIMARY KEY AUTOINCREMENT, StudentID INTEGER, 
               Date DATE, Housepoints INTEGER, Sanctions TEXT, Action TEXT, 
               FOREIGN KEY(StudentID) REFERENCES students(StudentID))''')


cursor.execute('''CREATE TABLE IF NOT EXISTS Teachers 
               (TeacherID INTEGER PRIMARY KEY AUTOINCREMENT, Firstname TEXT, 
                Surname TEXT, Gender TEXT, Email TEXT, Role TEXT)''')


cursor.execute('''CREATE TABLE IF NOT EXISTS Subjects 
               (SubjectID INTEGER PRIMARY KEY AUTOINCREMENT, Subjectname TEXT, 
               TeacherID INTEGER, FOREIGN KEY(TeacherID) REFERENCES teachers(TeacherID))''')


cursor.execute('''CREATE TABLE IF NOT EXISTS Scores 
               (ScoreID INTEGER PRIMARY KEY AUTOINCREMENT, StudentID INTEGER, SubjectID INTEGER, 
               Score INTEGER, Assessment1 FLOAT, Assessment2 FLOAT, Assessment3 FLOAT, 
               FOREIGN KEY(StudentID) REFERENCES students(StudentID), 
               FOREIGN KEY(SubjectID) REFERENCES subjects(SubjectID))''')   


cursor.execute('''CREATE TABLE IF NOT EXISTS Assessments
               (AssessmentID INTEGER PRIMARY KEY AUTOINCREMENT, StudentID INTEGER, 
               SubjectID INTEGER, Type TEXT, Score FLOAT, Date DATE, 
               FOREIGN KEY(StudentID) REFERENCES students(StudentID), 
               FOREIGN KEY(SubjectID) REFERENCES subjects(SubjectID))''')


cursor.execute('''CREATE TABLE IF NOT EXISTS Summaries
               (SummaryID INTEGER PRIMARY KEY AUTOINCREMENT, StudentID INTEGER, 
               Week DATE, SummaryText TEXT, 
               FOREIGN KEY(StudentID) REFERENCES students(StudentID))''')



cursor.execute("INSERT INTO Teachers (Firstname, Surname, Gender, Email, Role) VALUES (?,?,?,?,?)", ('Joshua', 'Curran', 'F', 'curranj@mercia.school', 'T'))
connection.commit()
