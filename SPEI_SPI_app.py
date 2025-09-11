## importation des packages 
import pandas as pd
import numpy as np 
import seaborn as sns 
import matplotlib.pyplot as plt
import plotly.express as px
from scipy.stats import fisk, norm
from scipy.stats import gamma, norm
import streamlit as st 

## titre 
st.title("Dashboard des indices SPI et SPEI à partir des données climatiques")
## importation des données 
file = st.file_uploader("📂 Chargez un fichier CSV", type="csv")
sep = st.radio("Choissisez un séparateur :", [",", ";", "\t"], index =  1)

if file :
    df = pd.read_csv(file, sep = sep)
    st.write("Aperçu des données :", df.head())
    ##sélection des colonnes 
    colonnes = df.columns.tolist()
    rain_col = st.selectbox("Pluviométrie:", colonnes)
    tmin_col = st.selectbox("Température minimale :", colonnes)
    tmax_col = st.selectbox("Température maximale :", colonnes)
    rad_col = st.selectbox("Radiation : ", colonnes)

    ##définition de la date 
    if "YEAR" in df.columns and "DOY" in df.columns:
        df["Date"] = pd.to_datetime(df["YEAR"].astype(str) + df["DOY"].astype(str), format="%Y%j")
    else:
        df["Date"] = pd.to_datetime(df.index)  # fallback


    ## imputation des valeurs aberrantes par la médiane (limité ici)
    cols = df.select_dtypes(include =  'number').columns.tolist()
    for p in cols : 
        df[p] = df[p].mask(df[p]<0) ##mettre NaN pour les valeurs aberrantes 
        df = df.fillna(df[df[p]>0].median()) ##imputation par la médiane des valeurs positives

    ## calcul de l'évapotranspiration avec la méthode de Hargreaves 
    df['Tmean'] = (df[tmin_col] + df[tmax_col]) / 2
    df['ET0'] = 0.0023 * (df[tmax_col] - df[tmin_col])**0.5 * (
        df['Tmean'] + 17.8) * df[rad_col]
    df['Deficit'] = df[rain_col] - df['ET0']

    ## calcul du SPEI 
    df['SPEI30'] = df["Deficit"].rolling(window = 30).sum()  ##cumul sur fenêtre glissante
    spei = df['SPEI30'].dropna()
    params = fisk.fit(spei)  ## ajustement log-logistique
    F_x = fisk.cdf(spei, *params) ##CDF pour chaque valeur
    SPEI30 = norm.ppf(F_x) ##SPEI en bonne et due forme 
    df.loc[spei.index, 'SPEI30'] = SPEI30 ##ajout à la base de données 

    ## calcul du SPI
    df['SPI30'] = df[rain_col].rolling(window = 30).sum()  ##cumul sur fenêtre glissante
    spi = df['SPI30'].dropna()
    parms = gamma.fit(spi) ##ajustement gamma
    F_x = gamma.cdf(spi, *parms) ##CDF pour chaque valeur
    SPI30 = norm.ppf(F_x) ##SPEI en bonne et due forme 
    df.loc[spi.index, 'SPI30'] = SPI30 ##ajout à la base de données 

    ## graphique 
    import plotly.graph_objects as go
    fig = go.Figure()
    # Courbe SPEI
    fig.add_trace(go.Scatter(
        x=df.index,
        y=df["SPEI30"],
        mode="lines",
        name="SPEI30",
        line=dict(color="blue", width=2)
        ))
    # Courbe SPI
    fig.add_trace(go.Scatter(
        x=df.index,
        y=df["SPI30"],
        mode="lines",
        name="SPI30",
        line=dict(color="black", width=1),
        opacity=0.7
        ))

     # Lignes de référence
    fig.add_hline(y=0, line=dict(color="black", dash="dash"))
    fig.add_hline(y=-1, line=dict(color="red", dash="dash"), annotation_text="Début sécheresse")
    fig.add_hline(y=-2, line=dict(color="darkred", dash="dash"), annotation_text="Sécheresse intense")
    fig.add_hline(y=1, line=dict(color="blue", dash="dash"), annotation_text="Humide")
    fig.add_hline(y=2, line=dict(color="darkblue", dash="dash"), annotation_text="Très humide")

    # Layout
    fig.update_layout(
        title="Évolution SPI & SPEI (fenêtre de 30 jours)",
        xaxis_title="Date",
        yaxis_title="Indice",
        template="plotly_white",
        legend=dict(orientation="h", y=-0.2)
    )
    st.plotly_chart(fig, use_container_width=True)

