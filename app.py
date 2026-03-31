from flask import render_template
from flask import request, redirect, url_for
from flask import Flask
import os
import json
app = Flask(__name__)


def load_expenses():
    if not os.path.exists("expenses.json"):
        return []

    with open("expenses.json", "r") as f:
        return json.load(f)

def save_expenses(expenses):
    with open("expenses.json", "w") as f:
        json.dump(expenses, f, indent=2)



def calculate_summary(expenses):

    print(expenses)
    total = 0
    for item in expenses:
        total += item["amount"]

    category_totals = {}

    for item in expenses:
        c = item["category"]
        category_totals[c] = category_totals.get(c, 0) + item["amount"]

    return total, category_totals




expenses = load_expenses()


@app.route("/")
def index():
    return render_template("index.html", expenses = expenses)

@app.route("/add", methods=["POST"])
def add():
    amount = float(request.form["amount"])
    category = request.form["category"]
    note = request.form["note"]
    
    record = {}
    record["amount"] = amount
    record["category"] = category
    record["note"] = note
    expenses.append(record)

    save_expenses(expenses)

    # print(amount, category, note)  

    return redirect(url_for("index"))

@app.route("/summary")
def summary():

    total, category_totals = calculate_summary(expenses)

    print(category_totals)
    return render_template(
        "summary.html",
        total=total,
        category_totals=category_totals
    )
