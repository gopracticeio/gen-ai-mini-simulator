import pandas as pd
from datetime import datetime
from collections import defaultdict
import random
from random import shuffle

TOO_OLD_DATE = datetime(2022, 1, 1)
MAJOR_EVENT_DATE = datetime(2022, 10, 1)

def load_reviews(path):
    all_reviews_df = pd.read_csv(path)
    all_reviews_df["date"] = all_reviews_df["date"].apply(lambda x: datetime.strptime(x, "%Y-%m-%d %H:%M:%S"))
    return all_reviews_df

def split_reviews_by_event_date(all_reviews_df):
    samples = defaultdict(list)
    for r in all_reviews_df.to_dict("records"):
        if r["date"] < TOO_OLD_DATE:
            continue
        interval = "after"
        if r["date"] < MAJOR_EVENT_DATE:
            interval = "before"
        samples[interval].append(r)
    return samples

def prepare_train_validate(split, size=25):
    sample_size = size*2
    random.seed(100)
    sample_before = list(split["before"])
    shuffle(sample_before)
    sample_before = sample_before[0:sample_size]

    sample_after = list(split["after"])
    shuffle(sample_after)
    sample_after = sample_after[0:sample_size]

    mini_sample_size = int(size/2)
    dataset_v1 = (sample_before[0:mini_sample_size] + sample_after[0:(mini_sample_size+1)])
    dataset_v2 = (sample_before[mini_sample_size:] + sample_after[(mini_sample_size+1):])

    return dataset_v1, dataset_v2

def prepare_stratified_dataset(samples):
    import random
    random.seed(42)

    size_before_part = len(samples["before"])
    size_after_part = len(samples["after"])

    min_size = min(size_before_part, size_after_part)

    all_reviews = []
    for r in samples["before"]:
        if random.random() < min_size/float(size_before_part):
            all_reviews.append(r)
    for r in samples["after"]:
        if random.random() < min_size/float(size_after_part):
            all_reviews.append(r)
    return all_reviews

def prepare_topic_sample(extraction_results, size=200):
    topics_all = []
    for topics in extraction_results:
        for t in topics:
            if "topic" in t:
                topics_all.append(t)

    all_topic_names = (pd.DataFrame.from_records(topics_all)["topic"]
                       .apply(lambda x: x.lower().strip())
                       .unique()
                       .tolist())

    topics_sample = []
    topics_sample.extend(all_topic_names)

    random.seed(100)
    random.shuffle(topics_sample)
    topics_sample = topics_sample[0:min(size, len(topics_sample))]

    return all_topic_names, topics_sample

def build_topic_sentiments_df(
        reviews_df,
        topic_extraction_results,
        topic_category_mapping
):
    """
    This function build a table with columns: topic, sentiment, date, month
    :param reviews_df: reviews to process
    :param topic_extraction_results: results of 1st pipeline
    :param topic_category_mapping: results of mapping pipeline
    :return: pandas.DataFrame
    """
    review_dates = {}
    for r in reviews_df.to_dict("records"):
        review_dates[r["review"]] = r["date"]

    final_topic_mapping = {}
    for r in topic_category_mapping:
        if not len(r):
            continue
        k, v = list(r.items())[0]
        final_topic_mapping[k] = v

    topic_sentiments = []
    for topics in topic_extraction_results:
        for t in topics:
            topic_key = t["topic"].strip().lower()
            if not len(topic_key):
                continue
            if topic_key in final_topic_mapping:
                topic_sentiments.append({
                    "topic": final_topic_mapping[topic_key],
                    "sentiment": t["sentiment"],
                    "date": review_dates[t["review_text"]],
                    "month": datetime.strftime(review_dates[t["review_text"]].replace(day=1), "%Y-%m-%d")
                })
            else:
                print("No mapping for %s" % topic_key)
    return pd.DataFrame.from_records(topic_sentiments)
