import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from pathlib import Path

# Tentukan jalur file dataset lokal
DATA_FILENAME = Path(__file__).parent / 'data/day.csv'

# Judul dan pengantar
st.title('Analisis Data Bike Sharing')
st.write("""
    Selamat datang di aplikasi **Analisis Data Bike Sharing**! 
    Proyek ini menganalisis data (https://www.kaggle.com/datasets/lakshmi25npathi/bike-sharing-dataset?resource=download) peminjaman sepeda untuk menjawab pertanyaan bisnis utama:
    - Berapa banyak sepeda yang disewa oleh pengguna kasual dibandingkan dengan pengguna terdaftar?
    - Berapa rata-rata jumlah sepeda yang disewa per hari?
    - Bagaimana kecepatan angin dan suhu mempengaruhi penyewaan sepeda?
    
    Mari kita mulai dengan menganalisis data!
    """)

# Baca dataset lokal
try:
    data = pd.read_csv(DATA_FILENAME)

    # Menampilkan beberapa baris awal dari dataset
    st.subheader('Tinjauan Data')
    st.write(data.head())

    # 1. Perbandingan pengguna kasual vs terdaftar
    st.header('Peminjaman Pengguna Kasual vs Terdaftar')
    st.write("""
        Pertama, kita ingin memahami berapa banyak sepeda yang disewa oleh pengguna kasual dibandingkan dengan pengguna terdaftar. 
        Grafik di bawah ini menunjukkan perbandingan antara kedua kategori ini.
        """)

    # Hitung total peminjaman untuk pengguna kasual dan terdaftar
    total_casual = data['casual'].sum()
    total_registered = data['registered'].sum()

    # Membuat pie chart
    labels = ['Pengguna Kasual', 'Pengguna Terdaftar']
    sizes = [total_casual, total_registered]
    colors = ['skyblue', 'lightgreen']
    explode = (0.1, 0)  # Hanya meledakkan bagian pengguna kasual

    fig, ax = plt.subplots()
    ax.pie(sizes, explode=explode, labels=labels, colors=colors,
           autopct='%1.1f%%', shadow=True, startangle=90)
    ax.set_title('Proporsi Peminjaman oleh Pengguna Kasual vs Terdaftar')
    ax.axis('equal')  # Mengatur agar pie chart berbentuk lingkaran

    st.pyplot(fig)

    st.write("""
        **Insight:** 
        - Proporsi Penyewaan oleh Pengguna Kasual vs Pengguna Terdaftar:
            * Berdasarkan grafik pertama (diagram pie), pengguna terdaftar mendominasi penyewaan sepeda, menyumbang 81.2% dari total penyewaan, sementara pengguna kasual hanya menyumbang 18.8%.
            * Ini menunjukkan bahwa mayoritas penyewaan dilakukan oleh pengguna yang telah terdaftar, mungkin karena mereka lebih sering menggunakan layanan ini atau mendapatkan keuntungan khusus dibandingkan pengguna kasual berlangganan layanan ini.
        """)

    # 2. Rata-rata peminjaman sepeda per hari
    st.header('Peminjaman Sepeda Seiring Waktu')
    st.write("""
        Memahami bagaimana peminjaman sepeda berubah seiring waktu dapat membantu bisnis menyesuaikan operasionalnya.
        Di bawah ini adalah tren peminjaman sepeda sepanjang dataset.
        """)

    fig, ax = plt.subplots()
    sns.lineplot(data=data, x=data.index, y='cnt', ax=ax, label='Total Peminjaman')
    ax.set_xlabel('Hari')
    ax.set_ylabel('Jumlah Peminjaman')
    st.pyplot(fig)

    st.header('Rata-rata Peminjaman Sepeda per Hari')
    
    st.write("""
        Rata-rata jumlah sepeda yang disewa per hari memberikan wawasan tentang tren penggunaan secara keseluruhan.
        """)

    avg_rentals = data['cnt'].mean()
    st.metric(label="Rata-rata Peminjaman per Hari", value=f"{avg_rentals:.2f}")

    st.write("""
        **Insight:** 
        - Rata-rata Penyewaan Sepeda per Hari:
            * Grafik kedua menunjukkan jumlah penyewaan sepeda per hari sepanjang tahun, yang menunjukkan adanya tren musiman yang jelas. Penyewaan sepeda meningkat dari awal tahun, mencapai puncaknya pada musim panas (sekitar Juli-Agustus), dan menurun tajam menjelang musim dingin.
            * Rata-rata penyewaan sepeda harian selama periode puncak berkisar antara 4000-6000 sepeda per hari, dengan variasi harian yang cukup besar. Ini mengindikasikan adanya pengaruh cuaca atau musim terhadap permintaan penyewaan sepeda.nerja utama untuk pertumbuhan bisnis.
        """)

    # 3. Dampak kecepatan angin dan suhu
    
    st.header('Dampak Kecepatan Angin dan Suhu pada Peminjaman')
    st.write("""
        Lingkungan dapat berdampak signifikan pada penyewaan sepeda. 
        Mari kita analisis bagaimana suhu dan kecepatan angin mempengaruhi penggunaan sepeda.
        """)

    fig, ax = plt.subplots()
    sns.scatterplot(data=data, x='temp', y='cnt', ax=ax, label='Suhu', color='blue')
    sns.scatterplot(data=data, x='windspeed', y='cnt', ax=ax, label='Kecepatan Angin', color='orange')
    ax.set_xlabel('Suhu / Kecepatan Angin')
    ax.set_ylabel('Jumlah Peminjaman')
    ax.legend()
    st.pyplot(fig)

    st.write("""
        **Insight:**
        - Pengaruh Kecepatan Angin dan Suhu terhadap Penyewaan Sepeda:
            * Kecepatan Angin: Berdasarkan scatter plot dan nilai korelasi -0.23, ada hubungan negatif yang lemah antara kecepatan angin dan penyewaan sepeda. Ketika kecepatan angin meningkat, jumlah penyewaan cenderung menurun. Namun, karena nilai korelasi ini rendah, dampaknya tidak terlalu signifikan. Ini bisa disebabkan oleh kenyamanan bersepeda yang menurun saat angin lebih kencang, meskipun tidak selalu menjadi faktor yang menghalangi.
            * Suhu: Scatter plot menunjukkan adanya korelasi positif yang kuat antara suhu dan penyewaan sepeda, didukung dengan nilai korelasi 0.63. Saat suhu meningkat, jumlah penyewaan sepeda juga meningkat secara signifikan. Ini menunjukkan bahwa orang lebih suka bersepeda ketika cuaca lebih hangat. Pada suhu optimal, jumlah penyewaan bisa mencapai 6000-8000 sepeda per hari.
        """)

    # Kesimpulan
    st.header('Kesimpulan')
    st.write("""
        * Pengguna terdaftar lebih dominan dalam menggunakan layanan penyewaan sepeda dibandingkan pengguna kasual.
        * Penyewaan sepeda menunjukkan pola musiman, dengan puncaknya terjadi selama musim panas.
        * Suhu merupakan faktor yang memiliki dampak signifikan terhadap penyewaan sepeda. Semakin hangat cuaca, semakin banyak sepeda yang disewa. Kecepatan angin, meskipun memiliki dampak negatif, pengaruhnya relatif kecil terhadap keputusan penyewaan.
        """)

except FileNotFoundError:
    st.error(f"File {DATA_FILENAME} tidak ditemukan. Pastikan file berada di direktori yang benar.")
