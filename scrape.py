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
base_url = "https://www.indeed.com/"

#this method gets all the job links for a given location
def get_links(job, location):
    request_data = {"q":job, "l":location, "limit":jobs_per_page, "start":0}
    #get request
    response = requests.get(base_url+"jobs", params=request_data)
    #create soup so we can parse the html
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
    return links

#downloadJobs pulls all relevant job listings for the set of links and saves them at file_path
def download_jobs(links, file_path):
    jobs = []
    i=1 #keep track of loop for printing
    for link in links:
        print("Getting Job Posting " + str(i))
        i+=1
        #send get request to the specfic job link
        response = requests.get(base_url+link)
        url = response.url
        job = BeautifulSoup(response.content, "html.parser")

        #stop words to remove
        stop_words = nltk.corpus.stopwords.words('english')
        #sometimes the http request breaks so we try until we succeed
        giveup=0
        while True:
            #use a try because some responses get corrupted during transmission
            try:
                #job title
                title = job.find("h3", attrs={"class":"icl-u-xs-mb--xs icl-u-xs-mt--none jobsearch-JobInfoHeader-title"}).get_text(separator="\n")
                #company info
                company = job.find("div", attrs={"class":"icl-u-lg-mr--sm icl-u-xs-mr--xs"}).get_text()
                #grab the content and split it in to words
                content = job.find("div", attrs={"class":"jobsearch-JobComponent-description icl-u-xs-mt--md"}).get_text(separator="\n")
                #split in to words from the text using nltk tokenize
                content = nltk.tokenize.word_tokenize(content)
                #remove stop words which dont add any meaning
                content = [word for word in content if word not in stop_words]
            except:
                print("Trying again")
                response = requests.get(base_url+link)
                url = response.url
                job = BeautifulSoup(response.content, "html.parser")
                time.sleep(1)
                #we don't want to get stuck in a loop forever
                if giveup == 5:
                    break
                giveup +=1
                continue
            break
        #add job to list, we set the content because I only care about existence not frequency
        jobs.append({"url":url, "title":title, "company":company, "content":list(set(content))})
        time.sleep(1)

    #convert the dictionary to a pandas dataframe and save as a csv
    job_df = pd.DataFrame.from_dict(jobs)
    job_df.to_csv(location+".csv")

if __name__ == "__main__":
    top_cities = ["New+York", "Chicago", "Boston","San+Francisco","Houston","Seattle", "Denver"]
    for city in top_cities:
        print("Finding jobs in " + city)
        links=get_links("data+scientist", city)
        download_jobs(links, "")
