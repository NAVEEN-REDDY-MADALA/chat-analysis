import streamlit as st
import preprocessor
import helper
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import wordcloud

from helper import most_common_words

st.sidebar.title("WhatsApp Chat Analyzer")

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    raw_text = bytes_data.decode("utf-8")
    df = preprocessor.preprocessor(raw_text)

    # fetch unique users
    user_list=df["user"].unique().tolist()
    user_list.remove("group_notification")
    user_list.sort()
    user_list.insert(0,"overall")
    selected_user=st.sidebar.selectbox("show analysis wrt",user_list)
    if st.sidebar.button("show analysis"):
        num_messages,words,num_media_messages,num_urls_shared=helper.fetch_stats(selected_user,df)
        st.title("Top statistics")
        col1,col2,col3,col4=st.columns(4)

        st.title("Activity Map")
        with col1:
            st.header("Total Messages")
            st.title(num_messages)
        with col2:
            st.header("Total Words")
            st.title(words)
        with col3:
            st.header("Media Files")
            st.title(num_media_messages)
        with col4:
            st.header("URLs Shared")
            st.title(num_urls_shared)
            # timeline

        st.title("Monthly time")
        timeline = helper.monthly_timeline(selected_user, df)
        if timeline is not None and not timeline.empty:

            fig, ax = plt.subplots()
            ax.plot(timeline["time"], timeline["message"],color="green")
            plt.xticks(rotation="vertical")
            st.pyplot(fig)
        else:
            st.warning("No timeline data to plot.")

        st.title("Daily timeline")
        daily_timeline = helper.daily_timeline(selected_user, df)
        if timeline is not None and not timeline.empty:

            fig, ax = plt.subplots()
            ax.plot(daily_timeline["only_date"],daily_timeline["message"],color="orange")
            plt.xticks(rotation="vertical")
            st.pyplot(fig)
        else:
            st.warning("No timeline data to plot.")
# most active days

        if selected_user=="overall":
            st.title("Most busy users")
            x,busy_df=helper.most_busy_users(df)
            fig,ax=plt.subplots()
            col1,col2=st.columns(2)
            with col1:
                ax.bar(x.index, x.values)
                plt.xticks(rotation="vertical",color="red")
                st.pyplot(fig)
            with col2:
                st.dataframe(busy_df)

# activity map
        col1.col2=st.columns(2)
        with col1:
            st.header("Most busy day")
            busy_day=helper.week_activity_map(selected_user, df)
            fig,ax=plt.subplots()
            ax.bar(busy_day.index,busy_day.values)
            st.pyplot(fig)
        with col2:
            st.header("Most busy month")
            busy_month = helper.monthly_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values,color="black")
            st.pyplot(fig)




        st.title("Wordcloud")
        df_wc=helper.create_wordcloud(selected_user,df)
        fig,ax=plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)
        most_common_df = helper.most_common_words(selected_user, df)
        fig, ax = plt.subplots()


        ax.bar(most_common_df['Word'], most_common_df['Count'])
        plt.xticks(rotation="vertical", color="green")
        plt.title("Most common words")
        st.pyplot(fig)
# emoji
        emoji_df=helper.emoji_helper(selected_user, df)
        st.title("emoji analysis")
        col1,col2=st.columns(2)
        with col1:
            st.dataframe(emoji_df)
        with col2:
            fig,ax=plt.subplots()
            ax.pie(emoji_df["Count"],labels=emoji_df["Emoji"], autopct='%1.1f%%')
            st.pyplot(fig)

    st.title("Weekly Activity Map")
    user_heatmap = helper.activity_heatmap(selected_user, df)

    fig, ax = plt.subplots()
    sns.heatmap(user_heatmap, ax=ax)  # Correct call
    st.pyplot(fig)






