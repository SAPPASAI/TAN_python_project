from flask import Flask, render_template, request, redirect, url_for, session, flash, abort
import psycopg2
import os
from dotenv import load_dotenv



load_dotenv()
app = Flask(__name__)
app.secret_key = os.urandom(24) 

# PostgreSQL Database Configuration
app.config['DATABASE_URL'] = os.getenv("DATABASE_URL", "dbname=your_db user=your_user password=your_pass host=localhost")
#postgresql://my_flask_db_7rzp_user:K7Ty2AG6FHg4cDOzfcN8FjBM44vlCP27@dpg-d0phic0dl3ps73aq24lg-a.singapore-postgres.render.com/my_flask_db_7rzp

# Helper: Get DB connection
def get_db():
    return psycopg2.connect(app.config['DATABASE_URL'])

# Routes
# @app.route('/initdb')
def init_db():
    db = get_db()
    cur = db.cursor()

    # Create members table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS members (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100),
            email VARCHAR(100),
            phone VARCHAR(20),
            address TEXT,
            gender VARCHAR(10),
            membership_type VARCHAR(50),
            message TEXT
        )
    """)

    # Add other tables similarly
    cur.execute("""CREATE TABLE IF NOT EXISTS sponsors (
        id SERIAL PRIMARY KEY,
        name VARCHAR(100),
        logo VARCHAR(255),
        description TEXT,
        website VARCHAR(255)
    )""")

    cur.execute("""
    CREATE TABLE IF NOT EXISTS events (
        id SERIAL PRIMARY KEY,
        title VARCHAR(100),
        start TIMESTAMP,
        "end" TIMESTAMP
    )
""")

    cur.execute("""CREATE TABLE IF NOT EXISTS temples (
        id SERIAL PRIMARY KEY,
        name VARCHAR(100),
        location VARCHAR(100),
        image_url VARCHAR(255),
        description TEXT
    )""")

    cur.execute("""CREATE TABLE IF NOT EXISTS gallery_old (
        id SERIAL PRIMARY KEY,
        filename VARCHAR(255),
        title VARCHAR(100)
    )""")

    cur.execute("""CREATE TABLE IF NOT EXISTS gallery_current (
        id SERIAL PRIMARY KEY,
        filename VARCHAR(255),
        title VARCHAR(100)
    )""")

    cur.execute("""CREATE TABLE IF NOT EXISTS articles (
        id SERIAL PRIMARY KEY,
        title VARCHAR(100),
        excerpt TEXT,
        image_url VARCHAR(255),
        tags TEXT
    )""")

    cur.execute("""CREATE TABLE IF NOT EXISTS contacts (
        id SERIAL PRIMARY KEY,
        name VARCHAR(100),
        designation VARCHAR(100),
        phone VARCHAR(20),
        email VARCHAR(100),
        photo VARCHAR(255),
        facebook VARCHAR(255),
        twitter VARCHAR(255),
        linkedin VARCHAR(255),
        instagram VARCHAR(255)
    )""")

    cur.execute("""CREATE TABLE IF NOT EXISTS emergency_contacts (
        id SERIAL PRIMARY KEY,
        name VARCHAR(100),
        description TEXT,
        phone VARCHAR(20)
    )""")

    cur.execute("""CREATE TABLE IF NOT EXISTS jobs (
        id SERIAL PRIMARY KEY,
        title VARCHAR(100),
        company VARCHAR(100),
        location VARCHAR(100),
        type VARCHAR(10),
        apply_link VARCHAR(255)
    )""")

    db.commit()
    cur.close()
    db.close()
    return "Tables created!"


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/founders')
def founders():
    return render_template('founder.html')

@app.route('/trustees')
def trustees():
    return render_template('trusts.html')

@app.route('/previous-leadership')
def previous_leaderships():
    return render_template('previous_leaders.html')

@app.route('/present-leadership')
def present_leaderships():
    return render_template('present_leaders.html')

@app.route('/membership-benefits')
def membership_benefits():
    return render_template('membership_benefits.html')

@app.route("/membership-form", methods=["GET", "POST"])
def membership():
    if request.method == "POST":
        full_name = request.form["full_name"]
        email = request.form["email"]
        phone = request.form["phone"]
        address = request.form.get("address", "")
        gender = request.form.get("gender", "")
        membership_type = request.form.get("membership_type", "")
        message = request.form.get("message", "")

        db = get_db()
        cur = db.cursor()
        cur.execute("INSERT INTO members (name, email, phone, address, gender, membership_type, message) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                    (full_name, email, phone, address, gender, membership_type, message))
        db.commit()
        cur.close()
        db.close()

        return render_template("membership_form.html", success=True, name=full_name)
    return render_template("membership_form.html", success=False)

@app.route('/members-details')
def members_details():
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT * FROM members")
    members = [{"id": row[0], "name": row[1], "email": row[2], "phone": row[3], "address": row[4],
                "gender": row[5], "membership_type": row[6], "message": row[7]} for row in cur.fetchall()]
    cur.close()
    db.close()
    return render_template('members_details.html', members=members)

@app.route('/sponsors-slider')
def sponsors_slider():
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT * FROM sponsors")
    sponsors = [{"id": row[0], "name": row[1], "logo": row[2]} for row in cur.fetchall()]
    cur.close()
    db.close()
    return render_template('sponsors_slider.html', sponsors=sponsors)

@app.route('/sponsors-details')
def sponsor_details():
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT * FROM sponsors")
    sponsors = [{"id": row[0], "name": row[1], "description": row[2], "logo": row[3], "website": row[4]}
                for row in cur.fetchall()]
    cur.close()
    db.close()
    return render_template('sponsors_details.html', sponsors=sponsors)

@app.route('/gallery-old')
def gallery_old():
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT * FROM gallery_old")
    images = [{"id": row[0], "filename": row[1], "title": row[2]} for row in cur.fetchall()]
    cur.close()
    db.close()
    return render_template('gallery_old.html', images=images)

@app.route('/gallery-current')
def gallery_current():
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT * FROM gallery_current")
    images = [{"id": row[0], "filename": row[1], "title": row[2]} for row in cur.fetchall()]
    cur.close()
    db.close()
    return render_template('current_gallery.html', images=images)

@app.route("/events")
def events_calendar():
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT * FROM events")
    events = [{"id": row[0], "title": row[1], "start": row[2], "end": row[3]} for row in cur.fetchall()]
    cur.close()
    db.close()
    return render_template("event.html", events=events)

@app.route('/telugu-calendar')
def telugu_calendar():
    return render_template('telugu_calendar.html')

@app.route("/temples")
def temples():
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT * FROM temples")
    temples_data = [{"id": row[0], "name": row[1], "location": row[2], "image_url": row[3], "description": row[4]}
                    for row in cur.fetchall()]
    cur.close()
    db.close()
    return render_template("temples.html", temples=temples_data)

@app.route("/articles")
def articles():
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT * FROM articles")
    articles_list = [{"id": row[0], "title": row[1], "excerpt": row[2], "image_url": row[3], "tags": row[4]}
                     for row in cur.fetchall()]
    cur.close()
    db.close()
    tags = set()
    for article in articles_list:
        tags.update(article['tags'].split(","))
    return render_template("articles.html", articles=articles_list, tags=sorted(tags))

@app.route("/contact")
def contact_ids():
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT * FROM contacts")
    contacts = [{"id": row[0], "name": row[1], "designation": row[2], "phone": row[3],
                 "email": row[4], "photo": row[5], "social": {"facebook": row[6], "twitter": row[7],
                                                           "linkedin": row[8], "instagram": row[9]}}
                for row in cur.fetchall()]
    cur.close()
    db.close()
    return render_template("contact_id.html", contacts=contacts)

@app.route("/emergency-contacts")
def emergency_contacts():
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT * FROM emergency_contacts")
    emergency_contacts = [{"id": row[0], "name": row[1], "description": row[2], "phone": row[3]}
                          for row in cur.fetchall()]
    cur.close()
    db.close()
    return render_template("emergency_contact.html", emergency_contacts=emergency_contacts)

@app.route("/jobs")
def all_jobs():
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT * FROM jobs WHERE type = 'IT'")
    it_jobs = [{"id": row[0], "title": row[1], "company": row[2], "location": row[3], "type": row[4],
                "apply_link": row[5]} for row in cur.fetchall()]
    cur.execute("SELECT * FROM jobs WHERE type = 'Non-IT'")
    non_it_jobs = [{"id": row[0], "title": row[1], "company": row[2], "location": row[3], "type": row[4],
                    "apply_link": row[5]} for row in cur.fetchall()]
    cur.close()
    db.close()
    return render_template("jobs.html", it_jobs=it_jobs, non_it_jobs=non_it_jobs)

# Admin Section

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'admin' and password == 'password123':
            session['is_admin'] = True
            return redirect(url_for('admin_dashboard'))
        else:
            error = 'Invalid Credentials'
    return render_template('admin/login.html', error=error)

@app.route('/admin/logout')
def admin_logout():
    session.pop('is_admin', None)
    return redirect(url_for('admin_login'))

@app.route('/admin/dashboard')
def admin_dashboard():
    if not session.get('is_admin'):
        abort(403)
    return render_template('admin/dashboard.html')

@app.route('/admin/members')
def admin_members_details():
    if not session.get('is_admin'):
        abort(403)

    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT * FROM members")
    members = [{"id": row[0], "name": row[1], "email": row[2], "phone": row[3], "address": row[4],
                "gender": row[5], "membership_type": row[6], "message": row[7]} for row in cur.fetchall()]
    cur.close()
    db.close()
    return render_template('admin/members.html', members=members)

@app.route('/admin/member/delete/<int:id>')
def delete_member(id):
    if not session.get('is_admin'):
        abort(403)
    db = get_db()
    cur = db.cursor()
    cur.execute("DELETE FROM members WHERE id=%s", (id,))
    db.commit()
    cur.close()
    db.close()
    return redirect(url_for('admin_members_details'))

@app.route('/admin/member/edit/<int:id>', methods=['GET', 'POST'])
def edit_member(id):
    if not session.get('is_admin'):
        abort(403)

    db = get_db()
    cur = db.cursor()

    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        gender = request.form['gender']
        membership_type = request.form['membership_type']
        message = request.form.get('message', '')

        cur.execute(
            "UPDATE members SET name=%s, email=%s, phone=%s, gender=%s, membership_type=%s, message=%s WHERE id=%s",
            (name, email, phone, gender, membership_type, message, id)
        )
        db.commit()
        cur.close()
        db.close()
        return redirect(url_for('admin_members_details'))

    cur.execute("SELECT * FROM members WHERE id=%s", (id,))
    member = cur.fetchone()
    member_dict = {
        "id": member[0],
        "name": member[1],
        "email": member[2],
        "phone": member[3],
        "gender": member[5],
        "membership_type": member[6],
        "message": member[7]
    }
    cur.close()
    db.close()
    return render_template('admin/edit_member.html', member=member_dict)

@app.route('/admin/member/add', methods=['GET', 'POST'])
def add_member():
    if not session.get('is_admin'):
        abort(403)
    if request.method == 'POST':
        name = request.form['full_name']
        email = request.form['email']
        phone = request.form['phone']
        address = request.form.get('address', '')
        gender = request.form.get('gender', '')
        membership_type = request.form.get('membership_type', '')
        message = request.form.get('message', '')

        db = get_db()
        cur = db.cursor()
        cur.execute("INSERT INTO members (name, email, phone, address, gender, membership_type, message) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                    (name, email, phone, address, gender, membership_type, message))
        db.commit()
        cur.close()
        db.close()
        return redirect(url_for('admin_members_details'))

    return render_template('admin/add_member.html')

if __name__ == '__main__':
    app.run(debug=True)
