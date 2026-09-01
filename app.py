from flask import Flask, render_template, request, redirect, session
import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

app.secret_key = "blossom-school-secret-key"
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )
@app.route("/test-db")
def test_db():
    db = get_db_connection()
    db.close()
    return "Database connected successfully!"


# =========================
# MYSQL CONNECTION
# =========================

def get_db_connection():

    return mysql.connector.connect(
        host="localhost",
        user="root",
        password=os.getenv("DB_PASSWORD")
        database="blossom_school"
    )


# =========================
# HOME PAGE
# =========================


@app.route("/")
def homee():

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT * FROM home_content LIMIT 1")

    content = cursor.fetchone()

    cursor.close()
    db.close()

    return render_template("homee.html", content=content)


# =========================
# ABOUT PAGE
# =========================

@app.route("/about")
def about():
    return render_template("about.html")


# =========================
# GALLERY
# =========================
@app.route("/gallery")
def gallery():

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    # Get photos
    cursor.execute("SELECT * FROM gallery ORDER BY id DESC")
    photos = cursor.fetchall()

    # Get videos
    cursor.execute("SELECT * FROM videos ORDER BY id DESC")
    videos = cursor.fetchall()

    cursor.close()
    db.close()

    return render_template(
        "gallery.html",
        photos=photos,
        videos=videos
    )


# =========================
# ADMISSION
# =========================
@app.route("/admission", methods=["GET", "POST"])
def admission():

    if request.method == "POST":

        student_name = request.form["student_name"]
        dob = request.form["dob"]
        gender = request.form["gender"]
        class_apply = request.form["class_apply"]
        father_name = request.form["father_name"]
        mother_name = request.form["mother_name"]
        phone = request.form["phone"]
        email = request.form.get("email")
        address = request.form.get("address")

        db = get_db_connection()
        cursor = db.cursor()

        cursor.execute("""
            INSERT INTO admissions
            (
                student_name,
                dob,
                father_name,
                mother_name,
                gender,
                phone,
                email,
                address,
                class_apply
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            student_name,
            dob,
            father_name,
            mother_name,
            gender,
            phone,
            email,
            address,
            class_apply
        ))

        db.commit()

        cursor.close()
        db.close()

        return "Admission form submitted successfully!"

    return render_template("addmission.html")

# =========================
# CONTACT
# =========================

@app.route("/contact")
def contact():
    return render_template("contact.html")


# =========================
# ADMIN LOGIN
# =========================

@app.route("/admin", methods=["GET", "POST"])
def admin():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        if username == os.getenv("ADMIN_USERNAME") and password == os.getenv("ADMIN_PASSWORD"):

            session["admin"] = True

            return redirect("/dashboard")

        else:

            return render_template(
                "admin_login.html",
                error="Invalid username or password"
            )

    return render_template("admin_login.html")


# =========================
# ADMIN DASHBOARD
# =========================

@app.route("/dashboard")
def dashboard():

    if not session.get("admin"):
        return redirect("/admin")

    return render_template("admin.html")


# =========================
# LOGOUT
# =========================

@app.route("/logout")
def logout():

    session.pop("admin", None)

    return redirect("/admin")


@app.route("/add-photo", methods=["GET", "POST"])
def add_photo():

    if not session.get("admin"):
        return redirect("/admin")

    if request.method == "POST":

        event_name = request.form["event_name"]
        photo = request.files["photo"]

        if photo:

            filename = photo.filename

            # Save photo in static/image
            photo.save("static/image/" + filename)

            # Save information in MySQL
            db = get_db_connection()
            cursor = db.cursor()

            cursor.execute(
                "INSERT INTO gallery (event_name, image_name) VALUES (%s, %s)",
                (event_name, filename)
            )

            db.commit()

            cursor.close()
            db.close()

        return redirect("/dashboard")

    return render_template("add_photo.html")
#==========================================
#add video
#==========================================


@app.route("/add-video", methods=["GET", "POST"])
def add_video():

    if not session.get("admin"):
        return redirect("/admin")

    if request.method == "POST":

        event_name = request.form["event_name"]
        video = request.files["video"]

        if video:

            filename = video.filename

            # Save video in static/video
            video.save("static/video/" + filename)

            # Save information in MySQL
            db = get_db_connection()
            cursor = db.cursor()

            cursor.execute(
                "INSERT INTO videos (event_name, video_name) VALUES (%s, %s)",
                (event_name, filename)
            )

            db.commit()

            cursor.close()
            db.close()

        return redirect("/dashboard")

    return render_template("add_video.html")
 
# =========================
# MANAGE PHOTOS
# =========================

@app.route("/manage-photos")
def manage_photos():

    if not session.get("admin"):
        return redirect("/admin")

    image_folder = "static/image"

    photos = os.listdir(image_folder)

    return render_template(
        "manage_photos.html",
        photos=photos
    )


# =========================
# DELETE PHOTO
# =========================

@app.route("/delete-photo/<filename>")
def delete_photo(filename):

    if not session.get("admin"):
        return redirect("/admin")

    file_path = os.path.join("static/image", filename)

    if os.path.exists(file_path):
        os.remove(file_path)

    return redirect("/manage-photos")


# =========================
# MANAGE VIDEOS
# =========================

@app.route("/manage-videos")
def manage_videos():

    if not session.get("admin"):
        return redirect("/admin")

    video_folder = "static/video"

    videos = os.listdir(video_folder)

    return render_template(
        "manage_videos.html",
        videos=videos
    )


# =========================
# DELETE VIDEO
# =========================

@app.route("/delete-video/<filename>")
def delete_video(filename):

    if not session.get("admin"):
        return redirect("/admin")

    file_path = os.path.join("static/video", filename)

    if os.path.exists(file_path):
        os.remove(file_path)

    return redirect("/manage-videos")
#==========================
#view students
#=========================

@app.route("/view-students")
def view_students():

    if not session.get("admin"):
        return redirect("/admin")

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT * FROM admissions ORDER BY created_at DESC")

    students = cursor.fetchall()

    cursor.close()
    db.close()

    return render_template(
        "view_students.html",
        students=students
    )

# =========================
# RUN FLASK
# =========================

if __name__ == "__main__":
    app.run(debug=True)