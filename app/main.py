from flask import Flask, render_template
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
             'purchase1': "1", 'cost1': "1", 'category1': "want",
             'purchase2': "", 'cost2': "", 'category2': "need",
             'purchase3': "", 'cost3': "", 'category3': "need",
             'purchase4': "", 'cost4': "", 'category4': "need",
             'purchase5': "", 'cost5': "", 'category5': "need",
             'purchase6': "", 'cost6': "", 'category6': "need",
             'purchase7': "", 'cost7': "", 'category7': "need",
             'purchase8': "", 'cost8': "", 'category8': "need",
             'purchase9': "", 'cost9': "", 'category9': "need",
             'purchase10': "", 'cost10': "", 'category10': "need",
             'purchase11': "", 'cost11': "", 'category11': "need",
             'purchase12': "", 'cost12': "", 'category12': "need",
             'saving': ""
             }
    return render_template("setup.html", setup=setup)





if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5001)
