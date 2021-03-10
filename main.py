from flask import Flask, render_template, request
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
from os import path
import os
from glob import glob
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
        setup = pd.read_csv("data.csv").fillna('').iloc[0].to_dict()
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
def main(chosen_month=None, chosen_year=None):
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

    # Get dates
    temp = sorted(df['date'])
    start_date = temp[0]
    end_date = temp[-1]
    all_dates = pd.DataFrame(pd.date_range(start_date, end_date), columns=['date'])
    all_dates['date'] = all_dates['date'].astype(str)

    # Minus out all purchases since beginning of time (Using a join)
    purchases = pd.read_csv("purchases.csv")
    purchases = pd.DataFrame(purchases.groupby(['date'])['cost'].sum()).reset_index()
    purchases['date'] = purchases['date'].astype(str)
    purchases = all_dates.join(purchases.set_index(['date']), on='date', how='left').fillna(0)
    purchases['cumulative_cost'] = np.cumsum(purchases['cost'])
    print(purchases)
    df['date'] = df['date'].astype(str)
    df = df.join(purchases.set_index(['date']), on='date', how='left')

    # Get the funds column
    df['funds'] = df[['funds_with_no_spending', 'cumulative_cost']].apply(lambda x: subtract_two_numbers(*x), axis=1).astype(float)

    funds_as_of_today = df.loc[df['date'] == datetime.now().strftime("%Y-%m-%d")].iloc[0].funds
    df = df.set_index("date")
    matplotlib.use('Agg')
    plt.plot(df.funds)

    # Get new name.  Delete old file
    my_directory = os.getcwd() + "/static/"

    files = glob(my_directory + "*")
    my_file = [x for x in files if ".png" in x][0]
    current_number = int(my_file[:-4].split("/static/plot")[1])
    os.remove(my_directory + "plot" + str(current_number) + ".png")
    plt.savefig(my_directory + "plot" + str(current_number+1) + ".png")
    plt.clf()

    # Initialize data
    data = {'funds_as_of_today': funds_as_of_today, 'filename': "plot" + str(current_number+1) + ".png",
    'date1': '', 'purchase1': '', 'cost1': '', 'category1': 'need',
    'date2': '', 'purchase2': '', 'cost2': '', 'category2': 'need',
    'date3': '', 'purchase3': '', 'cost3': '', 'category3': 'need',
    'date4': '', 'purchase4': '', 'cost4': '', 'category4': 'need',
    'date5': '', 'purchase5': '', 'cost5': '', 'category5': 'need',
    'date6': '', 'purchase6': '', 'cost6': '', 'category6': 'need',
    'date7': '', 'purchase7': '', 'cost7': '', 'category7': 'need',
    'date8': '', 'purchase8': '', 'cost8': '', 'category8': 'need',
    'date9': '', 'purchase9': '', 'cost9': '', 'category9': 'need',
    'date10': '', 'purchase10': '', 'cost10': '', 'category10': 'need',
    'date11': '', 'purchase11': '', 'cost11': '', 'category11': 'need',
    'date12': '', 'purchase12': '', 'cost12': '', 'category12': 'need',
    'date13': '', 'purchase13': '', 'cost13': '', 'category13': 'need',
    'date14': '', 'purchase14': '', 'cost14': '', 'category14': 'need',
    'date15': '', 'purchase15': '', 'cost15': '', 'category15': 'need',
    'date16': '', 'purchase16': '', 'cost16': '', 'category16': 'need',
    'date17': '', 'purchase17': '', 'cost17': '', 'category17': 'need',
    'date18': '', 'purchase18': '', 'cost18': '', 'category18': 'need',
    'date19': '', 'purchase19': '', 'cost19': '', 'category19': 'need',
    'date20': '', 'purchase20': '', 'cost20': '', 'category20': 'need',
    'date21': '', 'purchase21': '', 'cost21': '', 'category21': 'need',
    'date22': '', 'purchase22': '', 'cost22': '', 'category22': 'need',
    'date23': '', 'purchase23': '', 'cost23': '', 'category23': 'need',
    'date24': '', 'purchase24': '', 'cost24': '', 'category24': 'need',
    'date25': '', 'purchase25': '', 'cost25': '', 'category25': 'need',
    'purchase1b': '', 'cost1b': '', 'category1b': 'need',
    'purchase2b': '', 'cost2b': '', 'category2b': 'need',
    'purchase3b': '', 'cost3b': '', 'category3b': 'need',
    'purchase4b': '', 'cost4b': '', 'category4b': 'need',
    'purchase5b': '', 'cost5b': '', 'category5b': 'need',
    'purchase6b': '', 'cost6b': '', 'category6b': 'need',
    'purchase7b': '', 'cost7b': '', 'category7b': 'need',
    'purchase8b': '', 'cost8b': '', 'category8b': 'need',
    'purchase9b': '', 'cost9b': '', 'category9b': 'need',
    'purchase10b': '', 'cost10b': '', 'category10b': 'need',
    'purchase11b': '', 'cost11b': '', 'category11b': 'need',
    'purchase12b': '', 'cost12b': '', 'category12b': 'need',
    'purchase13b': '', 'cost13b': '', 'category13b': 'need',
    'purchase14b': '', 'cost14b': '', 'category14b': 'need',
    'purchase15b': '', 'cost15b': '', 'category15b': 'need',
    'purchase16b': '', 'cost16b': '', 'category16b': 'need',
    'purchase17b': '', 'cost17b': '', 'category17b': 'need',
    'purchase18b': '', 'cost18b': '', 'category18b': 'need',
    'purchase19b': '', 'cost19b': '', 'category19b': 'need',
    'purchase20b': '', 'cost20b': '', 'category20b': 'need',
    'purchase21b': '', 'cost21b': '', 'category21b': 'need',
    'purchase22b': '', 'cost22b': '', 'category22b': 'need',
    'purchase23b': '', 'cost23b': '', 'category23b': 'need',
    'purchase24b': '', 'cost24b': '', 'category24b': 'need',
    'purchase25b': '', 'cost25b': '', 'category25b': ''
    }

    if path.exists("purchases.csv"):

        if chosen_month == None and chosen_year == None:
            year = str(datetime.now().year)
            month = str(datetime.now().month).zfill(2)
        else:
            year = str(chosen_year)
            month = str(str(chosen_month).zfill(2))
        # Update data
        data['year'] = year
        data['month'] = month

        # Load purchases df to build data more
        df = pd.read_csv("purchases.csv")
        df['year'] = df['date'].apply(lambda x: x[0:4])
        df['month'] = df['date'].apply(lambda x: x[5:7])
        df['day'] = df['date'].apply(lambda x: x[8:10])
        df = df.loc[(df['year'] == year) & (df['month'] == month)]
        df.drop(['year', 'month'], axis='columns', inplace=True)
        df.fillna('', inplace=True)

        # Load wishlist df2 to build data more
        if path.exists("wishlist.csv"):
            wishlist_data = pd.read_csv("wishlist.csv").fillna('').iloc[0].to_dict()
            for key, value in wishlist_data.items():
                data[key] = value

        # Fill data
        for index, row in df.iterrows():
            row_number = index + 1
            data[f'date{row_number}'] = row['day']
            data[f'purchase{row_number}'] = row['purchase']
            data[f'cost{row_number}'] = row['cost']
            data[f'category{row_number}'] = row['category']

    return render_template("main.html", data=data)

@app.route('/load-month', methods = ['POST'])
def load_month():
    result = request.form.to_dict(flat=True)
    chosen_month = result['month-selector1']
    chosen_year = result['year-selector1']
    return main(chosen_month=chosen_month, chosen_year=chosen_year)

@app.route('/save-changes', methods = ['POST'])
def save_changes():
    # Open the purchases dataset
    if not path.exists("purchases.csv"):
        df = pd.DataFrame({'date': [], 'purchase': [], 'cost': [], 'category': [], 'year': [], 'month': []})
    else:
        df = pd.read_csv("purchases.csv")
        df['year'] = df['date'].apply(lambda x: x[0:4])
        df['month'] = df['date'].apply(lambda x: x[5:7])

    # Get POST result
    result = request.form.to_dict(flat=True)

    # Delete all records from the purchases dataset where the month and year match
    df = df.loc[(df['year'] != result['year-selector']) | (df['month'] != result['month-selector'])]

    # drop the year and month columns
    df.drop(['year', 'month'], axis='columns', inplace=True)

    # Add records to the purchases dataset with the right year, month, and day
    dfs = [df]
    for i in range(1, 26):
        if result[f'date{i}'] not in ['', '00']:
            new_date = result['year-selector'] + "-" + result['month-selector'] + "-" + result[f'date{i}'].zfill(2)
            temp_df = pd.DataFrame({'date': [new_date], 'purchase': [result[f'purchase{i}']], 'cost': [result[f'cost{i}']], 'category': [result[f'category{i}']]})
            dfs.append(temp_df)
    df = pd.concat(dfs, axis='index')

    # Save purchases file
    df.to_csv("purchases.csv", index=False)

    # Work on the wishlist
    result = {k: [v] for (k, v) in result.items() if k.endswith('b')}
    df2 = pd.DataFrame(result)
    df2.to_csv("wishlist.csv")

    # Render the main.html
    return main()

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5001)
