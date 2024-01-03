import mysql.connector
from mysql.connector import Error
import pandas as pd
import streamlit as st

#Configuração do Banco de Dados
def create_db_connection(host_name, user_name, user_password, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name
        )
        print("MySQL Database connection successful")
    except Error as err:
        print(f"Error: '{err}'")

    return connection

connection = create_db_connection("192.185.213.59", "forsa432_portal", "Portal2023*", "forsa432_portal")

#Consulta do Banco de Dados
def read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as err:
        print(f"Error: '{err}'")

q1 = """
SELECT *
FROM rise_invoice_items;
"""
results = read_query(connection, q1)

from_db = []

for result in results:
   result = list(result)
   from_db.append(result)

columns = ["id", "Tipo de Negócio", "Descrição", "Qtd.", "Unid.", "Montante", "Total", "sort", "invoice_id", "item_id", "taxable", "deleted"]
df = pd.DataFrame(from_db, columns=columns)

#Configuração da Página
st.set_page_config(page_title="Dashboards NSGi")

with st.container():
    st.subheader("Dashboards NSGi")
    st.title("Dashboard Comercial")
    st.subheader("Negócios")

with st.container():
    st.write("---")
    # Contagem dos negócios por tipo
    count_by_type = df['Tipo de Negócio'].value_counts()

    # Criando o gráfico de barras usando st.bar_chart
    st.bar_chart(count_by_type)
    
    total_by_type = df.groupby("Tipo de Negócio")["Total"].sum()

    # Criando o gráfico de barras usando st.bar_chart
    chart = st.bar_chart(total_by_type)