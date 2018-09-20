import csv #file i/o for original dataset
import requests #library used for http web requests
from bs4 import BeautifulSoup #used to parse html
import time
import re

#downloadJobs pulls all relevant job listings for the job in the location supplied
def downloadJobs(job, location, file_path):
    request_data = {"q":job.replace(" ", "+"), "l":location, "limit":50}
    base_url = "https://www.indeed.com/"
    #get request
    response = requests.get(base_url+"jobs", params=request_data)

    soup = BeautifulSoup(response.content, "lxml")

    links = []
    titles = soup.find(id='resultsCol') #grab the results column for all the job listings
    for title in titles.find_all('h2', attrs={"class":"jobtitle"}):
        link = title.find('a').get("href") #find the reference link for the job post

        links.append(link)

    for link in links[:5]:
        print("Getting Job Posting")
        response = requests.get(base_url+link)
        print(response.url)
        job = BeautifulSoup(response.content, "lxml")

        # for script in job(["script", "style"]):
        #     script.extract() # Remove these two elements from the BS4 object
        # print(job.get_text())
        print("~~~Job Title~~~")
        print(job.find("div", attrs={"class":"jobsearch-JobComponent icl-u-xs-mt--sm"}).get_text(separator="\n"))
        # print(job.find("div", attrs={"class":"icl-u-lg-mr--sm icl-u-xs-mr--xs"}))
        print("~~~Job content~~~")
        # print(job.find("div", attrs={"class":"jobsearch-JobComponent-description icl-u-xs-mt--md"}))
        # print(job.find(id="job_summary"))
        #print(job.get_text())
        time.sleep(1)



if __name__ == "__main__":
    downloadJobs("data scientist", "Houston", "")
