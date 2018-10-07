import pandas as pd
from collections import Counter
import string
import matplotlib.pyplot as plt
import numpy as np

def get_word_counts(top_cites):
    word_counts = Counter()
    num_jobs = 0
    for city in top_cites:
        # create a dataframe from the mined data
        job_df = pd.read_csv(city+".csv", encoding="ISO-8859-1")
        for summary in job_df["content"]:
            # keep track of number of jobs to convert to percentage
            num_jobs += 1
            for word in summary.split():
                # remove punctuation and make all words lower case
                clean_word = word.translate(str.maketrans("","",string.punctuation)).lower()
                word_counts[clean_word] += 1
    return word_counts, num_jobs

def filter_words(word_counts, num_jobs, filter):
    filtered_words = {}
    # select words from the counts that we want
    for word in filter:
        filtered_words[word]= word_counts[word.lower()]
    # create dataframe from dictionary and convert raw counts to percentages
    filtered_df = pd.DataFrame.from_dict(filtered_words, orient="index")
    filtered_df.columns = ["Percent"]
    filtered_df["Percent"] = filtered_df["Percent"]/num_jobs*100

    return filtered_df

def plot_top(df, title):
    plt.style.use("seaborn")
    #name column to Jobs
    df.columns=["Jobs"]
    #sort by count in column Jobs
    df= df.sort_values(by="Jobs", ascending=False)
    top=df.plot(kind='bar')
    #set title and y label
    plt.title(title)
    plt.ylabel("Percentage")
    #label each bar with percentage value
    for idx, label in enumerate(list(df.index)):
        for acc in df.columns:
            value = np.round(df.ix[idx][acc],decimals=2)
            top.annotate(value,
                        (idx, value),
                         xytext=(0, 0),horizontalalignment="center",
                         textcoords='offset points')
    plt.show()

def plot_all(program, analysis, distributed, database, location):
    plt.style.use("seaborn")
    fig, axes = plt.subplots(nrows=2, ncols=2)
    fig.suptitle(location.replace("+", " "), fontsize=16)
    axes[0,0].set_ylabel("Percentage")
    axes[0,0].set_title("Top Programming Languages")
    program.sort_values(by="Percent", ascending=False).plot(kind='bar', ax=axes[0,0])

    axes[0,1].set_ylabel("Percentage")
    axes[0,1].set_title("Top Analysis Tools")
    analysis.sort_values(by="Percent", ascending=False).plot(kind='bar', ax=axes[0,1])

    axes[1,0].set_ylabel("Percentage")
    axes[1,0].set_title("Top Distributed Frameworks")
    distributed.sort_values(by="Percent", ascending=False).plot(kind='bar', ax=axes[1,0])

    axes[1,1].set_ylabel("Percentage")
    axes[1,1].set_title("Top Database Languages")
    database.sort_values(by="Percent", ascending=False).plot(kind='bar', ax=axes[1,1])

    plt.tight_layout(rect=[0, 0.03, 1, 0.95], pad=0.4, w_pad=1.5, h_pad=1.0)

if __name__ == "__main__":
    top_cities = ["New+York", "Chicago", "Boston", "San+Francisco", "Austin", "Houston", "Seattle", "Denver"]
    # filters for different plots
    program_lang_filter = ['Python', 'R', 'Java', 'C', 'Ruby', 'Perl', 'Matlab', 'JavaScript', 'Scala']
    analysis_filter = ['Excel', 'Tableau','SAS', 'SPSS','D3']
    distributed_filter = ['Hadoop', 'MapReduce', 'Spark', 'Pig', 'Hive', 'Shark', 'Oozie', 'ZooKeeper', 'Flume', 'Mahout']
    database_filter = ['SQL', 'NoSQL', 'HBase', 'Cassandra', 'MongoDB']
    lib_filter = ['Tensorflow', 'Matplotlib', 'Scikit', 'Numpy', 'Pandas', 'Keras', 'NLTK', 'Pyspark']

    for city in top_cities:
        word_counts, num_jobs = get_word_counts([city])
        program_lang = filter_words(word_counts, num_jobs, program_lang_filter)
        analysis = filter_words(word_counts, num_jobs, analysis_filter)
        distributed = filter_words(word_counts, num_jobs, distributed_filter)
        database = filter_words(word_counts, num_jobs, database_filter)
        plot_all(program_lang, analysis, distributed, database, city)

    word_counts, num_jobs = get_word_counts(["nation"])
    program_lang = filter_words(word_counts, num_jobs, program_lang_filter)
    analysis = filter_words(word_counts, num_jobs, analysis_filter)
    distributed = filter_words(word_counts, num_jobs, distributed_filter)
    database = filter_words(word_counts, num_jobs, database_filter)
    # plot the nationwide plots
    plot_top(program_lang, "Top Programming Languages")
    plot_top(analysis, "Top Analysis Tools")
    plot_top(distributed, "Top Distributed Frameworks")
    plot_top(database, "Top Database Languages")
    plot_top(libs, "Top Python Libraries")

    nationwide(["nation"])
