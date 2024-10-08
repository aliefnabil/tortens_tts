import streamlit as st
import requests

# Inject custom CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Serif:ital,wght@0,100;0,200;0,300;0,400;0,500;0,600;0,700;1,100;1,200;1,300;1,400;1,500;1,600;1,700&display=swap" rel="stylesheet');
    
    /* Change background color */
    body {
        background-color: #FDEACD;
    }
      
    /* Change font for st.title */
    h1 {
        font-family: "IBM Plex Serif", serif;
        font-weight: 600;
        font-style: normal;
        color: #FF3131;
    }
    
    /* Change font for st.write and st.text */
    p, div {
        font-family: "IBM Plex Serif", serif;
        font-weight: 400;
        font-style: normal;
    }
            
    </style>
    """, unsafe_allow_html=True)

# Eleven Labs API key and voice settings
API_KEY = "sk_eaf66e4fff574b730fca863f5cb9ac7d072d3b092a385450"
VOICE_ID = "XB0fDUnXU5powFXDhCwa"  # Replace with your specific voice ID

# Initialize session state to track whether the name has been entered
if 'name_entered' not in st.session_state:
    st.session_state['name_entered'] = False

# Streamlit App
st.title("Surat Dari Ibu")

if not st.session_state['name_entered']:
    user_name = st.text_input("Masukkan Nama Anda:")

    # When the user enters their name, lock the input
    if user_name:
        st.session_state['name_entered'] = True
        st.session_state['user_name'] = user_name

        letter_text = f"Dear {user_name},\n\nNak, ibu rindu. Ibu kirim Tiramisu favoritmu, semoga mengingatkanmu pada rumah. Kejar mimpimu, meski sulit, ibu selalu mendukungmu dari jauh. Jaga diri, kita akan bertemu lagi.\n\nPeluk hangat, Ibu"
        
        st.write(letter_text)

        #Eleven Labs API request
        headers = {
            "xi-api-key": API_KEY,
            "Content-Type": "application/json"
        }

        data = {
            "text": letter_text,
            "voice_settings": {
                "stability": 0.5,
                "similarity_boost": 0.75
            }
        }

        # Stream the audio while generating
        response = requests.post(
            f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}",
            headers=headers,
            json=data,
            stream=True  # Enable streaming
        )

        if response.status_code == 200:
            # Create audio file from stream chunks
            with open("output.mp3", "wb") as audio_file:
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        audio_file.write(chunk)

            # Play audio in Streamlit
            st.audio("output.mp3", format="audio/mp3")

            # Optionally provide a download link
            with open("output.mp3", "rb") as audio_file:
                st.download_button(label="Unduh Pesan Ibu", data=audio_file, file_name="letter.mp3")
            
            url = "https://www.instagram.com/tortens.s/"
            st.write("Bantu sebarkan Pesan Ibu melalui Instagram dan tag kami [@tortens.s](%s)" % url)
    
        else:
            st.error("Gagal mengeluarkan suara. Tolong coba lagi.")

else:
    # If the user tries to input the name again, show a pop-up message
    st.warning("Kamu hanya bisa memasukkan nama satu kali ya.")