# OAuth 2.0 Spotify Metadata Extractor 

An automated REST API integration built in Python to securely authenticate with Spotify, manage bearer tokens, and extract playlist metadata into structured CSV formats. 

**Disclaimer:** *This project was developed strictly as an educational proof-of-concept for understanding OAuth 2.0 Authorization Code flows, RFC 8252 compliance (loopback interface security), and defensive JSON parsing. It complies fully with Spotify's Developer Terms of Service.*

## 🛠️ Tech Stack
* **Python 3.x**
* **Spotipy** (OAuth 2.0 handling & API requests)
* **Dotenv** (Environment variable management)
* **Pandas / CSV** (Data structuring and export)

## ⚙️ Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/](https://github.com/)hellsguardianyt-cell/OAuth-2.0-Spotify-Metadata-Extractor.git
   cd Auth-2.0-Spotify-Metadata-Extractor.git
Set up the virtual environment:

DOS
python -m venv venv
venv\Scripts\activate
Install dependencies:

DOS
pip install -r requirements.txt
Configure Environment Variables:
Create a .env file in the root directory and add your Spotify Developer credentials:

Code snippet
SPOTIPY_CLIENT_ID='your_client_id_here'
SPOTIPY_CLIENT_SECRET='your_client_secret_here'
SPOTIPY_REDIRECT_URI='[http://127.0.0.1:8888/callback](http://127.0.0.1:8888/callback)'
Run the Extractor:

DOS
python main.py
Note: On the first run, your browser will open to request Spotify authorization. A local .cache file will be securely generated to manage token refreshes.
