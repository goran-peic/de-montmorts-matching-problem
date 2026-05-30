################################################################
# Hwang and Blitzstein. 2022. Introduction to Probability (25) #
# Example 1.6.4 de Montmort's Matching Problem                 #
# Flask App: Visualising the Simulation Results                #
################################################################

import json
import plotly
from flask import Flask, render_template, request, Response
from functions import simulate_outcomes_stream, build_figure

app = Flask(__name__)

@app.route('/')
def index():
    """Render the page with no plot pre-loaded; the user triggers simulation via the form."""
    return render_template('index.html', plot_json=None)

@app.route('/simulate')
def simulate():
    """
    Server-Sent Events endpoint.
    Query params: deck_size (int), sample_size (int)

    Streams SSE events:
      - progress: {"n": int, "pct": float}   — one per deck size computed
      - done:     Plotly figure JSON           — when all deck sizes are done
    """
    deck_size   = int(request.args.get('deck_size',   52))
    sample_size = int(request.args.get('sample_size', 10_000))

    # Clamp to safe ranges
    deck_size   = max(2,   min(deck_size,   500))
    sample_size = max(100, min(sample_size, 200_000))

    def event_stream():
        outcomes = []
        for n, prob in simulate_outcomes_stream(deck_size, sample_size):
            outcomes.append(prob)
            pct = round(n / deck_size * 100, 1)
            payload = json.dumps({'n': n, 'pct': pct})
            yield f'event: progress\ndata: {payload}\n\n'

        # All deck sizes done — send the finished figure
        fig      = build_figure(outcomes, deck_size)
        fig_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        yield f'event: done\ndata: {fig_json}\n\n'

    return Response(
        event_stream(),
        mimetype='text/event-stream',
        headers={
            'Cache-Control': 'no-cache',
            'X-Accel-Buffering': 'no',   # disable Nginx buffering if proxied
        }
    )

if __name__ == '__main__':
    app.run(debug=False)
