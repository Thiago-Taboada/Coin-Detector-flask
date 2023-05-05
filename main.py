from flask import Flask, render_template, request
import cv2
import os

app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

@app.route("/")
def homepage():
    return render_template("index.html")

@app.route("/detect", methods=["POST"])
def detect_coins():
    target = os.path.join(APP_ROOT, 'static/')
    if not os.path.isdir(target):
        os.mkdir(target)

    image_file = request.files["image"]
    image_filename = image_file.filename
    image_path = os.path.join(target, image_filename)
    image_file.save(image_path)

    img = cv2.imread(image_path)

    # Aplicar algoritmo de detecção de moedas
    # ...

    # Guardar imagen com detecção de moedas
    result_path = os.path.join(target, "result.jpg")
    cv2.imwrite(result_path, img)

    return render_template("index.html", result="static/result.jpg")

@app.route("/error")
def error():
    return render_template("error.html")

if __name__ == "__main__":
    app.run(debug=True)