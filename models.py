from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "users"

    username = db.Column(db.String(255), primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    pwd = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # relationship to Application
    applications = db.relationship(
        "Application",
        backref="user",
        cascade="all, delete",
        passive_deletes=True
    )


class Application(db.Model):
    __tablename__ = "application"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(
        db.Integer,
        db.ForeignKey("users.username", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False
    )

    company = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(255))
    location = db.Column(db.String(255))
    category = db.Column(db.String(255))
    allowance = db.Column(db.Numeric(10, 2))
    website = db.Column(db.String(255))

    status = db.Column(
        db.Enum("listed", "applied", "interview", "offered", "rejected", "accepted"),
        default="listed"
    )

    last_updated = db.Column(
        db.Date,
        default=date.today,
        onupdate=date.today,
    )