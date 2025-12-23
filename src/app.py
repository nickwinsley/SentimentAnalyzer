from flask import Flask, render_template, request, redirect, url_for
import joblib

app = Flask(__name__)

def PredictSentiment(input):
    model = joblib.load('sentiment.joblib')
    
    response = model.predict([input])
    
    res = "Negative" if response == 0 else "Positive"

    return (res)

results = {}

@app.route('/')
def setUp():
    return render_template('form.html', results = results)

@app.route('/process', methods = ['POST'])
def process():

    if request.method == 'POST':

        input = request.form.get('user_string', '')

        response = PredictSentiment(input)

        results[input] = response

        return render_template('results.html', original = input, result = response)

    return redirect(url_for(setUp))

if (__name__ == '__main__'):
    app.run(host = "0.0.0.0", port = 8080)
