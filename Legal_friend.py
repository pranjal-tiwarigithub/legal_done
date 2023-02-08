import streamlit as st
import numpy as np
import pandas as pd
import nltk


nltk.download('punkt')
from nltk.tokenize import sent_tokenize

from summarizer.sbert import SBertSummarizer
from summarizer import Summarizer






import warnings
warnings.filterwarnings("ignore", message="Numerical issues were encountered ")



import nltk








def main():
    st.title('Legal Brief Generator 👨‍⚖️')
    menu = ["Home", "Website"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Home":
        legal_brief_new = ""


        st.text('This is a web app to assist legal professionals in generating court briefs')
        from datetime import date

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

        facts = st.text_area(
            'Enter facts about the case (i.e. date and location of incident, history and prior judgements '
            'etc.)')
        legal_brief = legal_brief + "\nFacts of Case: " + facts

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

        legal_brief = legal_brief + "\n\n" + legal_brief_new
        legal_brief = legal_brief + "\n\n\n\nSignature: __________________________ "

        st.download_button('Download file 💾', legal_brief)

    elif choice == "Website":
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
            from newspaper import Article

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
                result = model(text, num_sentences=3)

                st.success(result)

                with open('final.txt', 'w') as f:
                    f.write('Court Proceddings')
                    f.write('\n')
                    for i in answers:
                        f.write(i[0])
                        f.write('\n')

                    f.write(df.to_string())

                    f.write('\n')
                    f.write('Summary of IPC & Case')
                    f.write('\n')
                    f.writelines(result)
                    f.write('\n')


                    #st.download_button('Download txt', f)
                    #st.download_button('Download file 💾', f)

                    def convert_df(df):
                        # IMPORTANT: Cache the conversion to prevent computation on every rerun
                        return df.to_csv().encode('utf-8')

                    csv = convert_df(df)

                    st.download_button(
                        label="Download IPC Sections as CSV",
                        data=csv,
                        file_name='IPC.csv',
                        mime='text/csv',
                    )

                    st.download_button('Download Summary 💾', result)



                    f.close()








if __name__ == '__main__':
    main()