from flask import Flask, render_template, redirect, jsonify
import sqlite3
from datetime import datetime

import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "attendance.db")
print(os.path.abspath(DB_PATH))

conn = sqlite3.connect(DB_PATH)
conn.execute("DROP TABLE IF EXISTS students")
conn.execute("""CREATE TABLE IF NOT EXISTS attendance(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER,
            name TEXT,
            time TEXT,
            status TEXT DEFAULT '미출석')""")
conn.execute("""CREATE TABLE IF NOT EXISTS students(
             id INTEGER PRIMARY KEY,
             studentno TEXT,
             name TEXT)""")
conn.execute("""INSERT OR IGNORE INTO students (id, studentno, name) VALUES
             (1, '2612', '여찬음'),
             (2, '2409', '박준수'),
             (3, '2409', '손흥민'),
             (4, "2612", "여찬음")""")
conn.commit()
conn.close()

app = Flask(__name__)
@app.route('/')
def index():
    conn = sqlite3.connect(DB_PATH)
    rows = conn.execute("SELECT * FROM attendance ORDER BY id DESC").fetchall()
    conn.close()
    return render_template("index.html", rows=rows)
@app.route('/clear')
def clear():
    conn=sqlite3.connect(DB_PATH)
    conn.execute("DELETE FROM attendance")
    conn.execute("DELETE FROM sqlite_sequence WHERE name='attendance'")
    conn.commit()
    conn.close()
    return redirect('/')
@app.route('/ref')
def refresh():
    conn = sqlite3.connect(DB_PATH)
    rows = conn.execute("SELECT * FROM attendance ORDER BY id DESC").fetchall()
    total = conn.execute("SELECT COUNT(*) FROM students").fetchone()[0]
    conn.close()
    data = []
    for row in rows:
        data.append({
            'id': row[0],
            'student_id': row[1],
            'name': row[2],
            'time': row[3],
            'status': row[4]
        })
    return jsonify({
        "attendance": data,
        "total": total
    })

def choolseokcheck(faceid):
    print("출석 체크:", faceid)

    conn = sqlite3.connect(DB_PATH)

    student = conn.execute(
        "SELECT * FROM students WHERE id=?",
        (faceid,)
    ).fetchone()

    print("학생:", student)

    if student:
        already = conn.execute(
            "SELECT * FROM attendance WHERE student_id=?",
            (student[1],)
        ).fetchone()

        print("이미 있음?", already)

        if not already:
            print("DB 저장!")
            now = datetime.now()
            if now.minute < 23:
                status = "출석"
            else:
                status = "지각"

            conn.execute("""
                INSERT INTO attendance(student_id, name, time, status)
                VALUES (?, ?, ?, ?)
            """, (student[1], student[2], now.strftime("%Y-%m-%d %H:%M:%S"), status))

            conn.commit()

    conn.close()
if __name__ == '__main__':
    app.run()