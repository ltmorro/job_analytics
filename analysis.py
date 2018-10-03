import pandas as pd
from collections import Counter
import string
import matplotlib.pyplot as plt

def plot_top(df, title, x, y):
    plt.style.use("seaborn-dark")

    df.columns=["Jobs"]
    df.sort_values(by="Jobs", ascending=False).plot(kind='bar')
    plt.title(title)
    plt.xlabel(x)
    plt.ylabel(y)

def plot_all(program, analysis, distributed, database, location):
    plt.style.use("seaborn")
    fig, axes = plt.subplots(nrows=2, ncols=2)
    fig.suptitle(location.replace("+", " "), fontsize=16)
    axes[0,0].set_ylabel("Percentage")
    axes[0,0].set_title("Top Programming Languages")
    #axes[0,0].ylim(0, 100)
    program.plot(kind='bar', ax=axes[0,0])

    axes[0,1].set_ylabel("Percentage")
    axes[0,1].set_title("Top Analysis Tools")
    analysis.plot(kind='bar', ax=axes[0,1])

    axes[1,0].set_ylabel("Percentage")
    axes[1,0].set_title("Top Distributed Frameworks")
    distributed.plot(kind='bar', ax=axes[1,0])

    axes[1,1].set_ylabel("Percentage")
    axes[1,1].set_title("Top Database Languages")
    database.plot(kind='bar', ax=axes[1,1])

    plt.tight_layout(rect=[0, 0.03, 1, 0.95], pad=0.4, w_pad=1.5, h_pad=1.0)

def get_top_words(location):
    job_df = pd.read_csv(location+".csv", encoding="ISO-8859-1")

    top_words = Counter()
    num_jobs = 0
    for summary in job_df["content"]:
        num_jobs += 1
        for word in summary.split():
            clean_word = word.translate(str.maketrans("","",string.punctuation)).lower()

            top_words[clean_word] += 1

    program_lang = {'Python':top_words['python'], 'R':top_words['r'],
                    'Java':top_words['java'], 'C':top_words['c'],
                    'Ruby':top_words['ruby'], 'Perl':top_words['perl'],
                    'Matlab':top_words['matlab'], 'JavaScript':top_words['javascript'],
                    'Scala': top_words['scala']}

    analysis_tools = {'Excel':top_words['excel'],  'Tableau':top_words['tableau'],
                        'D3.js':top_words['d3.js'], 'SAS':top_words['sas'],
                        'SPSS':top_words['spss'], 'D3':top_words['d3']}

    distributed_tools = {'Hadoop':top_words['hadoop'], 'MapReduce':top_words['mapreduce'],
                'Spark':top_words['spark'], 'Pig':top_words['pig'],
                'Hive':top_words['hive'], 'Shark':top_words['shark'],
                'Oozie':top_words['oozie'], 'ZooKeeper':top_words['zookeeper'],
                'Flume':top_words['flume'], 'Mahout':top_words['mahout']}

    database_lang = {'SQL':top_words['sql'], 'NoSQL':top_words['nosql'],
                    'HBase':top_words['hbase'], 'Cassandra':top_words['cassandra'],
                    'MongoDB':top_words['mongodb']}

    python_libs = {'Tensorflow':top_words['tensorflow'], 'Matplotlib':top_words['matplotlib'], 'Scikit':top_words['scikit'],
                   'Numpy':top_words['numpy'], 'Pandas':top_words['pandas'], 'Keras':top_words['keras'], 'NLTK':top_words['nltk']}

    language = pd.DataFrame.from_dict(program_lang, orient="index")
    language.columns = ["Percent"]
    language["Percent"] = language["Percent"]/num_jobs*100
    analysis = pd.DataFrame.from_dict(analysis_tools, orient="index")
    analysis.columns = ["Percent"]
    analysis["Percent"] = analysis["Percent"]/num_jobs*100
    distributed = pd.DataFrame.from_dict(distributed_tools, orient="index")
    distributed.columns = ["Percent"]
    distributed["Percent"] = distributed["Percent"]/num_jobs*100
    database = pd.DataFrame.from_dict(database_lang, orient="index")
    database.columns = ["Percent"]
    database["Percent"] = database["Percent"]/num_jobs*100


    # plot_top(language, "Top Programming Languages", "Language", "Percentage")
    # plot_top(analysis, "Top Analysis Tools", "Tool", "Percentage")
    # plot_top(distributed, "Top Distributed Tools", "Tool", "Percentage")
    # plot_top(database, "Top Database Languages", "Language", "Percentage")

    plot_all(language, analysis, distributed, database, location)
    plt.show()

    libs = pd.DataFrame.from_dict(python_libs, orient="index")
    libs.columns = ["Percent"]
    libs["Percent"] = libs["Percent"]/num_jobs*100
    plot_top(libs, "Top Python Libraries", "Library", "Percentage")

if __name__ == "__main__":
    top_cities = ["New+York", "Chicago", "Boston", "San+Francisco", "Austin", "Houston", "Seattle"]
    for city in top_cities:
        print("Finding jobs in " + city)
        get_top_words(city)
