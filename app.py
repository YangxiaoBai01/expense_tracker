from flask import render_template
from flask import request, redirect, url_for
from flask import Flask
import os
import json
import urllib.request
app = Flask(__name__)


def convert_to_usd(amount, currency):
    if currency == "USD":
        return amount
    url = f"https://api.frankfurter.app/latest?from={currency}&to=USD"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    response = urllib.request.urlopen(req)
    data = json.loads(response.read())
    rate = data["rates"]["USD"]
    return round(amount * rate, 2)


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
    currency = request.form["currency"]
    category = request.form["category"]
    note = request.form["note"]

    amount_usd = convert_to_usd(amount, currency)

    record = {}
    record["amount"] = amount_usd
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
