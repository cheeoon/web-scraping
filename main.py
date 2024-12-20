import requests
from bs4 import BeautifulSoup
import pandas as pd

# Define the URL of the JobStreet search page
BASE_URL = "https://sg.jobstreet.com/software-jobs"

# Send a GET request
response = requests.get(BASE_URL, headers={"User-Agent": "Mozilla/5.0"})
soup = BeautifulSoup(response.text, 'html.parser')

# Initialize a list to store job data
jobs = []

# Locate job cards on the page
job_cards = soup.find_all('article', {"data-automation": "normalJob"})

for job_card in job_cards:

    title = None
    company = None
    salary = None
    location = None
    link = None

    try:
        title = job_card.get("aria-label")
    except AttributeError:
        title = "Not Available"

    try:
        company = job_card.find("a",{"data-automation":"jobCompany"}).text.strip()
    except AttributeError:
        company = "Not Available"

    try: 
        salary = job_card.find("span",{"data-automation":"jobSalary"}).text.strip()
    except AttributeError:
        salary = "Not Available"

    try: 
        getlink = job_card.find("a",{"data-automation":"job-list-view-job-link"}, href=True).get('href')
        link = 'https://sg.jobstreet.com' + getlink
    except AttributeError:
        link = "Not Available"

    try: 
        locations= job_card.find_all('a', {'data-automation': 'jobLocation'})
        location = [link.get_text() for link in locations]
    except AttributeError:
         location = "Not Available"

    jobs.append({
            "Job Title": title,
            "Company": company,
            "Salary" : salary,
            "Location" : location,
            "Link":  link
        })
print(location)  # Check the result
# Convert the list to a DataFrame
df = pd.DataFrame(jobs)

# Save to CSV
df.to_csv("jobstreet_jobs.csv", index=False)
print("Data saved to jobstreet_jobs.csv")
