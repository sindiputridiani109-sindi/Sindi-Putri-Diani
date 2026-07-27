"""
Analisis Klaster Lokasi Gerai Kopi dan Deteksi Zona Sepi
=========================================================
Aplikasi Streamlit untuk:
1. Meng-cluster lokasi gerai kopi berdasarkan koordinat (latitude, longitude)
2. Menandai klaster mana yang tergolong "Ramai" atau "Sepi" berdasarkan
   jumlah gerai dalam klaster tersebut
3. Memvisualisasikan hasil clustering pada scatter plot geografis
4. Menerima input lokasi baru dan memprediksi klaster + status zona
   (ramai / sepi) untuk lokasi tersebut

Cara menjalankan:
    streamlit run app.py
"""

import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
from sklearn.cluster import KMeans

st.set_page_config(
    page_title="Klaster Gerai Kopi & Zona Sepi",
    page_icon="☕",
    layout="wide",
)

st.title("☕ Analisis Klaster Lokasi Gerai Kopi dan Deteksi Zona Sepi")

st.markdown(
    """
Aplikasi ini menggunakan **algoritma clustering (K-Means)** untuk menganalisis
persebaran gerai kopi berdasarkan koordinat geografis (*latitude* & *longitude*),
lalu menentukan zona mana yang **ramai** (padat gerai) dan zona mana yang
berisiko **sepi** (jarang gerai / berjauhan dari gerai lain), berdasarkan
jumlah gerai per klaster.
"""
)

# ---------------------------------------------------------------------------
# 1. Load Data
# ---------------------------------------------------------------------------
st.sidebar.header("1️⃣ Data Gerai Kopi")

uploaded_file = st.sidebar.file_uploader(
    "Upload CSV (kolom wajib: nama, latitude, longitude)", type=["csv"]
)

@st.cache_data
def load_default_data():
    return pd.read_csv("sample_data.csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.sidebar.success(f"Data berhasil diupload: {len(df)} baris")
else:
    df = load_default_data()
    st.sidebar.info("Menggunakan data contoh (sample_data.csv). Upload data asli untuk hasil nyata.")

required_cols = {"latitude", "longitude"}
if not required_cols.issubset(set(c.lower() for c in df.columns)):
    st.error("File CSV harus memiliki kolom 'latitude' dan 'longitude'.")
    st.stop()

# Normalisasi nama kolom
df.columns = [c.lower() for c in df.columns]
if "nama" not in df.columns:
    df["nama"] = [f"Gerai {i+1}" for i in range(len(df))]

with st.expander("Lihat data mentah"):
    st.dataframe(df, use_container_width=True)

# ---------------------------------------------------------------------------
# 2. Parameter Clustering
# ---------------------------------------------------------------------------
st.sidebar.header("2️⃣ Parameter Clustering")

k = st.sidebar.slider("Jumlah klaster (K)", min_value=2, max_value=10, value=4)
sepi_threshold = st.sidebar.slider(
    "Ambang batas jumlah gerai per klaster (di bawah ini = Zona Sepi)",
    min_value=1,
    max_value=30,
    value=max(3, int(len(df) / k * 0.4)),
)

# ---------------------------------------------------------------------------
# 3. Clustering (K-Means)
# ---------------------------------------------------------------------------
coords = df[["latitude", "longitude"]].to_numpy()

kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
df["klaster"] = kmeans.fit_predict(coords).astype(str)
centroids = kmeans.cluster_centers_

# Hitung jumlah gerai per klaster -> tentukan status ramai / sepi
cluster_counts = df["klaster"].value_counts().to_dict()
status_map = {
    c: ("Sepi" if cnt < sepi_threshold else "Ramai")
    for c, cnt in cluster_counts.items()
}
df["status_zona"] = df["klaster"].map(status_map)

# ---------------------------------------------------------------------------
# 4. Visualisasi
# ---------------------------------------------------------------------------
st.subheader("📍 Visualisasi Hasil Clustering")

col1, col2 = st.columns([3, 1])

with col1:
    fig = px.scatter_mapbox(
        df,
        lat="latitude",
        lon="longitude",
        color="klaster",
        symbol="status_zona",
        hover_name="nama",
        hover_data={"status_zona": True, "klaster": True, "latitude": ":.4f", "longitude": ":.4f"},
        zoom=11,
        height=550,
        mapbox_style="open-street-map",
        title="Persebaran Gerai Kopi berdasarkan Klaster",
    )
    # Tandai centroid tiap klaster
    fig.add_scattermapbox(
        lat=centroids[:, 0],
        lon=centroids[:, 1],
        mode="markers",
        marker=dict(size=16, symbol="star", color="black"),
        name="Pusat Klaster",
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.markdown("**Ringkasan Klaster**")
    summary = (
        df.groupby("klaster")
        .agg(jumlah_gerai=("nama", "count"), status=("status_zona", "first"))
        .reset_index()
        .sort_values("klaster")
    )
    st.dataframe(summary, use_container_width=True, hide_index=True)

    n_sepi = (df["status_zona"] == "Sepi").sum()
    n_ramai = (df["status_zona"] == "Ramai").sum()
    st.metric("Gerai di Zona Ramai", n_ramai)
    st.metric("Gerai di Zona Sepi", n_sepi)

# Scatter plot koordinat murni (tanpa peta latar, sesuai permintaan tugas)
st.subheader("📊 Scatter Plot Klaster (Latitude vs Longitude)")
fig2 = px.scatter(
    df,
    x="longitude",
    y="latitude",
    color="klaster",
    symbol="status_zona",
    hover_name="nama",
    title="Scatter Plot Klaster Gerai Kopi",
    height=500,
)
fig2.add_scatter(
    x=centroids[:, 1],
    y=centroids[:, 0],
    mode="markers",
    marker=dict(size=14, symbol="x", color="black"),
    name="Pusat Klaster",
)
st.plotly_chart(fig2, use_container_width=True)

# ---------------------------------------------------------------------------
# 5. Input Lokasi Baru -> Prediksi Klaster & Status
# ---------------------------------------------------------------------------
st.subheader("📌 Cek Lokasi Baru")
st.markdown("Masukkan koordinat lokasi baru untuk mengetahui klaster dan status zonanya.")

c1, c2, c3 = st.columns([1, 1, 1])
with c1:
    input_lat = st.number_input("Latitude", value=float(df["latitude"].mean()), format="%.6f")
with c2:
    input_lon = st.number_input("Longitude", value=float(df["longitude"].mean()), format="%.6f")
with c3:
    st.write("")
    st.write("")
    cek = st.button("🔍 Analisis Lokasi", use_container_width=True)

if cek:
    new_point = np.array([[input_lat, input_lon]])
    pred_cluster = kmeans.predict(new_point)[0]
    pred_status = status_map.get(str(pred_cluster), "Tidak diketahui")

    dist_to_centroid = np.linalg.norm(centroids[pred_cluster] - new_point[0])

    st.success(
        f"📍 Lokasi ({input_lat:.5f}, {input_lon:.5f}) termasuk **Klaster {pred_cluster}** "
        f"dan tergolong zona **{pred_status.upper()}**."
    )
    st.info(
        f"Jarak ke pusat klaster: {dist_to_centroid:.5f} (satuan derajat koordinat) · "
        f"Jumlah gerai di klaster ini: {cluster_counts.get(pred_cluster, 0)}"
    )

    # tampilkan titik baru di peta
    fig3 = px.scatter(
        df,
        x="longitude",
        y="latitude",
        color="klaster",
        symbol="status_zona",
        title="Posisi Lokasi Baru terhadap Klaster yang Ada",
    )
    fig3.add_scatter(
        x=[input_lon],
        y=[input_lat],
        mode="markers",
        marker=dict(size=18, symbol="star", color="red"),
        name="Lokasi Baru",
    )
    st.plotly_chart(fig3, use_container_width=True)

st.markdown("---")
st.caption(
    "Catatan: Status 'Sepi'/'Ramai' ditentukan berdasarkan jumlah gerai pada klaster "
    "yang sama dibandingkan dengan ambang batas yang bisa diatur di sidebar. "
    "Semakin sedikit gerai dalam suatu klaster, semakin besar kemungkinan area "
    "tersebut adalah zona sepi."
)
