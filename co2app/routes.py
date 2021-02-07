from co2app import app
import json, plotly
from flask import render_template
from data_scripts.worldbank_data import create_figures

@app.route('/')
@app.route('/index')
def index():

    figures = create_figures()

    # plot ids for the html id tag
    ids = ['figure-{}'.format(i) for i, _ in enumerate(figures)]

    # Convert the plotly figures to JSON for javascript in html template
    figuresJSON = json.dumps(figures, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('index.html',
                           ids=ids,
                           figuresJSON=figuresJSON)