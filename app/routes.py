from datetime import date
from flask import Blueprint, render_template, request, redirect, url_for, flash
from . import db
from .models import Habit, HabitCheckin

bp = Blueprint("main", __name__)

@bp.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        if not name:
            flash("Please enter a habit name.", "error")
        else:
            existing = Habit.query.filter_by(name=name).first()
            if existing:
                flash("That habit already exists.", "error")
            else:
                db.session.add(Habit(name=name))
                db.session.commit()
                flash("Habit added!", "success")
        return redirect(url_for("main.index"))

    habits = Habit.query.order_by(Habit.created_at.desc()).all()
    today = date.today()
    checked_today = {
        h.id: HabitCheckin.query.filter_by(habit_id=h.id, day=today).first() is not None
        for h in habits
    }
    return render_template("index.html", habits=habits, checked_today=checked_today)

@bp.post("/checkin/<int:habit_id>")
def checkin(habit_id):
    today = date.today()
    habit = Habit.query.get(habit_id)
    if not habit:
        flash("Habit not found.", "error")
        return redirect(url_for("main.index"))

    existing = HabitCheckin.query.filter_by(habit_id=habit_id, day=today).first()
    if existing:
        db.session.delete(existing)
        db.session.commit()
        flash("Unchecked for today.", "info")
    else:
        db.session.add(HabitCheckin(habit_id=habit_id, day=today))
        db.session.commit()
        flash("Checked in for today!", "success")

    return redirect(url_for("main.index"))

@bp.route("/stats")
def stats():
    total_habits = Habit.query.count()
    total_checkins = HabitCheckin.query.count()
    return render_template("stats.html",
                           total_habits=total_habits,
                           total_checkins=total_checkins)
