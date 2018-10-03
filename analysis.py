import pandas as pd
from collections import Counter
import string

def get_top_words(location):
    job_df = pd.read_csv(location+".csv")

    top_words = Counter()
    for summary in job_df["content"]:
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

    distributed = {'Hadoop':top_words['hadoop'], 'MapReduce':top_words['mapreduce'],
                'Spark':top_words['spark'], 'Pig':top_words['pig'],
                'Hive':top_words['hive'], 'Shark':top_words['shark'],
                'Oozie':top_words['oozie'], 'ZooKeeper':top_words['zookeeper'],
                'Flume':top_words['flume'], 'Mahout':top_words['mahout']}

    database = {'SQL':top_words['sql'], 'NoSQL':top_words['nosql'],
                    'HBase':top_words['hbase'], 'Cassandra':top_words['cassandra'],
                    'MongoDB':top_words['mongodb']}

    print("Top Programming Languages")
    print(program_lang)
    print("Top Analysis Tools")
    print(analysis_tools)
    print("Top Distributed Data Tools")
    print(distributed)
    print("Top Database Languages")
    print(database)

if __name__ == "__main__":
    get_top_words("Houston")
