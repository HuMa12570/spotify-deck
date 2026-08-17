import time
import urllib.request
import os
import subprocess
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# ================= 사용자 설정 =================
CLIENT_ID = 'YOUR_SPOTIFY_CLIENT_ID'
CLIENT_SECRET = 'YOUR_SPOTIFY_CLIENT_SECRET'
REDIRECT_URI = 'http://127.0.0.1:8888/callback'
# ===============================================

def git_push():
    """favicon.png 변경사항을 깃허브로 푸시"""
    try:
        subprocess.run(["git", "add", "favicon.png"], check=True)
        subprocess.run(["git", "commit", "-m", "Update album art"], check=True)
        subprocess.run(["git", "push"], check=True)
        print(">> 깃허브 푸시 완료!")
    except Exception as e:
        print(f"Git Push 에러: {e}")

scope = "user-read-currently-playing user-read-playback-state"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=CLIENT_ID, client_secret=CLIENT_SECRET, redirect_uri=REDIRECT_URI, scope=scope
))

current_track_id = None
print("스포티파이 -> 깃허브 동기화 가동 중...")

while True:
    try:
        playback = sp.current_playback()
        if playback and playback.get('is_playing'):
            item = playback.get('item')
            if item and item['id'] != current_track_id:
                current_track_id = item['id']
                image_url = item['album']['images'][0]['url']
                
                # 1) favicon.png 파일로 저장
                urllib.request.urlretrieve(image_url, "favicon.png")
                print(f"곡 변경 감지: {item['name']} - {item['artists'][0]['name']}")
                
                # 2) 깃허브 자동 푸시
                git_push()
    except Exception as e:
        print(f"Error: {e}")

    time.sleep(3)