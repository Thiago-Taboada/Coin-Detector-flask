from flask import Flask, render_template, request
import cv2
import os
from roboflow import Roboflow

app = Flask(__name__)

rf = Roboflow(api_key="52ZPGjDntv3smMG4Yr7b")
project = rf.workspace().project("moedas-pmfos")
model = project.version(9).model

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

@app.route("/")
def homepage():
    return render_template("index.html")

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route("/detect", methods=["POST"])
def detect_coins():
    target = os.path.join(APP_ROOT, 'static/')
    if not os.path.isdir(target):
        os.mkdir(target)

    image_file = request.files["image"]
    image_filename = image_file.filename
    image_path = os.path.join(target, image_filename)
    image_file.save(image_path)

    response = model.predict(image_path, confidence=70, overlap=30).json()

    sum = 0
    for pred in response['predictions']:
        print(pred['class'])
        if pred['class'] == '1 Real':
            sum += 1
        if pred['class'] == '50 Cent':
            sum += 0.5
        if pred['class'] == '25 Cent':
            sum += 0.25
        if pred['class'] == '10 Cent':
            sum += 0.10
        if pred['class'] == '5 Cent':
            sum += 0.5
    print("Valor total aproximado: R$" + str(sum))

    prediction_path = os.path.join(target, "prediction.jpg")
    model.predict(image_path, confidence=70, overlap=30).save(prediction_path)

    return render_template("index.html", result="static/prediction.jpg", value="Valor total aproximado: R$" + str(sum))

@app.route("/error")
def error():
    return render_template("error.html")

if __name__ == "__main__":
    app.run(debug=True)
