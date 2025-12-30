import streamlit as st
import graph6 as g

st.title("Twitt Generator")

st.write("Generate tweets based on your input!")

form = st.form("tweet_form")

with form:
    topic = form.text_input("Enter the topic for the tweet:")
    tweet_length = form.number_input("Enter the maximum tweet length (in characters):", min_value=1, max_value=280, value=140)
    tone = form.selectbox("Select the tone of the tweet:", ["Formal", "Informal", "Humorous", "Serious"])
    max_evolution = form.number_input("Enter the maximum number of evolutions allowed:", min_value=1, max_value=10, value=3)
    submit = form.form_submit_button("Generate Tweet")

    if submit:
        tweet = g.genTweet(topic, tweet_length, tone, max_evolution)
        st.subheader("Generated Tweet:")
        st.write(tweet['tweet'])

