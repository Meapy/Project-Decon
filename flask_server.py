from flask import Flask, render_template
from imageProcessing import imageProcessing

app = Flask(__name__)



@app.route('/flask', methods=['GET'])
def index():
    img = "data/letter.png"
    imageProc = imageProcessing(img)
    img = imageProc.run(img)
    print(img)
    return render_template('index.html', user_image = img)

if __name__ == "__main__":
    app.run(port=3000, debug=True)