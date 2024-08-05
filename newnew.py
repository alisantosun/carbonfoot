import streamlit as st
import pandas as pd

# GitHub'dan CSV dosyasını okumak için URL belirtin
csv_file_path = 'https://raw.githubusercontent.com/alisantosun/carbonfoot/main/karbon_ayak_izi_duzenlenmis.csv'

def load_csv(csv_url):
    try:
        # Veriyi oku
        df = pd.read_csv(csv_url, error_bad_lines=False, warn_bad_lines=True)
        return df
    except Exception as e:
        st.error(f"CSV dosyasını yüklerken bir hata oluştu: {e}")
        return None

# CSV dosyasını yükle
df = load_csv(csv_file_path)
if df is not None:
    st.write(df)



# 1. CSV Dosyasını Yükleme
def load_csv(csv_file_path):
    try:
        df = pd.read_csv(csv_file_path)
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
toplu_tasima_haftalik = st.slider("Haftalık Toplu Taşıma Süresi (saat)", 0, 20, 1)
arac_km_yillik = st.number_input("Yıllık Araç Kullanım Mesafesi (km)", min_value=0)
enerji_tipi = st.selectbox("Evde Kullanılan Enerji Tipi", options=['Elektrik', 'Doğalgaz', 'Kömür'])

# 3. Karbon Ayak İzi Hesaplama
def calculate_carbon_footprint(arac_km, enerji):
    # Burada basit bir hesaplama örneği yapalım
    arac_emisyon = arac_km * 0.2  # Her km başına ortalama 0.2 kg CO2 emisyonu
    enerji_emisyon = data[data['Arac_yakit_tipi'] == enerji]['Emisyon_Toplam'].mean()  # Enerji tipine göre ortalama emisyon
    total_emisyon = toplu_tasima_emisyon + arac_emisyon + enerji_emisyon
    return total_emisyon

# Kullanıcıdan gelen verilere göre hesaplama yapalım
carbon_footprint = calculate_carbon_footprint(arac_km_yillik, enerji_tipi)
st.write(f"Toplam Karbon Ayak İzi: {carbon_footprint:.2f} kg CO2")

# Karbon ayak izi eşik değerleri ve öneriler
if carbon_footprint > 5000:
    st.warning("Karbon ayak iziniz yüksek. Karbon ayak izinizi azaltmak için toplu taşıma kullanmayı ve enerji verimliliği sağlamayı düşünebilirsiniz.")
elif carbon_footprint > 2000:
    st.info("Karbon ayak iziniz orta seviyede. Enerji tasarrufu için evinizde enerji verimli cihazlar kullanmayı ve araç kullanımını azaltmayı düşünebilirsiniz.")
else:
    st.success("Karbon ayak iziniz düşük. Bu şekilde devam edin ve çevreyi koruyun!")

