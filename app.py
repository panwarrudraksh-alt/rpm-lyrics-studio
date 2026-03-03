import streamlit as st
import lyricsgenius
import requests

st.set_page_config(page_title="RPM Lyrics Studio", page_icon="🎵", layout="centered")

st.title("🎵 RPM Lyrics Studio")

# -------------------------
# Load API Key Safely
# -------------------------
api_key = None

try:
    api_key = st.secrets["GENIUS_API_KEY"]
except KeyError:
    st.error("⚠ Genius API key not found in Streamlit Secrets.")
    st.stop()

# -------------------------
# Initialize Genius Safely
# -------------------------
try:
    genius = lyricsgenius.Genius(
        api_key,
        timeout=20,
        retries=3,
        sleep_time=1,
        remove_section_headers=True,
        skip_non_songs=True,
        excluded_terms=["(Remix)", "(Live)"]
    )
    genius.verbose = False
except Exception:
    st.error("⚠ Failed to initialize Genius API.")
    st.stop()

# -------------------------
# User Inputs
# -------------------------
song_name = st.text_input("Enter Song Name")
artist_name = st.text_input("Enter Artist Name (recommended)")

# -------------------------
# Fetch Lyrics
# -------------------------
if st.button("Get Lyrics"):

    if not song_name:
        st.warning("Please enter a song name.")
        st.stop()

    with st.spinner("Fetching lyrics..."):

        try:
            song = genius.search_song(song_name, artist_name)

            if song is None:
                st.warning("Song not found on Genius.")
            else:
                st.success("Lyrics fetched successfully!")
                st.text_area("Lyrics", song.lyrics, height=400)

        except requests.exceptions.HTTPError as http_err:
            if http_err.response.status_code == 401:
                st.error("❌ Invalid Genius API Key.")
            elif http_err.response.status_code == 429:
                st.error("⚠ API rate limit reached. Please try again later.")
            elif http_err.response.status_code == 403:
                st.error("❌ Access forbidden. Genius may be blocking cloud requests.")
            else:
                st.error("HTTP error occurred.")

        except requests.exceptions.Timeout:
            st.error("⏳ Request timed out. Please try again.")

        except Exception:
            st.error("""
Unable to fetch lyrics right now.

Possible reasons:
• API rate limit reached  
• Song not available on Genius  
• Temporary API issue  
• Genius blocking cloud server
""")
