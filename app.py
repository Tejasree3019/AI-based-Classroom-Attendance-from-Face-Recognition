import csv, sqlite3
from datetime import datetime
from pathlib import Path
from flask import Flask, render_template, request, redirect, url_for, flash, send_file
from face_recognition.recognition import register_face, recognize_faces, model_available

BASE = Path(__file__).resolve().parent
DB = BASE / "database" / "attendance.db"
DATASET = BASE / "dataset" / "students"
EXPORTS = BASE / "exports"

app = Flask(__name__)
app.secret_key = "classroom-attendance-demo-key"

def get_db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def index():
    conn = get_db()
    students = conn.execute("SELECT * FROM students ORDER BY name").fetchall()
    today = datetime.now().strftime("%Y-%m-%d")
    present = conn.execute("SELECT COUNT(*) FROM attendance WHERE date=? AND status='Present'", (today,)).fetchone()[0]
    conn.close()
    return render_template("index.html", students=students, present=present, model_ok=model_available())

@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name","").strip()
        reg = request.form.get("register_no","").strip()
        image = request.files.get("image")
        if not name or not reg or not image or image.filename == "":
            flash("Enter name, register number and upload a clear face image.", "danger")
            return redirect(url_for("register"))
        conn = get_db()
        try:
            next_label = conn.execute("SELECT COALESCE(MAX(face_label),0)+1 FROM students").fetchone()[0]
            student_id = conn.execute(
                "INSERT INTO students(register_no,name,face_label) VALUES(?,?,?)",
                (reg, name, next_label)
            ).lastrowid
            student_dir = DATASET / f"{next_label}_{reg}"
            student_dir.mkdir(parents=True, exist_ok=True)
            image_path = student_dir / "face.jpg"
            image.save(image_path)
            if not register_face(str(image_path), next_label):
                conn.execute("DELETE FROM students WHERE id=?", (student_id,))
                conn.commit()
                flash("No clear face was detected. Try a front-facing, well-lit image.", "danger")
                return redirect(url_for("register"))
            conn.commit()
            flash(f"{name} registered successfully.", "success")
        except sqlite3.IntegrityError:
            conn.rollback()
            flash("Register number already exists.", "danger")
        finally:
            conn.close()
        return redirect(url_for("index"))
    return render_template("register.html")

@app.route("/attendance", methods=["GET","POST"])
def attendance():
    conn = get_db()
    students = conn.execute("SELECT * FROM students ORDER BY name").fetchall()
    if request.method == "POST":
        image = request.files.get("classroom_image")
        if not image or image.filename == "":
            flash("Upload a classroom photo.", "danger")
            conn.close()
            return redirect(url_for("attendance"))
        temp = BASE / "classroom_temp.jpg"
        image.save(temp)
        try:
            labels = recognize_faces(str(temp))
            today = datetime.now().strftime("%Y-%m-%d")
            now = datetime.now().strftime("%H:%M:%S")
            for s in students:
                status = "Present" if s["face_label"] in labels else "Absent"
                conn.execute("""INSERT INTO attendance(student_id,date,time,status)
                    VALUES(?,?,?,?)
                    ON CONFLICT(student_id,date) DO UPDATE SET time=excluded.time,status=excluded.status""",
                    (s["id"], today, now, status))
            conn.commit()
            flash(f"Attendance marked. Recognized {len(labels)} registered face(s).", "success")
        except Exception as e:
            flash(f"Recognition error: {e}", "danger")
        finally:
            if temp.exists(): temp.unlink()
        conn.close()
        return redirect(url_for("dashboard"))
    conn.close()
    return render_template("attendance.html", students=students, model_ok=model_available())

@app.route("/dashboard")
def dashboard():
    date = request.args.get("date") or datetime.now().strftime("%Y-%m-%d")
    conn = get_db()
    rows = conn.execute("""SELECT s.name,s.register_no,a.date,a.time,a.status
                           FROM students s LEFT JOIN attendance a
                           ON s.id=a.student_id AND a.date=?
                           ORDER BY s.name""", (date,)).fetchall()
    conn.close()
    return render_template("dashboard.html", rows=rows, date=date)

@app.post("/update/<register_no>")
def update_attendance(register_no):
    date = request.form["date"]
    status = request.form["status"]
    conn = get_db()
    student = conn.execute("SELECT id FROM students WHERE register_no=?", (register_no,)).fetchone()
    if student:
        now = datetime.now().strftime("%H:%M:%S")
        conn.execute("""INSERT INTO attendance(student_id,date,time,status) VALUES(?,?,?,?)
                        ON CONFLICT(student_id,date) DO UPDATE SET time=excluded.time,status=excluded.status""",
                     (student["id"], date, now, status))
        conn.commit()
    conn.close()
    return redirect(url_for("dashboard", date=date))

@app.route("/export")
def export():
    date = request.args.get("date") or datetime.now().strftime("%Y-%m-%d")
    conn = get_db()
    rows = conn.execute("""SELECT s.register_no,s.name,COALESCE(a.status,'Absent') status,
                                  COALESCE(a.time,'-') time
                           FROM students s LEFT JOIN attendance a
                           ON s.id=a.student_id AND a.date=?
                           ORDER BY s.name""", (date,)).fetchall()
    conn.close()
    out = EXPORTS / f"attendance_{date}.csv"
    with open(out, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Register No","Student Name","Status","Time","Date"])
        for r in rows:
            writer.writerow([r["register_no"],r["name"],r["status"],r["time"],date])
    return send_file(out, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
