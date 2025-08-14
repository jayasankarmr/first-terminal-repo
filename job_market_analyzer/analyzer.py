import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
import os

def analyze_job_data(csv_filepath, static_dir='job_market_analyzer/static'):
    """
    Performs data cleaning, analysis, and visualization on the job postings data.

    Args:
        csv_filepath (str): The path to the job postings CSV file.
        static_dir (str): The directory to save the generated images.
    """
    try:
        df = pd.read_csv(csv_filepath)
    except FileNotFoundError:
        print(f"Error: The file at {csv_filepath} was not found.")
        return

    # Data Cleaning
    df.drop_duplicates(inplace=True)
    df['Location'].fillna('Not Specified', inplace=True)
    df['Company Name'].fillna('Not Specified', inplace=True)

    # Data Analysis
    location_counts = df['Location'].value_counts().head(10)
    print("Top 10 Job Locations:")
    print(location_counts)

    # Ensure the static directory exists
    if not os.path.exists(static_dir):
        os.makedirs(static_dir)

    # Create and save the bar chart
    plt.figure(figsize=(10, 8))
    sns.barplot(x=location_counts.values, y=location_counts.index, palette='viridis')
    plt.title('Top 10 Job Locations', fontsize=16)
    plt.xlabel('Number of Job Postings', fontsize=12)
    plt.ylabel('Location', fontsize=12)
    plt.tight_layout()
    bar_chart_path = os.path.join(static_dir, 'jobs_by_location.png')
    plt.savefig(bar_chart_path)
    print(f"Bar chart saved to {bar_chart_path}")

    # Create and save the word cloud
    # Concatenate all job summaries into a single string
    text = ' '.join(df['Job Summary'].dropna())

    if text:
        wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
        plt.figure(figsize=(10, 5))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        wordcloud_path = os.path.join(static_dir, 'skills_wordcloud.png')
        wordcloud.to_file(wordcloud_path)
        print(f"Word cloud saved to {wordcloud_path}")
    else:
        print("Not enough data to generate a word cloud.")


if __name__ == '__main__':
    csv_file = 'job_market_analyzer/job_postings.csv'
    analyze_job_data(csv_file)
