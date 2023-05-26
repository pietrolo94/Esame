import streamlit as st
import pandas as pd
import joblib
import io
import numpy as np

def add_bg_from_url():
    st.markdown(
         f"""
         <style>
         .stApp {{
             background-image: url("https://w.wallhaven.cc/full/96/wallhaven-968zwd.jpg");
             background-attachment: fixed;
             background-size: cover
         }}
         </style>
         """,
         unsafe_allow_html=True
     )

def main():
    st.markdown('<div align="center"><h1>Aspettativa di vita</h1></div>', unsafe_allow_html=True)

    newmodel = joblib.load("Life_exp.pkl")
    adult_mortality = st.number_input("Adult mortality")
    hiv_aids = st.number_input("HIV or AIDS")
    income = st.number_input("Income composition of resources")
    schooling = st.number_input("Schooling")
    res = newmodel.predict([[adult_mortality,hiv_aids, income, schooling]])[0]
    st.write(f"aspettativa di vita: {round(res, 1)} anni")


    # Parte per caricare il file CSV o Excel
    st.header("Caricamento dati")
    file = st.file_uploader("Carica un file CSV o Excel", type=["csv", "xlsx"])
    if file is not None:
        if file.type.startswith('application/vnd.openxmlformats-officedocument.spreadsheetml'):
            df = pd.read_excel(file, engine='openpyxl')
        else:
            df = pd.read_csv(file)
        dfx = df[['Adult Mortality',' HIV/AIDS','Income composition of resources','Schooling']]
        # Mostra i dati caricati
        st.write("Dati caricati:")
        st.write(df)

        # Previsione dei dati usando il modello di regressione lineare
        st.header("Previsione aspettativa di vita")
        predictions = newmodel.predict(dfx)
        df['Predizione aspettativa di vita'] = np.round(predictions,1)
        st.write("Risultati previsione:")
        st.write(df)
        # Aggiungi un pulsante per il download del file
        output = io.BytesIO()
        writer = pd.ExcelWriter(output, engine='xlsxwriter')
        df.to_excel(writer,sheet_name='Profit_prediction', index=False)
        writer.save()
        output.seek(0)
        st.download_button(
            label="Scarica file Excel",
            data=output,
            file_name='Life_exp_prediction.xlsx',
            mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    add_bg_from_url()
if __name__ == '__main__':
	main()