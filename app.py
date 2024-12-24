from flask import Flask, render_template, request
import math

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Get form data
        principal = float(request.form["principal"])
        annual_rate = float(request.form["annual_rate"]) / 100  # Convert percentage to decimal
        years = int(request.form["years"])
        contribution_amount = float(request.form["contribution_amount"])
        contribution_frequency = request.form["contribution_frequency"]
        compounding_frequency = request.form["compounding_frequency"]
        inflation_rate = float(request.form["inflation_rate"]) / 100  # Convert percentage to decimal
        currency = request.form["currency"]
        
        # Adjust for contribution frequency
        if contribution_frequency == "monthly":
            contribution_n = 12
        elif contribution_frequency == "semi-annually":
            contribution_n = 2
        elif contribution_frequency == "quarterly":
            contribution_n = 4
        elif contribution_frequency == "weekly":
            contribution_n = 52
        else:
            contribution_n = 1  # Annually
        
        # Adjust for compounding frequency
        if compounding_frequency == "monthly":
            n = 12
        elif compounding_frequency == "quarterly":
            n = 4
        elif compounding_frequency == "semi-annually":
            n = 2
        elif compounding_frequency == "weekly":
            n = 52
        elif compounding_frequency == "daily":
            n = 365
        else:
            n = 1  # Annually

        # Calculate the balances for each year
        starting_balance_without_inflation = principal
        starting_balance_with_inflation = principal
        yearly_summary_without_inflation = {}
        yearly_summary_with_inflation = {}

        for year in range(1, years + 1):
            total_contributions = contribution_amount * contribution_n * year

            # Interest calculations
            interest_earned_without_inflation = starting_balance_without_inflation * (1 + annual_rate / n) ** (n * year) - starting_balance_without_inflation
            interest_earned_with_inflation = starting_balance_with_inflation * (1 + annual_rate / n) ** (n * year) - starting_balance_with_inflation

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

        return render_template(
            "result.html",
            principal=principal,
            annual_rate=annual_rate * 100,
            years=years,
            compounding_frequency=compounding_frequency,
            contribution_amount=contribution_amount,
            inflation_rate=inflation_rate * 100,
            currency=currency,
            final_balance_without_inflation=final_balance_without_inflation,
            final_balance_with_inflation=final_balance_with_inflation,
            yearly_summary_without_inflation=yearly_summary_without_inflation,
            yearly_summary_with_inflation=yearly_summary_with_inflation
        )
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
