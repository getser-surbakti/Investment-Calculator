from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/result', methods=['POST'])
def result():
    initial_amount = float(request.form['initial_amount'])
    years = int(request.form['years'])
    return_rate = float(request.form['return_rate']) / 100
    interest_type = request.form['interest_type']
    currency = request.form['currency']

    compound_option = request.form.get('compound_options', 'annually')
    compound_periods = {
        'daily': 365,
        'weekly': 52,
        'monthly': 12,
        'quarterly': 4,
        'semi-annually': 2,
        'annually': 1
    }
    n = compound_periods.get(compound_option, 1)

    yearly_balances = []

    if interest_type == 'compound':
        for year in range(1, years + 1):
            yearly_balance = initial_amount * (1 + return_rate / n) ** (n * year)
            yearly_balances.append(yearly_balance)
    else:
        for year in range(1, years + 1):
            yearly_balance = initial_amount + (initial_amount * return_rate * year)
            yearly_balances.append(yearly_balance)

    final_amount = yearly_balances[-1] if yearly_balances else initial_amount

    return render_template('result.html', initial_amount=initial_amount, years=years,
                           return_rate=return_rate * 100, interest_type=interest_type,
                           compound_option=compound_option, final_amount=final_amount,
                           yearly_balances=yearly_balances, currency=currency, enumerate=enumerate)

if __name__ == '__main__':
    app.run(debug=True)
