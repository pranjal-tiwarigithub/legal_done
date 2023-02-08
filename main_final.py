import streamlit as st
import numpy as np
import pandas as pd
import nltk


nltk.download('punkt')
from nltk.tokenize import sent_tokenize
from datetime import date
from summarizer.sbert import SBertSummarizer
from summarizer import Summarizer
from newspaper import Article

menu = ["Home", "Website", "Indicator"]
choice = st.sidebar.selectbox("Menu", menu)

legal_brief_new = ""

st.title('Legal Brief Generator 👨‍⚖️')
st.text('This is a web app to assist legal professionals in generating court briefs')

today = date.today()
d2 = today.strftime("%B %d, %Y")
st.write(d2)

legal_brief = "Date: " + d2

case_number = st.text_input("Enter Case Number")
legal_brief = legal_brief + "\nCase Number: " + case_number

category = st.text_input("Enter Category of case")
category = category.lower()

title = st.text_input('Enter the title of the case')
legal_brief = legal_brief + "\nTitle: " + title

plaintiff = st.text_input('Enter the name of the plaintiff')
legal_brief = legal_brief + "\nName of Plaintiff: " + plaintiff
defendant = st.text_input('Enter the name of the defendant')
legal_brief = legal_brief + "\nName of Defendant: " + defendant
choice = st.radio('You represent the:', ['Plaintiff', 'Defendant'])
facts = st.text_area('Enter facts about the case (i.e. date and location of incident, history and prior judgements '
                     'etc.)')

data = pd.read_csv('Court Arguments - final.csv')

crime2_input = None
type2_input = None

if choice == "Defendant":
    type2_input = 1

elif choice == "Plaintiff":
    type2_input = 2

if category == "drunk driving":
    crime2_input = 0

elif category == "corruption":
    crime2_input = 1

elif category == "murder":
    crime2_input = 2

elif category == "theft":
    crime2_input = 3

elif category == "rape":
    crime2_input = 4

elif category == "drugs":
    crime2_input = 5

elif category == "financial fraud":
    crime2_input = 6

elif category == "cybercrime":
    crime2_input = 7

if st.button("Submit"):
    st.header("Possible Arguments")
    legal_brief_new = "\nPossible Arguments"

    if (crime2_input != None and type2_input != None):
        paragraph = data.iloc[crime2_input, type2_input]
        for sentence in sent_tokenize(paragraph):
            st.write(sentence)
            legal_brief_new = legal_brief_new + "\n" + sentence

        st.subheader("IPC (Indian Penal Code) - Sections")

        from newspaper import Article

        import sqlite3

        conn = sqlite3.connect('test_database')
        c = conn.cursor()

        search_st = category

        c.execute(f'SELECT * FROM products WHERE clauses LIKE "% {search_st} %" ')

        answers = []
        for row in c.fetchall():
            answers.append(row)
            print(row)

        if len(answers) != 0:
            st.success("IPC Suggestions")
            arr = np.array(answers)

            df = pd.DataFrame(
                data=arr,
                columns=("Sections", "Clauses"))

            st.table(df)

        if len(answers) != 0:

            url = st.text_input('Please enter the URL here ')



            st.write(url)
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
            result = model(text, num_sentences=3)

            st.success(result)
            legal_brief = legal_brief + result

legal_brief = legal_brief + "\n\n" + legal_brief_new
legal_brief = legal_brief + "\n\n\n\nSignature: __________________________ "

st.download_button('Download file 💾', legal_brief)
