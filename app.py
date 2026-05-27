################################################################
# Hwang and Blitzstein. 2022. Introduction to Probability (25) #
# Example 1.6.4 de Montmort's Matching Problem                 #
# Flask App: Visualising the Simulation Results                #
################################################################

import json
import plotly
from flask import Flask, render_template
from functions import simulate_outcomes, build_figure

app = Flask(__name__)

DECK_SIZE = 50
SAMPLE_SIZE = 20_000

outcomes = simulate_outcomes(DECK_SIZE, SAMPLE_SIZE)

@app.route('/')
def index():
    fig = build_figure(outcomes, DECK_SIZE)
    plot_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template('index.html', plot_json=plot_json)

if __name__ == '__main__':
    app.run(debug=False)
