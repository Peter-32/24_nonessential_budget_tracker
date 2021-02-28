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
def index():
    return render_template("setup.html")    





if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5001)
