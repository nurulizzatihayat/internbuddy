from flask import Flask, render_template, request, redirect, session, flash, url_for
from itsdangerous import URLSafeTimedSerializer
from config import Config
from models import db, User, Application
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mail import Mail, Message

app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = "careerwoman"

mail = Mail(app)
mail.init_app(app)    
db.init_app(app)

#Dashboard
@app.route("/")
def home():
    if "username_session" not in session:

        return render_template(
            "index.html",
            total_applications=12,
            status_counts = {
                "listed": Application.query.filter_by(username="Jwoo", status="listed").count(),
                "applied": Application.query.filter_by(username="Jwoo", status="applied").count(),
                "interview": Application.query.filter_by(username="Jwoo", status="interview").count(),
                "offered": Application.query.filter_by(username="Jwoo", status="offered").count(),
                "rejected": Application.query.filter_by(username="Jwoo", status="rejected").count(),
                "accepted": Application.query.filter_by(username="Jwoo", status="accepted").count(),
            },
            recent_applications=Application.query.filter_by(
                username="Jwoo"
            ).order_by(
                Application.last_updated.asc()
            ).limit(5).all(),
            success_rate=25,
            recommendation=Application.query.all()
        )

    recommendation=Application.query.all()
    
    total_applications = Application.query.filter_by(
        username=session["username_session"]
    ).count()

    status_counts = {
        "listed": Application.query.filter_by(username=session["username_session"], status="listed").count(),
        "applied": Application.query.filter_by(username=session["username_session"], status="applied").count(),
        "interview": Application.query.filter_by(username=session["username_session"], status="interview").count(),
        "offered": Application.query.filter_by(username=session["username_session"], status="offered").count(),
        "rejected": Application.query.filter_by(username=session["username_session"], status="rejected").count(),
        "accepted": Application.query.filter_by(username=session["username_session"], status="accepted").count(),
    }

    recent_applications = Application.query.filter_by(
        username=session["username_session"]
    ).order_by(Application.last_updated.desc()).limit(5).all()

    return render_template(
        "index.html", 
        total_applications=total_applications, 
        status_counts=status_counts, 
        recent_applications=recent_applications,
        recommendation=recommendation
    )

#Register
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == 'POST':
        #Get data from text field
        email = request.form["email"]
        username = request.form["username"]
        password = request.form["pwd"]

        #Validating data
        existing_email = User.query.filter_by(email=email).first()
        existing_username = User.query.filter_by(username=username).first()

        if existing_email:
            flash("Email already exists.", "danger")
            return redirect("/register")
        if existing_username:
            flash("Username is already taken.", "danger")
            return redirect("/register")
        if len(password) < 8:
            flash("Password must be at least 8 characters.", "danger")
            return redirect("/register")

        
        hashed_password = generate_password_hash(password)
        new_user = User(email=email, pwd=hashed_password, username=username)

        db.session.add(new_user)
        db.session.commit()

        flash("Account created successfully!", "success")
        return redirect("/login")
    return render_template("register.html")

#Login
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        #Get data
        username = request.form["username"]
        password = request.form["pwd"]

        #Validating username
        user = User.query.filter_by(username=username).first()
        
        #Failed login
        if not user:
            flash("Invalid username", "danger")
            return redirect("/login")
        if not check_password_hash(user.pwd, password):
            flash("Incorrect password", "danger")
            return redirect("/login")
        
        #Success login
        if user and check_password_hash(user.pwd, password):
            #Session
            session["username_session"] = user.username
            flash("Successful log in", "success")
            return redirect("/")
    return render_template("login.html")

#Logout
@app.route("/logout")
def logout():
    session.clear()
    flash("Successfully logged out.", "success")
    return redirect("/")

#Forgot password
@app.route('/forgotpassword', methods=['GET', 'POST'])
def forgotpassword():
    if request.method == 'POST':
        email = request.form['email']
        user = User.query.filter_by(email=email).first()

        if not user:
            flash("Email not found.", "danger")
            return redirect(url_for('forgotpassword'))

        serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
        token = serializer.dumps(email, salt='password-reset-salt')
        reset_url = url_for('resetpassword', token=token, _external=True )

        try:
            with open("static/reset-pwd.txt", "r") as file:
                email_body = file.read()
                email_body = email_body.replace("{{ url }}",  reset_url )

            msg = Message(
                subject="Password Reset Request",
                recipients=[email],
                body=email_body
            )

            mail.send(msg)

            flash("Password reset email sent successfully.", "success" )
            return redirect(url_for('login'))

        except Exception as e:
            print("EMAIL ERROR:", e)
            flash(f"Error sending email: {str(e)}", "danger")
            return redirect(url_for('forgotpassword'))
        
    return render_template('forgotpassword.html')

#Reset password
@app.route('/forgotpassword/<token>', methods=['GET', 'POST'])
def resetpassword(token):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    try:
        email = serializer.loads(token, salt='password-reset-salt', max_age=3600 )

    except:
        flash("Reset link expired or invalid.", "danger")
        return redirect(url_for('forgotpassword'))

    if request.method == 'POST':
        password = request.form['password']
        hashed_password = generate_password_hash(password)
        user = User.query.filter_by(email=email).first()
        user.pwd = hashed_password
        db.session.commit()
        flash("Password updated successfully.", "success")
        return redirect(url_for('login'))
    return render_template('resetpassword.html', token=token)

#Bug report
@app.route('/reportbug', methods=['GET', 'POST'])
def reportbug():
    if request.method == 'POST':
        bug_description = request.form['bug_description']
        try:
            with open("static/bugreport.txt", "r") as file:
                email_body = file.read()
                email_body = email_body.replace("{{ description }}",  bug_description )

            msg = Message(
                subject="New Bug Report",
                recipients=[app.config['MAIL_USERNAME']],
                body=email_body
            )

            mail.send(msg)

            flash("Bug report sent successfully.", "success" )
            return redirect("/")

        except Exception as e:
            flash(f"Error sending bug report: {str(e)}", "danger")
            return redirect("/reportbug")
        
    return render_template('bugreport.html')

#View application
@app.route("/application", methods=["GET", "POST"])
def application():
    if "username_session" not in session:
        return redirect("/login")
    
    if request.method == "POST":
        appid = request.form["app_id"]
        application = Application.query.filter_by(
            id=appid,
            username=session["username_session"]
        ).first()
        if application:
            new_status = request.form["status"]
            application.status = new_status
            db.session.commit()
            flash("Status updated.", "success")

    search_query = request.args.get("searchbar", "")
    filter_status = request.args.get("statusFilter", "")

    query = Application.query.filter_by(
        username=session["username_session"]
    ).order_by(Application.last_updated.desc())

    # search filter
    if search_query:
        query = query.filter(
            (Application.company.ilike(f"%{search_query}%")) |
            (Application.role.ilike(f"%{search_query}%"))
        )

    # status filter
    if filter_status:
        query = query.filter(Application.status == filter_status)

    applications = query.all()
    
    return render_template(
        "application.html",
        applications=applications,
        current_status=filter_status,
        search_query=search_query
    )

#Add application
@app.route("/addApplication", methods=["GET", "POST"])
def add():
    if request.method == 'POST':
        #Get data from text field
        company = request.form["company"]
        location = request.form["location"]
        role = request.form["role"]
        category = request.form["category"]
        allowance = request.form["allowance"]
        website = request.form["website"]
        
        new_application = Application(
            username= session["username_session"],
            company=company, 
            role=role, 
            location=location,
            category=category,
            allowance=allowance,
            website=website
        )

        db.session.add(new_application)
        db.session.commit()

        flash("Application added successfully!", "success")
    return redirect("/application")

#Manage application (update/delete)
@app.route("/manage/<int:id>", methods=["POST"])
def manage(id):

    if "username_session" not in session:
        return redirect("/login")

    application = Application.query.filter_by(
        id=id,
        username=session["username_session"]
    ).first()

    if not application:
        flash("Application not found.", "danger")
        return redirect("/application")

    # DELETE
    if "deletebtn" in request.form:

        db.session.delete(application)
        db.session.commit()

        flash("Application deleted.", "success")

    # UPDATE
    elif "updatebtn" in request.form:

        application.role = request.form["role"]
        application.location = request.form["location"]
        application.category = request.form["category"]
        application.allowance = request.form["allowance"]
        application.website = request.form["website"]

        db.session.commit()

        flash("Application updated.", "success")

    return redirect("/application")

if __name__ == "__main__":
    app.run(debug=True)