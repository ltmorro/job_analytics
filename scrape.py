#import csv #file i/o for original dataset
import requests #library used for http web requests
from bs4 import BeautifulSoup #used to parse html
import time
import math
import pandas as pd
import nltk.tokenize
import nltk.corpus
import string
jobs_per_page = 50

#downloadJobs pulls all relevant job listings for the job in the location supplied
def download_jobs(job, location, file_path):
    request_data = {"q":job, "l":location, "limit":jobs_per_page, "start":0}
    base_url = "https://www.indeed.com/"
    #get request
    response = requests.get(base_url+"jobs", params=request_data)

    soup = BeautifulSoup(response.content, "html.parser")

    links = []
    #grab the number of pages from search result "Page x of y jobs"
    num_pages = soup.find(id="searchCount").get_text()
    print(num_pages)
    num_pages = math.ceil(int(num_pages.split()[3]) / jobs_per_page) # get the ceiling of the num of jobs / jobs per page

    for i in range(num_pages):
        request_data = {"q":job, "l":location, "limit":jobs_per_page, "start":i*jobs_per_page}
        #get request
        response = requests.get(base_url+"jobs", params=request_data)
        print(response.url)
        soup = BeautifulSoup(response.content, "html.parser")

        titles = soup.find(id='resultsCol') #grab the results column for all the job listings
        for title in titles.find_all('h2', attrs={"class":"jobtitle"}):
            link = title.find('a').get("href") #find the reference link for the job post

            links.append(link)
        time.sleep(1)

    links = list(set(links))

    jobs = []
    i=1 #keep track of loop for printing
    for link in links[:1]:
        print("Getting Job Posting " + str(i))
        i+=1
        response = requests.get(base_url+link)
        url = response.url
        job = BeautifulSoup(response.content, "lxml")

        #stop words to remove
        stop_words = nltk.corpus.stopwords.words('english')
        #Job Title
        #sometimes the http request breaks so we try until we succeed
        while True:
            try:
                title = job.find("h3", attrs={"class":"icl-u-xs-mb--xs icl-u-xs-mt--none jobsearch-JobInfoHeader-title"}).get_text(separator="\n")
                company = job.find("div", attrs={"class":"icl-u-lg-mr--sm icl-u-xs-mr--xs"}).get_text()
                #grab the content and split it in to words
                content = job.find("div", attrs={"class":"jobsearch-JobComponent-description icl-u-xs-mt--md"}).get_text(separator="\n")
                content = nltk.tokenize.word_tokenize(content)
                #remove stop words which dont add any meaning
                content = [word for word in content if word not in stop_words and word.isalpha()]
            except:
                response = requests.get(base_url+link)
                url = response.url
                job = BeautifulSoup(response.content, "lxml")
                continue
            break
        jobs.append({"url":url, "title":title, "company":company, "content":list(set(content))})
        time.sleep(1)

    job_df = pd.DataFrame.from_dict(jobs)
    print(job_df)

    job_df.to_csv(location+".csv")


if __name__ == "__main__":
    top_cities = ["New+York", "Chicago", "Boston", "San+Francisco", "Austin", "Houston", "Seattle"]
    for city in top_cities:
        print("Finding jobs in " + city)
        download_jobs("data+scientist", city, "")
