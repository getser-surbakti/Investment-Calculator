from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Get form data
        principal = float(request.form["principal"])
        annual_rate = float(request.form["annual_rate"])/100  # Convert percentage to decimal
        years = int(request.form["years"])
        contribution_amount = float(request.form["contribution_amount"])
        contribution_frequency = request.form["contribution_frequency"]
        compounding_frequency = request.form["compounding_frequency"]
        inflation_rate = float(request.form["inflation_rate"])/100  # Convert percentage to decimal
        currency = request.form["currency"]

        # Adjust for contribution frequency
        contribution_n = {
            "monthly": 12,
            "quarterly": 4,
            "semi-annually": 2,
            "weekly": 52,
            "daily": 365,
            "annually": 1
        }.get(contribution_frequency, 1)

        # Adjust for compounding frequency
        n = {
            "monthly": 12,
            "quarterly": 4,
            "semi-annually": 2,
            "weekly": 52,
            "daily": 365,
            "annually": 1
        }.get(compounding_frequency, 1)

        # Calculate the balances for each year
        starting_balance_without_inflation = principal
        starting_balance_with_inflation = principal
        yearly_summary_without_inflation = {}
        yearly_summary_with_inflation = {}

        for year in range(1, years + 1):
            # Contributions for the current year
            total_contributions = contribution_amount * contribution_n

            # Interest calculations for the current year
            interest_earned_without_inflation = starting_balance_without_inflation * ((1 + annual_rate / n) ** n - 1)
            interest_earned_with_inflation = starting_balance_with_inflation * ((1 + annual_rate / n) ** n - 1)

            # Ending balances
            ending_balance_without_inflation = starting_balance_without_inflation + interest_earned_without_inflation + total_contributions
            ending_balance_with_inflation = (starting_balance_with_inflation + interest_earned_with_inflation + total_contributions) / (1 + inflation_rate)

            # Store yearly results
            yearly_summary_without_inflation[year] = {
                'starting_balance': starting_balance_without_inflation,
                'interest_earned': interest_earned_without_inflation,
                'contributions': total_contributions,
                'ending_balance': ending_balance_without_inflation
            }

            yearly_summary_with_inflation[year] = {
                'starting_balance': starting_balance_with_inflation,
                'interest_earned': interest_earned_with_inflation,
                'contributions': total_contributions,
                'ending_balance': ending_balance_with_inflation
            }

            # Update for the next year
            starting_balance_without_inflation = ending_balance_without_inflation
            starting_balance_with_inflation = ending_balance_with_inflation

        final_balance_without_inflation = yearly_summary_without_inflation[years]['ending_balance']
        final_balance_with_inflation = yearly_summary_with_inflation[years]['ending_balance']

        total_contributions = contribution_amount * contribution_n * years
        total_capital = principal + total_contributions

        return render_template(
    'result.html',
    principal=principal,
    contribution_amount=contribution_amount,
    contribution_n=contribution_n,
    years=years,
    final_balance_without_inflation=final_balance_without_inflation,
    final_balance_with_inflation=final_balance_with_inflation,
    currency=currency,
    inflation_rate=inflation_rate,
    annual_rate=annual_rate,
    compounding_frequency=compounding_frequency,
    contribution_frequency=contribution_frequency,
    yearly_summary_without_inflation=yearly_summary_without_inflation,
    yearly_summary_with_inflation=yearly_summary_with_inflation,
    total_capital=total_capital,
    total_contributions=total_contributions

)

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
