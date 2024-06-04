import matplotlib.pyplot as plt
from datetime import datetime
import pandas as pd

MAJOR_EVENT_DATE = datetime(2022, 11, 1)
DEFAULT_FIGSIZE = (22, 10)

class ReviewAnalysisPlots(object):
    def __init__(self, topic_sentiments_df):
        topic_sentiments_df['month'] = topic_sentiments_df['month'].apply(lambda x: datetime.strptime(x, "%Y-%m-%d"))
        topic_sentiments_df['sentiment'] = topic_sentiments_df['sentiment'].apply(lambda x: x.lower() if type(x) is str else x)
        topic_sentiments_df["count"] = 1

        clean = topic_sentiments_df[(topic_sentiments_df.topic != "Not applicable") & (topic_sentiments_df.topic != "Not enough context to categorize")]

        m = pd.DataFrame({"month": clean["month"].unique()})
        s = pd.DataFrame({"sentiment": ["positive", "negative", "neutral"]})
        t = pd.DataFrame({"topic": clean["topic"].unique()})

        self.topic_sentiments_df = (m
            .merge(s, how='cross')
            .merge(t, how="cross")
            .set_index(["month", "topic", "sentiment"])
            .join(clean.set_index(["month", "topic", "sentiment"]), on=["month", "topic", "sentiment"], how="left")
            .fillna(0)
            .reset_index()
            .sort_values(by=['month', 'topic', 'sentiment'], ascending=True)
        )

        self.topic_sentiment_counts = self.topic_sentiments_df.groupby(["month", "topic", "sentiment"], as_index=False)["count"].sum()

        self.monthly_counts = self.topic_sentiments_df.groupby(["month"], as_index=False)["count"].sum()
        self.monthly_counts["monthly_count"] = self.monthly_counts["count"]

        self.topic_counts = self.topic_sentiments_df.groupby(["month", "topic"], as_index=False)["count"].sum()
        self.topic_counts["topic_count"] = self.topic_counts["count"]

        self.sentiment_counts = self.topic_sentiments_df.groupby(["month", "sentiment"], as_index=False)["count"].sum()
        self.sentiment_counts["sentiment_count"] = self.sentiment_counts["count"]

    def plot_sentiment_rate_by_topic(self, topic):
        d1 = self.topic_counts[self.topic_counts.topic == topic][["month", "topic", "topic_count"]]
        d2 = self.topic_sentiment_counts[self.topic_sentiment_counts.topic == topic]

        result = d2.set_index(["month", "topic"]).join(d1.set_index(["month", "topic"]), on=["month", "topic"])
        result["rate"] = result["count"]/result["topic_count"]

        p = result.reset_index()
        neg = p[p.sentiment=="negative"]
        neg.plot(x="month", y="rate", title=topic + " (negative rate)")


    def plot_topic_rate(self, topic, add_vline=True, save_to=None):
        d1 = self.monthly_counts[["month", "monthly_count"]]
        d2 = self.topic_sentiment_counts[self.topic_sentiment_counts.topic == topic][["month", "count"]].groupby(["month"]).sum().reset_index()

        result = d2.set_index(["month"]).join(d1.set_index(["month"]), on=["month"])
        result["rate"] = result["count"]/result["monthly_count"]

        p = result.reset_index()
        if save_to is not None:
            p.to_csv(save_to + ".csv", index=False)
        p.plot(x="month", y="rate", title=topic + " (rate)")
        if add_vline:
            plt.axvline(x=MAJOR_EVENT_DATE, color="red")
        if save_to is not None:
            plt.savefig(save_to + ".png", bbox_inches='tight')

    def plot_topic_rate_all(self, topic, add_vline=True, save_to=None):
        d1 = self.monthly_counts[["month", "monthly_count"]]
        d2 = (self.topic_sentiment_counts[self.topic_sentiment_counts.topic == topic][["sentiment", "month", "count"]]
              .groupby(["sentiment", "month"])
              .sum()
              .reset_index())

        result = d2.set_index(["month"]).join(d1.set_index(["month"]), on=["month"])
        result["rate"] = result["count"]/result["monthly_count"]

        p = result.reset_index()
        if save_to is not None:
            p.to_csv(save_to + ".csv", index=False)
        ax = p[p.sentiment == "negative"].plot(x="month", y="rate", title=topic + " (rate)", label="negative")
        p[p.sentiment == "positive"].plot(ax=ax, x="month", y="rate", title=topic + " (rate)", label="positive")
        p[p.sentiment == "neutral"].plot(ax=ax, x="month", y="rate", title=topic + " (rate)", label="neutral")
        if add_vline:
            plt.axvline(x=MAJOR_EVENT_DATE, color="red")
        if save_to is not None:
            plt.savefig(save_to + ".png", bbox_inches='tight')

    def plot_topic_sentiment_rates(self, topic, save_to=None, add_vline=True):
        d1 = self.topic_counts[self.topic_counts.topic == topic][["month", "topic_count"]]
        d2 = self.topic_sentiment_counts[self.topic_sentiment_counts.topic == topic][["sentiment", "month", "count"]]

        result = d2.set_index(["month"]).join(d1.set_index(["month"]), on=["month"])
        result = result[result.topic_count > 0]
        result["rate"] = result["count"]/result["topic_count"]

        p = result.reset_index()
        if save_to is not None:
            p.to_csv(save_to + ".csv", index=False)

        p.pivot(index="month", columns="sentiment", values="rate").plot.area()
        if add_vline:
            plt.axvline(x=MAJOR_EVENT_DATE, color="red")
        if save_to is not None:
            plt.savefig(save_to + ".png", bbox_inches='tight')

    def plot_topic_rate_of_sentiment(self, topic, sentiment, add_vline=True, save_to=None):
        d1 = self.sentiment_counts[self.sentiment_counts.sentiment == sentiment][["month", "sentiment_count"]]
        d2 = self.topic_sentiment_counts[(self.topic_sentiment_counts.topic == topic) & (self.topic_sentiment_counts.sentiment == sentiment)][["month", "count"]].groupby(["month"]).sum().reset_index()

        result = d2.set_index(["month"]).join(d1.set_index(["month"]), on=["month"])
        result["rate"] = result["count"]/result["sentiment_count"]

        p = result.reset_index()
        if save_to is not None:
            p.to_csv(save_to + ".csv", index=False)
        p.plot(x="month", y="rate", title=topic + " (rate from all " + sentiment + ")")
        if add_vline:
            plt.axvline(x=MAJOR_EVENT_DATE, color="red")
        if save_to is not None:
            plt.savefig(save_to + ".png", bbox_inches='tight')
        plt.close()


    def plot_sentiment_rate(self, sentiment, save_to=None):
        d1 = self.monthly_counts[["month", "monthly_count"]]
        d2 = self.sentiment_counts[self.sentiment_counts.sentiment == sentiment][["month", "sentiment_count"]]

        result = d2.set_index(["month"]).join(d1.set_index(["month"]), on=["month"])
        result["rate"] = result["sentiment_count"]/result["monthly_count"]

        p = result.reset_index()
        if save_to is not None:
            p.to_csv(save_to + ".csv", index=False)
        p.plot(x="month", y="rate", title=sentiment + " (rate)")
        if save_to is not None:
            plt.savefig(save_to + ".png", bbox_inches='tight')

    def plot_sentiment_rates(self, save_to=None, add_vline=True):
        d1 = self.monthly_counts[["month", "monthly_count"]]
        d2 = self.sentiment_counts[["sentiment", "month", "sentiment_count"]]

        result = d2.set_index(["month"]).join(d1.set_index(["month"]), on=["month"])
        result["rate"] = result["sentiment_count"]/result["monthly_count"]

        p = result.reset_index()
        if save_to is not None:
            p.to_csv(save_to + ".csv", index=False)

        ax = p[p["sentiment"] == "negative"].plot(x="month", y="rate", label="negative", title="Share of sentiments")
        p[p["sentiment"] == "positive"].plot(ax=ax, x="month", y="rate", label="positive", title="Share of sentiments")
        p[p["sentiment"] == "neutral"].plot(ax=ax, x="month", y="rate", label="neutral", title="Share of sentiments")
        if add_vline:
            plt.axvline(x=MAJOR_EVENT_DATE, color="red")
        if save_to is not None:
            plt.savefig(save_to + ".png", bbox_inches='tight')

    def plot_topics_pie_chart(self, sentiment, save_to=None):
        counts_df = self.topic_sentiments_df[self.topic_sentiments_df.sentiment == sentiment].groupby(["topic"]).count()
        if save_to is not None:
            counts_df.reset_index().to_csv(save_to + ".csv", index=False)
        (counts_df
         .plot.pie(y="date", figsize=DEFAULT_FIGSIZE, legend=None)
         )
        if save_to is not None:
            plt.savefig(save_to + ".png", bbox_inches='tight')

    def plot_topics_bar_chart(self, sentiment, save_to=None):
        df = (self.topic_sentiments_df if sentiment is None else
            self.topic_sentiments_df[self.topic_sentiments_df.sentiment == sentiment])
        counts_df = (df[["topic", "date"]]
                     .groupby(["topic"])
                     .count()
                     .sort_values(by=['date'], ascending=False)
                     )
        counts_df = counts_df / counts_df.sum()
        if save_to is not None:
            counts_df.reset_index().to_csv(save_to + ".csv", index=False)
        title = "Share (%%) of topic among %s" % sentiment if sentiment is not None else "Share (%) of topic"
        (counts_df
         .plot(kind="bar", figsize=DEFAULT_FIGSIZE, legend=None, title=title)
         )
        if save_to is not None:
            plt.savefig(save_to + ".png", bbox_inches='tight')

    def plot_topics_bar_chart_all(self, save_to=None):
        df = self.topic_sentiments_df
        topic_counts_df = (df[["topic", "date"]]
                             .groupby(["topic"])
                             .count()
                             .reset_index())
        topic_counts_df["topic_count"] = topic_counts_df["date"]

        counts_df = (df[["sentiment", "topic", "date"]]
                     .groupby(["sentiment", "topic"])
                     .count()
                     .join(topic_counts_df[["topic", "topic_count"]].set_index(["topic"]), on=["topic"])
                     .sort_values(by=['topic_count', 'sentiment'], ascending=False)
                     )
        counts_df = counts_df / counts_df.sum()
        counts_df["positive"] = counts_df["date"]
        counts_df["negative"] = counts_df["date"]
        counts_df["neutral"] = counts_df["date"]
        counts_df = counts_df.reset_index()

        if save_to is not None:
            counts_df.to_csv(save_to + ".csv", index=False)
        title = "Share (%) of topic"
        base = topic_counts_df.sort_values(by=['topic_count'], ascending=False)[["topic"]].reset_index()
        pos = counts_df[counts_df["sentiment"]=="positive"][["topic", "positive"]]
        neg = counts_df[counts_df["sentiment"]=="negative"][["topic", "negative"]]
        neutral = counts_df[counts_df["sentiment"]=="neutral"][["topic", "neutral"]]
        all = (base.set_index(["topic"])
               .join(pos.set_index(["topic"]), on=["topic"], how="left")
               .join(neg.set_index(["topic"]), on=["topic"], how="left")
               .join(neutral.set_index(["topic"]), on=["topic"], how="left")
               ).reset_index()
        all.plot(kind="bar", figsize=DEFAULT_FIGSIZE, title=title, x="topic", y=["positive", "negative", "neutral"])
        if save_to is not None:
            plt.savefig(save_to + ".png", bbox_inches='tight')

