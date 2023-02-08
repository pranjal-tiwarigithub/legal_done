import streamlit as st
import pandas as pd
import numpy as np
from newspaper import Article

import nltk
nltk.download('punkt')

def main():
    st.subheader("website App")

    st.subheader("IPC - Sections ")

    import sqlite3


    conn = sqlite3.connect('test_database')
    c = conn.cursor()

    search_st = st.text_input('Please enter the keyword here ')

    c.execute(f'SELECT * FROM products WHERE clauses LIKE "% {search_st} %" ')

    answers = []
    for row in c.fetchall():
        answers.append(row)
        print (row)

    if len(answers)!= 0:
        st.success("IPC Suggestions")
        arr = np.array(answers)

        df = pd.DataFrame(
            data=arr,
            columns=("Sections", "Clauses"))

        st.table(df)


    if len(answers)!= 0:

        url = st.text_input('Please enter the URL here ')

        if (url):
    # create an article object
            article = Article(url)
            article.download()
            article.parse()
            article.nlp()

            title = article.title
            link = article.url
            authors = article.authors
            date = article.publish_date
            image = article.top_image
            summary = article.summary
            text = article.text


            from summarizer import Summarizer
            from summarizer.sbert import SBertSummarizer

            model = SBertSummarizer('paraphrase-MiniLM-L6-v2')
            result = model(text , num_sentences=3)

            st.success(result)



if __name__ == '__main__':
	main()

