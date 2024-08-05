import streamlit as st
import pandas as pd
import numpy as np
import base64

# Base64 formatında arka plan resmi
def get_base64(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode('utf-8')

background_image = get_base64("background_min.jpg")

# Arka plan resmini ayarlamak için CSS
st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url(data:image/jpeg;base64,{background_image});
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# GitHub'dan CSV dosyasını okumak için URL belirtin
csv_file_path = 'https://raw.githubusercontent.com/alisantosun/carbonfoot/main/karbon_ayak_izi_duzenlenmis.csv'

def load_csv(csv_url):
    try:
        df = pd.read_csv(csv_url)
        if df.empty:
            st.error("CSV dosyası boş. Lütfen doğru bir dosya yükleyin.")
            st.stop()
        return df
    except FileNotFoundError:
        st.error("CSV dosyası bulunamadı. Lütfen dosya yolunu kontrol edin.")
        st.stop()
    except pd.errors.EmptyDataError:
        st.error("CSV dosyası boş. Lütfen doğru bir dosya yükleyin.")
        st.stop()
    except Exception as e:
        st.error(f"CSV dosyasını yüklerken bir hata oluştu: {e}")
        st.stop()

# CSV dosyasını yükle
data = load_csv(csv_file_path)

# 2. Kullanıcı Arayüzü
st.title("Karbon Ayak İzi Hesaplayıcı")

# Kullanıcıdan veri girişi alalım
toplu_tasima_haftalik = tab1.slider("Haftalık Toplu Taşıma Süresi (saat)", 0, 20, 1)
arac_km_yillik = tab2.number_input("Yıllık Araç Kullanım Mesafesi (km)", min_value=0)
enerji_tipi = tab3.selectbox("Evde Kullanılan Enerji Tipi", options=['Elektrik', 'Doğalgaz', 'Kömür'])

# 3. Karbon Ayak İzi Hesaplama
def calculate_carbon_footprint(toplu_tasima_haftalik, arac_km_yillik, enerji_tipi):
    try:
        # Basit bir hesaplama örneği yapalım
        toplu_tasima_emisyon = toplu_tasima_haftalik * data['Emisyon_toplu_tasima'].mean()  # Ortalama emisyon değeri ile çarpalım
        arac_emisyon = arac_km_yillik * 0.2  # Her km başına ortalama 0.2 kg CO2 emisyonu
        
        # Enerji tipine göre emisyon hesaplama
        if enerji_tipi in data['Arac_yakit_tipi'].values:
            enerji_emisyon = data[data['Arac_yakit_tipi'] == enerji_tipi]['Emisyon_Toplam'].mean()  # Enerji tipine göre ortalama emisyon
        else:
            st.error("Enerji tipi veri çerçevesinde bulunamadı.")
            return None
        
        total_emisyon = toplu_tasima_emisyon + arac_emisyon + enerji_emisyon
        return total_emisyon
    except KeyError as e:
        st.error(f"Veri çerçevesinde beklenmeyen bir sütun adı: {e}")
        return None
    except Exception as e:
        st.error(f"Karbon ayak izi hesaplanırken bir hata oluştu: {e}")
        return None

# Kullanıcıdan gelen verilere göre hesaplama yapalım
carbon_footprint = calculate_carbon_footprint(toplu_tasima_haftalik, arac_km_yillik, enerji_tipi)
if carbon_footprint is not None:
    st.write(f"Toplam Karbon Ayak İzi: {carbon_footprint:.2f} kg CO2")

    # Karbon ayak izi eşik değerleri ve öneriler
    if carbon_footprint > 5000:
        st.warning("Karbon ayak iziniz yüksek. Karbon ayak izinizi azaltmak için toplu taşıma kullanmayı ve enerji verimliliği sağlamayı düşünebilirsiniz.")
    elif carbon_footprint > 2000:
        st.info("Karbon ayak iziniz orta seviyede. Enerji tasarrufu için evinizde enerji verimli cihazlar kullanmayı ve araç kullanımını azaltmayı düşünebilirsiniz.")
    else:
        st.success("Karbon ayak iziniz düşük. Bu şekilde devam edin ve çevreyi koruyun!")
