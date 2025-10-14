from emoji import analyze
from urlextract import URLExtract
from wordcloud import WordCloud
from collections import Counter
import pandas as pd
from nltk.corpus import stopwords
import emoji
import streamlit as st
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
analyzer =SentimentIntensityAnalyzer()




def fetch_stats(selected_user, df):
    extractor = URLExtract()

    if selected_user == "overall":
        num_messages = df.shape[0]

        words = []
        all_urls = []
        for message in df["message"]:
            words.extend(message.split())
            # Extract URLs from each message
            urls_in_message = extractor.find_urls(message)
            all_urls.extend(urls_in_message)

        # Count media messages
        num_media_messages = df[df['message'] == '<Media omitted>'].shape[0]

        # Count total URLs shared
        num_urls_shared = len(all_urls)

        return num_messages, len(words), num_media_messages, num_urls_shared
    else:
        new_df = df[df["user"] == selected_user]
        num_messages = new_df.shape[0]

        words = []
        all_urls = []
        for message in new_df["message"]:
            words.extend(message.split())
            # Extract URLs from each message
            urls_in_message = extractor.find_urls(message)
            all_urls.extend(urls_in_message)

        # Count media messages for selected user
        num_media_messages = new_df[new_df['message'] == '<Media omitted>'].shape[0]

        # Count URLs shared by selected user
        num_urls_shared = len(all_urls)

        return num_messages, len(words), num_media_messages, num_urls_shared
def most_busy_users(df):
        x= df["user"].value_counts().head()
        busy_users=round((df["user"].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(
            columns={"user": "Name", "count": "MessagePercentage"})
        return x,busy_users
def create_wordcloud(selected_user, df):
    from wordcloud import WordCloud
    if selected_user == "overall":
        wc = WordCloud(width=500, height=500, min_font_size=10, background_color="white")
        df_wc = wc.generate(df["message"].str.cat(sep=" "))
        return df_wc
    else:
        # For specific user, filter the DataFrame or handle differently
        user_df = df[df["user"] == selected_user]
        wc = WordCloud(width=500, height=500, min_font_size=10, background_color="white")
        df_wc = wc.generate(user_df["message"].str.cat(sep=" "))
        return df_wc


def most_common_words(selected_user, df):
    stop_words = set(stopwords.words("english"))

    if selected_user == "overall":
        messages = df["message"]
    else:
        filtered_df = df[df["user"] == selected_user]
        messages = filtered_df["message"]

    words = []
    for message in messages:
        message_str = str(message).strip().lower()
        if not message_str or "<media omitted>" in message_str:
            continue
        for word in message_str.split():
            if word not in stop_words:
                words.append(word)

    print("Total filtered words:", len(words))
    if not words:
        print("No words found for selected user/messages!")

    most_common = Counter(words).most_common(20)
    print("Most common words:", most_common)

    result_df = pd.DataFrame(most_common, columns=['Word', 'Count'])
    return result_df


def emoji_helper(selected_user, df):
    if selected_user != "overall":
        df = df[df["user"] == selected_user]
    emojis = []
    for message in df["message"]:
        emojis.extend([c for c in str(message) if c in emoji.EMOJI_DATA])
    emoji_df = pd.DataFrame(Counter(emojis).most_common(10), columns=["Emoji", "Count"])
    return emoji_df

# monthly timeline
def monthly_timeline(selected_user, df):
    # Filter for a specific user, if not 'overall'
    if selected_user != "overall":
        df = df[df["user"] == selected_user]

    # Group by year, month number, month name and count messages
    timeline = df.groupby(["year", "month_num", "month"]).count()["message"].reset_index()

    # Create a column with combined labels
    timeline["time"] = timeline["month"] + " - " + timeline["year"].astype(str)
    return timeline

# daily timeline
def daily_timeline(selected_user,df):
    if selected_user !="overall":
        df=df[df["user"]==selected_user]
    daily_timeline = df.groupby("only_date").count()["message"].reset_index()
    return daily_timeline

def week_activity_map(selected_user,df):
    if selected_user !="overall":
        df=df[df["user"]==selected_user]
    return df["day_name"].value_counts()

def monthly_activity_map(selected_user,df):
    if selected_user != "overall":
        df = df[df["user"] == selected_user]
    return df["month"].value_counts()
def activity_heatmap(selected_user,df):
    if selected_user != "overall":
        df = df[df["user"] == selected_user]
    user_heatmap=df.pivot_table(index="day_name", columns="period", values="message", aggfunc="count").fillna(0)
    return user_heatmap




