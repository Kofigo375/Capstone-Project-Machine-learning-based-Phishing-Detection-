from flask import  Flask, request, jsonify
import feature_extraction
from model import predict_rf, predict_xgb
import os
import psycopg2
from dotenv import load_dotenv
import numpy as np


# creating flask application
app = Flask(__name__)
database_url = os.getenv('DATABASE_URL')
connection = psycopg2.connect(database_url)

# making environment variables available
load_dotenv()


# make predictions using model
def make_predictions(url):
    x_pred = feature_extraction.generate_dataset(url)
    x_pred_array = np.array(x_pred)
    x_pred_array = x_pred_array.reshape(1,-1)
    print(f"This is extracted features {x_pred_array} with the shape {x_pred_array.shape}")  # noqa: E501
    prediction = predict_rf(x_pred_array)
    print(f" predicted value : {prediction[0]}")
    return prediction[0]

# defining queries
CREATE_URL_TABLE = (
    "CREATE TABLE IF NOT EXISTS url_predictions (id SERIAL PRIMARY KEY, url TEXT, prediction INTEGER);"  # noqa: E501
)
INSERT_URL_TABLE = (
    "INSERT INTO url_predictions (url, prediction) VALUES (%s, %s) RETURNING id;"
)

def create_prediction(predicted):
    data = request.get_json()
    url = data["url"]
    prediction = predicted
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(CREATE_URL_TABLE)
            cursor.execute(INSERT_URL_TABLE, (url, prediction))
            url_id = cursor.fetchone()[0]
    return {"url": url, "message": f"Prediction for {url} created successfully", "id": url_id}  # noqa: E501



@app.route("/", methods=["POST", "GET"])
def home():
    if request.method == "POST":
        data = request.get_json()
        url = data["url"]
        prediction = make_predictions(url)
        prediction = int(prediction)

        # store prediction in database
        create_prediction(prediction)
    return jsonify({"url": url,"prediction": prediction})

if __name__ == "__main__":
    app.run()

# new requirements:
# this api shouldn't render an html page 
# it should just return the prediction as a response back to the client(chrome extension)
























































'''from flask import Flask, render_template, request
import model
import numpy as np


app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def display_risk():
    if request.method == 'POST':
        entry_content = request.form.get("url")
        #app.db.insert_one({"content": entry_content, "phishing_status": "this is a phishing web page"})

    test_data = [-1,1,-1,1,1,-1,1,1,-1,1,1,-1,1,1,-1,1,1,-1,1,1,-1,1,1,-1,1]
    check_dimension = np.array(test_data).reshape(1,-1)

    #print(len(test_data))
    predicted = model.prediction(check_dimension)
    print(predicted)
    print(type(predicted))
    if predicted == 1:            
        print("this is a phishing website")
    else:
        pass
    return render_template('home.html', predicted = predicted)

"""
@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        result = request.form.get("url")

    return render_template('/submit.html', result = result)

"""
# mongodb url
# 
'''