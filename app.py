import streamlit as st
import lyricsgenius
import os

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="RPM Lyrics Studio", layout="wide")

# ---------------- SAFE GENIUS SETUP ----------------
api_key = st.secrets.get("GENIUS_API_KEY") or os.getenv("GENIUS_API_KEY")

if not api_key:
    st.error("⚠ Genius API Key not found. Please configure it in Streamlit Cloud Secrets.")
    st.stop()

genius = lyricsgenius.Genius(api_key)
genius.skip_non_songs = True
genius.excluded_terms = ["(Remix)", "(Live)"]
genius.remove_section_headers = True

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>

body {
    background: linear-gradient(to bottom right, #000000, #2a003f);
    color: white;
    font-family: 'Georgia', serif;
    scroll-behavior: smooth;
}

.title {
    font-size: 70px;
    font-weight: 900;
    text-align: center;
    letter-spacing: 4px;
    background: linear-gradient(90deg, #ff00cc, #ffae00);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.stButton>button {
    background-color: #ffae00;
    color: black;
    border-radius: 30px;
    padding: 10px 25px;
    font-weight: bold;
    transition: 0.3s ease-in-out;
}

.stButton>button:hover {
    background-color: #ff00cc;
    color: white;
    transform: scale(1.05);
    box-shadow: 0px 0px 15px #ff00cc;
}

.lyrics-box {
    height: 500px;
    overflow-y: auto;
    padding: 20px;
    border-radius: 20px;
    background: rgba(255,255,255,0.05);
    backdrop-filter: blur(10px);
    animation: fadeIn 1.5s ease-in-out;
}

@keyframes fadeIn {
    from {opacity: 0;}
    to {opacity: 1;}
}

.equalizer {
  display: flex;
  justify-content: center;
  margin-top: 20px;
}

.bar {
  width: 5px;
  height: 30px;
  margin: 3px;
  background: #ff00cc;
  animation: bounce 1s infinite ease-in-out;
}

.bar:nth-child(2) { animation-delay: 0.2s; }
.bar:nth-child(3) { animation-delay: 0.4s; }
.bar:nth-child(4) { animation-delay: 0.6s; }
.bar:nth-child(5) { animation-delay: 0.8s; }

@keyframes bounce {
  0%, 100% { height: 20px; }
  50% { height: 60px; }
}

</style>
""", unsafe_allow_html=True)

# ---------------- TITLE ----------------
st.markdown("<div class='title'>🎵 RPM Lyrics Studio</div>", unsafe_allow_html=True)
st.markdown("### Experience lyrics in motion ✨")

# ---------------- THEME SELECTOR ----------------
theme = st.selectbox("🎨 Choose Mood Theme",
                     ["Neon Club (Pop)", "Retro Jazz", "Rock Fire"])

if theme == "Retro Jazz":
    st.markdown("""
    <style>
    body { background: linear-gradient(to bottom right, #000000, #3b0066); }
    .bar { background: gold; }
    </style>
    """, unsafe_allow_html=True)

elif theme == "Rock Fire":
    st.markdown("""
    <style>
    body { background: linear-gradient(to bottom right, #000000, #4b0000); }
    .bar { background: orange; }
    </style>
    """, unsafe_allow_html=True)

# ---------------- SEARCH SECTION ----------------
song_title = st.text_input("🎶 Enter Song Name")
artist_name = st.text_input("🎤 Enter Artist Name")

if st.button("✨ Fetch Lyrics"):

    if not song_title.strip():
        st.warning("⚠ Please enter a song name.")
        st.stop()

    try:
        with st.spinner("Searching the Genius universe..."):
            song = genius.search_song(song_title.strip(), artist_name.strip())

        if song and song.lyrics:
            st.success("Lyrics Found! 🎉")

            lyrics_lines = song.lyrics.split("\n")

            lyrics_html = "<div class='lyrics-box'>"
            for line in lyrics_lines:
                lyrics_html += f"<p>{line}</p>"
            lyrics_html += "</div>"

            st.markdown(lyrics_html, unsafe_allow_html=True)

            st.markdown("""
            <div class="equalizer">
                <div class="bar"></div>
                <div class="bar"></div>
                <div class="bar"></div>
                <div class="bar"></div>
                <div class="bar"></div>
            </div>
            """, unsafe_allow_html=True)

        else:
            st.error("❌ Song not found. Try different keywords.")

    except Exception:
        st.error("⚠ Unable to fetch lyrics right now.")
        st.info("Possible reasons:")
        st.write("- API rate limit reached")
        st.write("- Song not available on Genius")
        st.write("- Temporary API issue")

# ---------------- FOOTER ----------------
st.markdown("---")
st.markdown("Built by Rudraksh,Priyanshu and Mridul")
