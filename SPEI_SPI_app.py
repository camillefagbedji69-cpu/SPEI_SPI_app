## importation des packages 
import pandas as pd
import numpy as np
import streamlit as st
import plotly.graph_objects as go
from scipy.stats import fisk, gamma, norm

## titre 
st.title("📊 Dashboard des indices SPI et SPEI à partir des données climatiques")

## upload du fichier
file = st.file_uploader("📂 Chargez un fichier CSV", type="csv")

if file:
    sep = st.radio("Choisissez un séparateur :", [",", ";", "\t"], index=1)
    df = pd.read_csv(file, sep=sep)
    st.write("Aperçu des données :", df.head())

    # Sélection des colonnes
    colonnes = df.columns.tolist()
    rain_col = st.selectbox("Pluviométrie :", colonnes)
    tmin_col = st.selectbox("Température minimale :", colonnes)
    tmax_col = st.selectbox("Température maximale :", colonnes)
    rad_col = st.selectbox("Radiation :", colonnes)

    # Conversion forcée en numérique
    df[rain_col] = pd.to_numeric(df[rain_col], errors="coerce")
    df[tmin_col] = pd.to_numeric(df[tmin_col], errors="coerce")
    df[tmax_col] = pd.to_numeric(df[tmax_col], errors="coerce")
    df[rad_col] = pd.to_numeric(df[rad_col], errors="coerce")

    # Définition de la date
    if "YEAR" in df.columns and "DOY" in df.columns:
        df["Date"] = pd.to_datetime(df["YEAR"].astype(str) + df["DOY"].astype(str), format="%Y%j")
    else:
        df["Date"] = pd.to_datetime(df.index)  # fallback

    # Imputation des valeurs aberrantes par médiane
    cols_num = df.select_dtypes(include="number").columns.tolist()
    for col in cols_num:
        df[col] = df[col].mask(df[col] < 0)
        median_val = df.loc[df[col] > 0, col].median()
        df[col] = df[col].fillna(median_val)

    # Calcul ET0 (Hargreaves)
    df["Tmean"] = (df[tmin_col] + df[tmax_col]) / 2
    df["ET0"] = 0.0023 * np.sqrt(df[tmax_col] - df[tmin_col]) * (df["Tmean"] + 17.8) * df[rad_col]
    df["Deficit"] = df[rain_col] - df["ET0"]

    # Calcul du SPEI
    df["SPEI30"] = df["Deficit"].rolling(window=30).sum()
    spei = df["SPEI30"].dropna()
    if len(spei) > 10:  # vérifier assez de données
        params = fisk.fit(spei)
        F_x = fisk.cdf(spei, *params)
        SPEI30 = norm.ppf(F_x)
        df.loc[spei.index, "SPEI30"] = SPEI30
    else:
        st.warning("⚠️ Pas assez de données valides pour calculer le SPEI30.")
        df["SPEI30"] = np.nan

    # Calcul du SPI
    df["SPI30"] = df[rain_col].rolling(window=30).sum()
    spi = df["SPI30"].dropna()
    if len(spi) > 10:
        parms = gamma.fit(spi)
        F_x = gamma.cdf(spi, *parms)
        SPI30 = norm.ppf(F_x)
        df.loc[spi.index, "SPI30"] = SPI30
    else:
        st.warning("⚠️ Pas assez de données valides pour calculer le SPI30.")
        df["SPI30"] = np.nan

    # Graphique interactif
    fig = go.Figure()

    # Courbe SPEI
    fig.add_trace(go.Scatter(
        x=df["Date"],
        y=df["SPEI30"],
        mode="lines",
        name="SPEI30",
        line=dict(color="blue", width=2)
    ))

    # Courbe SPI
    fig.add_trace(go.Scatter(
        x=df["Date"],
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

