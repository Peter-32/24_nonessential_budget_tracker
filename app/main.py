from flask import Flask, render_template, request
import pandas as pd
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
    print(result)
    result = {k: [v] for (k, v) in result.items()}
    df = pd.DataFrame(result)
    df.to_csv("data.csv")
    return render_template("index.html")

@app.route('/main')
def main():
    return render_template("main.html", setup=setup)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5001)
