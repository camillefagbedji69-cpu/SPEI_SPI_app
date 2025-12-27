# Hydro-Climate Dashboard: SPI & SPEI Interactive Analysis Tool

## 📌 Context & Overview
Monitoring water deficits and rainfall excess is vital for precision agriculture and water resource management. This project delivers an interactive web-based dashboard designed to quantify and visualize drought and humidity levels through the **Standardized Precipitation Index (SPI)** and the **Standardized Precipitation-Evapotranspiration Index (SPEI)**.

## 🎯 Objectives
* **Dynamic Index Calculation:** Computing 30-day rolling SPI and SPEI indices from raw climate data.
* **Automated Detection:** Identifying extreme drought and humidity episodes using standardized thresholds.
* **Decision Support:** Providing an intuitive interface for environmental managers to analyze local hydric stress.

## 🛠️ Tech Stack & Implementation
* **Framework:** `Streamlit` (Web Interface)
* **Visualization:** `Plotly` (Interactive Time-Series)
* **Statistics:** `Scipy.stats` (Gamma distribution for SPI, Fisk/Log-logistic for SPEI), `Numpy`, `Pandas`.
* **Deployment:** GitHub & Streamlit Cloud.

### Core Features:
1. **Flexible Data Ingestion:** Upload any CSV with rainfall, temperature, and radiation data.
2. **On-the-fly Physics:** Real-time calculation of Reference Evapotranspiration ($ET_0$) via the Hargreaves equation.
3. **Statistical Robustness:** Automatic outlier imputation and data normalization.
4. **Conditional Visualization:** Toggle between indices and view drought reference lines (Thresholds at ±1.0, ±1.5, and ±2.0).



## 🚀 Key Results
* **Functional Dashboard:** A robust tool capable of handling heterogeneous CSV formats.
* **Real-time Insights:** Users can immediately identify "Severe" or "Extreme" drought periods (e.g., SPEI < -1.5).
* **Interactive Exploration:** Zoomable and hover-capable charts to pinpoint specific dates of climatic stress.

## 🔮 Perspectives for Improvement
* **Temporal Sliders:** Allowing users to adjust the rolling window scale (e.g., 7-day for flash droughts, 90-day for seasonal monitoring).
* **Spatial Integration:** Adding heatmaps and interactive maps for regional hydric analysis.
* **Export Functionality:** Direct CSV download of the calculated indices and statistics.

## URL de l'application 
https://speispiapp-uiycpejdavnvsb7rmqfzd8.streamlit.app/
