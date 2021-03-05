from flask import Flask, render_template, request
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
from os import path
from datetime import datetime, timedelta

def subtract_two_numbers(a, b):
    b = 0 if pd.isnull(b) else b
    return a - b

app = Flask(__name__)
# with open("/Users/petermyers/Desktop/high_quality_programs/24_nonessential_budget_tracker/secrets.txt") as file:
#     google_data = file.read().split()
# google_id = google_data[1]
# google_password = google_data[1]



@app.route('/')
def index():
    return render_template("index.html")

@app.route('/setup')
def setup():
    if path.exists("data.csv"):
        setup = pd.read_csv("data.csv").iloc[0].to_dict()
    else:
        setup = {'earnings': "2100",
             'purchase1': "Rent", 'cost1': "500", 'category1': "need",
             'purchase2': "", 'cost2': "", 'category2': "need",
             'purchase3': "", 'cost3': "", 'category3': "need",
             'purchase4': "", 'cost4': "", 'category4': "need",
             'purchase5': "", 'cost5': "", 'category5': "need",
             'purchase6': "", 'cost6': "", 'category6': "need",
             'purchase7': "", 'cost7': "", 'category7': "need",
             'purchase8': "", 'cost8': "", 'category8': "need",
             'purchase9': "", 'cost9': "", 'category9': "need",
             'purchase10': "", 'cost10': "", 'category10': "need",
             'saving': ""
             }
    return render_template("setup.html", setup=setup)

@app.route('/save-setup', methods = ['POST'])
def save_setup():
    result = request.form.to_dict(flat=True)
    if path.exists("data.csv"):
        result['created'] = pd.read_csv("data.csv").iloc[0].to_dict()['created']
    else:
        result['created'] = datetime.now().strftime("%Y-%m-%d")
    result = {k: [v] for (k, v) in result.items()}

    df = pd.DataFrame(result)
    df.to_csv("data.csv")
    return render_template("index.html")

@app.route('/main')
def main():
    # Calculate monthly total budget
    setup = pd.read_csv("data.csv").iloc[0].to_dict()
    total_budget = 0 if pd.isnull(setup['salary']) else setup['salary']
    for i in range(1, 11):
        total_budget -= 0 if pd.isnull(setup[f'cost{i}']) else setup[f'cost{i}']
    total_budget -= 0 if pd.isnull(setup['saving']) else setup['saving']

    # From created date:
    first_day_next_month_from_today = (datetime.now() + timedelta(days=35)).replace(day=1)
    created = datetime.strptime(setup['created'], "%Y-%m-%d")
    date = created.replace(day=1)
    dfs = []
    while date < first_day_next_month_from_today:
        print(date)
        # Calculate days this month and budget per day for the month
        first_day_next_month = (date + timedelta(days=35)).replace(day=1)
        first_day_this_month = date
        days_this_month = ((first_day_next_month - first_day_this_month) + timedelta(seconds=100)).days
        budget_per_day = total_budget / days_this_month

        # Forecast the earnings for every day of every month (Up until this month)
        temp_df = pd.DataFrame(pd.date_range(date, periods=days_this_month, freq='D'), columns=['date'])
        temp_df['new_funds'] = budget_per_day

        # Filter for all days prior to today (so remove rest of this month; showing some days for visual on first use).  Also starts on created date
        days_ahead = 0 if setup['created'] != datetime.now().strftime("%Y-%m-%d") else 2
        temp_df = temp_df.loc[temp_df['date'] <= (datetime.now() + timedelta(days=days_ahead)).strftime("%Y-%m-%d")]
        temp_df = temp_df.loc[temp_df['date'] >= setup['created']]

        # Final commands
        dfs.append(temp_df)
        date = first_day_next_month

    # Create dataframe
    df = pd.concat(dfs, axis='index')

    # Accumulate the funds based on new funds
    df['funds_with_no_spending'] = np.cumsum(df['new_funds'])

    # Minus out all purchases since beginning of time (Using a join)
    purchases = pd.read_csv("purchases.csv")
    purchases = pd.DataFrame(purchases.groupby(['date'])['cost'].sum()).reset_index()
    purchases['date'] = purchases['date'].astype(str)
    df['date'] = df['date'].astype(str)
    df = df.join(purchases.set_index(['date']), on='date', how='left')

    # Get the funds column
    df['funds'] = df[['funds_with_no_spending', 'cost']].apply(lambda x: subtract_two_numbers(*x), axis=1).astype(float)

    funds_as_of_today = df.loc[df['date'] == datetime.now().strftime("%Y-%m-%d")]
    df = df.set_index("date")
    matplotlib.use('Agg')
    plt.plot(df.funds)
    plt.savefig('app/static/plot.png')

    return render_template("main.html", funds_as_of_today=funds_as_of_today)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5001)
