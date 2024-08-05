import streamlit as st
import pandas as pd
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

# CSV dosyasının sütun isimlerini yazdır
st.write("CSV dosyasının sütun isimleri:")
st.write(data.columns.tolist())

# Function to get the unique questions
def get_unique_questions(data):
    return data['Question'].unique()

# Function to get the options for a specific question
def get_options_for_question(data, question):
    return data[data['Question'] == question]['Options'].unique()

# Function to get the carbon footprint value for a specific question and option
def get_carbon_footprint_value(data, question, option):
    return data[(data['Question'] == question) & (data['Options'] == option)]['Carbon_Footprint_Value'].values[0]

# Initialize total carbon footprint
total_carbon_footprint = 0

# Get unique questions
questions = get_unique_questions(data)

# User inputs for each question
responses = {}

for question in questions:
    options = get_options_for_question(data, question)
    response = st.selectbox(question, options)
    responses[question] = response

# Add a "Hesapla" button
if st.button('Karbon Ayak İzini Hesapla'):
    # Calculate total carbon footprint
    for question, option in responses.items():
        total_carbon_footprint += get_carbon_footprint_value(data, question, option)
    
    # Display total carbon footprint
    st.write(f"Toplam Karbon Ayak İzi: {total_carbon_footprint} birim")

# Optional: Provide additional information or tips
st.write("Karbon ayak izinizi azaltmak için bazı ipuçları: ...")
