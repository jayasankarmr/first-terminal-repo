import pandas as pd
import requests
from bs4 import BeautifulSoup

def scrape_job_postings(url):
    """
    Scrapes job posting data from a URL.

    Args:
        url (str): The URL of the job search results page.

    Returns:
        list: A list of dictionaries, where each dictionary represents a job posting.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes
    except requests.exceptions.RequestException as e:
        print(f"Error: Failed to retrieve the webpage. {e}")
        return []

    soup = BeautifulSoup(response.content, 'html.parser')
    job_postings = []

    for job_div in soup.find_all('div', class_='job-posting'):
        title = job_div.find('h2', class_='job-title').text.strip()
        company = job_div.find('span', class_='company-name').text.strip()
        location = job_div.find('div', class_='job-location').text.strip()
        summary = job_div.find('p', class_='job-summary').text.strip()

        job_postings.append({
            'Job Title': title,
            'Company Name': company,
            'Location': location,
            'Job Summary': summary
        })

    return job_postings

if __name__ == '__main__':
    url_to_scrape = 'http://127.0.0.1:8000/job_market_analyzer/job_postings.html'
    output_csv_path = 'job_market_analyzer/job_postings.csv'

    scraped_data = scrape_job_postings(url_to_scrape)

    if scraped_data:
        print(f"Successfully scraped {len(scraped_data)} job postings.")

        # Convert to DataFrame and save as CSV
        df = pd.DataFrame(scraped_data)
        df.to_csv(output_csv_path, index=False)

        print(f"Data saved to {output_csv_path}")
    else:
        print("No job postings were scraped.")
