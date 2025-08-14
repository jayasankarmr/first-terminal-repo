from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)

@app.route('/')
def index():
    """
    Renders the main dashboard page.
    """
    try:
        df = pd.read_csv('job_market_analyzer/job_postings.csv')
        # Get the top 10 job postings
        top_10_jobs = df.head(10).to_dict(orient='records')
    except FileNotFoundError:
        top_10_jobs = []

    return render_template('index.html', jobs=top_10_jobs)

if __name__ == '__main__':
    app.run(debug=True)
