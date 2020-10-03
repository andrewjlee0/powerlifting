import flask
import pickle
import pandas as pd

# Use pickle to load in the pre-trained model.
with open(f'model/model_file_deadlift.pkl', 'rb') as f:
    model = pickle.load(f)['model']

app = flask.Flask(__name__, template_folder='templates')
@app.route('/', methods=['GET', 'POST'])

def main():
    if flask.request.method == 'GET':
        return(flask.render_template('main.html'))

    if flask.request.method == 'POST':
        vars = dict(flask.request.form)
        input_variables = pd.DataFrame([vars], columns=vars.keys(), dtype=float)
        prediction = model.predict(input_variables)[0]
        return flask.render_template('main.html', original_input=vars, result=prediction)

if __name__ == '__main__':
    app.run()
