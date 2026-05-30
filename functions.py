################################################################
# Hwang and Blitzstein. 2022. Introduction to Probability (25) #
# Example 1.6.4 de Montmort's Matching Problem                 #
# Approximating the Solution via Simulation in Python          #
################################################################

import random
import plotly.graph_objs as go

def simulate_outcomes(deck_size: int, sample_size: int) -> list[float]:
    """
    Simulate the probability of at least one match (a 'win') in
    de Montmort's Matching Problem for each deck size from 1 to deck_size.

    Args:
        deck_size:   Maximum deck size to simulate up to.
        sample_size: Number of games simulated per deck size.

    Returns:
        A list of win probabilities, one per deck size (index 0 = deck size 1).
    """
    return list(p for _, p in simulate_outcomes_stream(deck_size, sample_size))

def simulate_outcomes_stream(deck_size: int, sample_size: int):
    """
    Generator version of simulate_outcomes.
    Yields (n, probability) tuples one at a time as each deck size is computed,
    allowing callers to stream progress to the client.

    Args:
        deck_size:   Maximum deck size to simulate up to.
        sample_size: Number of games simulated per deck size.

    Yields:
        Tuples of (n: int, probability: float) for n in 1..deck_size.
    """
    for n in range(1, deck_size + 1):
        wins = sum(
            any(a == b for a, b in zip(
                random.sample(range(1, n + 1), n),
                random.sample(range(1, n + 1), n)
            ))
            for _ in range(sample_size)
        )
        yield n, wins / sample_size

def build_figure(outcomes: list[float], deck_size: int) -> go.Figure:
    """Build and return the Plotly figure for the simulation results."""
    avg_probability = sum(outcomes[3:]) / len(outcomes[3:])

    fig = go.Figure()

    # Probability curve
    fig.add_trace(go.Scatter(
        x=list(range(1, deck_size + 1)),
        y=outcomes,
        mode='lines',
        name='Probability',
        line=dict(color='#00d2ff', width=3),
        fill='tozeroy',
        fillcolor='rgba(0, 210, 255, 0.1)'
    ))

    # Average probability line (deck size > 3)
    fig.add_hline(
        y=avg_probability,
        line=dict(color='red', width=2, dash='dash')
    )

    # Average probability annotation
    fig.add_annotation(
        xref='paper', yref='y',
        x=0.5, y=avg_probability,
        text=f'Average Probability: {avg_probability:.4f}',
        yshift=50,
        showarrow=False,
        xanchor='center',
        font=dict(color='red', size=20)
    )

    fig.update_layout(
        title="Solving De Montmort's Matching Problem via Simulation",
        title_x=0.5,
        xaxis_title='Deck Size',
        yaxis_title='Probability',
        template='plotly_dark',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        hovermode='x unified',
        xaxis=dict(range=[1, deck_size]),
        yaxis=dict(range=[0, 1]),
        margin=dict(l=40, r=40, t=60, b=40)
    )

    return fig
