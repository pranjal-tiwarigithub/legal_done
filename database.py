import pandas as pd
import streamlit as st

with open(r'C:\Users\pranj\PycharmProjects\Phoneix_Final\Ipc_Sections.csv', errors="ignore") as f:
    table = pd.read_csv(f)

table = table.dropna(how='any')
table.head(100)

table["sections"] = table["Sections "]
table["clauses"] = table["Clauses "]

table = table.drop(["Sections " ,"Clauses " ] , axis = 1 )


import sqlite3


conn = sqlite3.connect('test_database')
c = conn.cursor()

c.execute('CREATE TABLE IF NOT EXISTS products (sections text, clauses text)')
conn.commit()

table.to_sql('products', conn, if_exists='replace', index = False)

c.execute('CREATE TABLE IF NOT EXISTS products (sections text, clauses text)')
conn.commit()

search = input("Enter the crime ")

c.execute(f'SELECT * FROM products WHERE clauses LIKE "% {search} %" ')

answers = []
for row in c.fetchall():
    answers.append(row)
    print (row)




st.subheader("website App")

st.subheader("IPC - Sections ")

search_st = st.text_input('Please enter the keyword here ')

c.execute(f'SELECT * FROM products WHERE clauses LIKE "% {search_st} %" ')

answers = []
for row in c.fetchall():
    answers.append(row)
    print (row)

st.success(answers)
