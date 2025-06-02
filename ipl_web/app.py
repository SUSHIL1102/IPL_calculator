from flask import Flask, render_template, request
import io
import sys
import math

app = Flask(__name__)

# ───── YOUR UNCHANGED FUNCTIONS ─────

def crypto_converter(inr_list):
    result = []
    for inr in inr_list:
        usdt = inr * 0.01168
        result.append(f"{inr} INR ---->  {usdt:.4f} USDT")
    return result


def Bet_calculator(t1, o1, t2, o2):
    teams = ["PBKS", "RCB", "GT", "MI", "DC", "SRH", "LSG", "KKR", "RR", "CSK"]
    if t1 not in teams or t2 not in teams:
        return "Invalid team names!"

    o1 = float(o1)
    o2 = float(o2)

    BetA = max(500, (500 * o2) / o1)
    BetB = BetA * (o1 / o2)

    payout_A = BetA * o1
    payout_B = BetB * o2

    PA1 = BetA * (o1 - 1)
    PB1 = -BetB

    bonus_payout_B = min(payout_B, 2100)
    PB2 = bonus_payout_B - BetB
    PA2 = PA1

    PA3 = -BetA
    PB3 = BetB * (o2 - 1)

    bonus_payout_A = min(payout_A, 2100)
    PA4 = bonus_payout_A - BetA
    PB4 = PB3

    def transfer_to_A(PA, PB):
        return (PA + PB) / 2 - PA

    results = [
        f"Person A should bet ₹{BetA:.2f} on {t1}",
        f"Person B should bet ₹{BetB:.2f} on {t2}",
        "",
        f"Scenario 1: {t1} wins, {t2} hits no six\n  A profit = {PA1:.2f}, B profit = {PB1:.2f}, Transfer to A = {transfer_to_A(PA1, PB1):.2f}",
        f"Scenario 2: {t1} wins, {t2} hits six\n  A profit = {PA2:.2f}, B profit = {PB2:.2f}, Transfer to A = {transfer_to_A(PA2, PB2):.2f}",
        f"Scenario 3: {t2} wins, {t1} hits no six\n  A profit = {PA3:.2f}, B profit = {PB3:.2f}, Transfer to A = {transfer_to_A(PA3, PB3):.2f}",
        f"Scenario 4: {t2} wins, {t1} hits six\n  A profit = {PA4:.2f}, B profit = {PB4:.2f}, Transfer to A = {transfer_to_A(PA4, PB4):.2f}",
    ]

    return results


# ───── ROUTES ─────

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/bet', methods=['GET', 'POST'])
def bet():
    result = None
    if request.method == 'POST':
        t1 = request.form['team1'].upper()
        o1 = request.form['odds1']
        t2 = request.form['team2'].upper()
        o2 = request.form['odds2']
        result = Bet_calculator(t1, o1, t2, o2)
    return render_template("bet.html", result=result)

@app.route('/convert', methods=['GET', 'POST'])
def convert():
    result = None
    if request.method == 'POST':
        try:
            values = [float(x.strip()) for x in request.form['values'].split(',')]
            result = crypto_converter(values)
        except ValueError:
            result = ["Invalid input. Please enter comma-separated numbers."]
    return render_template("convert.html", result=result)


if __name__ == "__main__":
    app.run(debug=True)
