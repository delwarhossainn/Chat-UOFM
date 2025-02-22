import sqlite3


conn = sqlite3.connect("students.db")
cursor = conn.cursor()


cursor.execute('''
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE,
        major TEXT,
        gpa REAL
    )
''')


students = [
    ("Delwar Hossain", "Computer Science", 3.85),
    ("John Doe", "Mathematics", 3.70),
    ("Jane Smith", "Physics", 3.90)
]

for student in students:
    cursor.execute("INSERT OR IGNORE INTO students (name, major, gpa) VALUES (?, ?, ?)", student)


conn.commit()
conn.close()

print("Database created successfully with sample data!")
