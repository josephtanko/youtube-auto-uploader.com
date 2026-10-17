import os
import random
import re
import subprocess
import io
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload

# Environment Variables
DRIVE_FOLDER_ID = os.environ.get("DRIVE_FOLDER_ID")
CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID")
CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET")
REFRESH_TOKEN = os.environ.get("GOOGLE_REFRESH_TOKEN")

# Artist Tag Database
ARTIST_TAGS = {
    "drake x travis scott": {
        "tags": ["#DrakeTypeBeat", "#TravisScottTypeBeat", "#DarkTrap", "#MelodicTrap", "#FLStudio"],
        "genre": "Dark Melodic Trap"
    },
    "lil baby x gunna": {
        "tags": ["#LilBabyTypeBeat", "#GunnaTypeBeat", "#HardTrap", "#WaveRunner", "#FLStudio"],
        "genre": "Hard Trap"
    },
    "default": {
        "tags": ["#TypeBeat", "#Instrumental", "#BeatStash", "#FLStudio", "#NewBeat"],
        "genre": "Instrumental"
    }
}

def get_google_credentials():
    return Credentials(
        token=None,
        refresh_token=REFRESH_TOKEN,
        token_uri="https://oauth2.googleapis.com/token",
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET
    )

def list_drive_files(service):
    query = f"'{DRIVE_FOLDER_ID}' in parents and trashed = false"
    results = service.files().list(q=query, fields="files(id, name, mimeType)").execute()
    return results.get('files', [])

def download_file(service, file_id, destination_path):
    request = service.files().get_media(fileId=file_id)
    fh = io.FileIO(destination_path, 'wb')
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while not done:
        status, done = downloader.next_chunk()
    print(f"Downloaded: {destination_path}")

def delete_drive_file(service, file_id):
    service.files().delete(fileId=file_id).execute()
    print(f"Deleted file ID {file_id} from Google Drive.")

def parse_filename(filename):
    """
    Parses: 'Drake x Travis Scott type beat - Midnight.mp3'
    Returns: artist_combo ('drake x travis scott'), beat_title ('Midnight')
    """
    name_without_ext = os.path.splitext(filename)[0]
    
    if " type beat - " in name_without_ext.lower():
        # Split by ' type beat - ' case-insensitively
        parts = re.split(r' type beat - ', name_without_ext, flags=re.IGNORECASE)
        artist_combo = parts[0].strip().lower()
        beat_title = parts[1].strip()
    else:
        # Fallback if naming convention varies slightly
        artist_combo = "default"
        beat_title = name_without_ext.strip()
        
    return artist_combo, beat_title

def generate_metadata(artist_combo, beat_title):
    # Match artist tags or fall back to default
    config = ARTIST_TAGS.get(artist_combo, ARTIST_TAGS["default"])
    
    title = f"{artist_combo.title()} Type Beat - \"{beat_title}\" | Free Instrumental"
    
    description = (
        f"🎧 Stream & download '{beat_title}' ({config['genre']}).\n\n"
        f"Produced by $oulesssK.\n"
        f"📩 For leasing or custom beats: Check channel info.\n\n"
        f"{' '.join(config['tags'])}"
    )
    
    return title, description, config['tags']

def render_video(audio_path, image_path, output_path="output.mp4"):
    print("Rendering video with FFmpeg...")
    cmd = [
        "ffmpeg", "-loop", "1", "-i", image_path, "-i", audio_path,
        "-c:v", "libx264", "-tune", "stillimage", "-c:a", "aac", "-b:a", "192k",
        "-shortest", "-pix_fmt", "yuv420p", output_path, "-y"
    ]
    subprocess.run(cmd, check=True)
    print("Video rendered successfully.")

def upload_to_youtube(youtube_service, video_path, title, description, tags):
    print(f"Uploading '{title}' to YouTube...")
    body = {
        "snippet": {
            "title": title,
            "description": description,
            "tags": tags,
            "categoryId": "10"  # Music category
        },
        "status": {
            "privacyStatus": "public"  # Change to "unlisted" or "private" if testing first
        }
    }
    media = MediaFileUpload(video_path, chunksize=-1, resumable=True, mimetype="video/mp4")
    request = youtube_service.videos().insert(part="snippet,status", body=body, media_body=media)
    response = request.execute()
    print(f"Upload complete! Video ID: {response.get('id')}")

def main():
    creds = get_google_credentials()
    drive_service = build('drive', 'v3', credentials=creds)
    youtube_service = build('youtube', 'v3', credentials=creds)

    files = list_drive_files(drive_service)
    
    audio_files = [f for f in files if f['name'].lower().endswith(('.mp3', '.wav', '.m4a'))]
    image_files = {os.path.splitext(f['name'])[0].lower(): f for f in files if f['name'].lower().endswith(('.jpg', '.jpeg', '.png'))}

    if not audio_files:
        print("No beats found in the Google Drive folder. Exiting.")
        return

    # Pick ONE random beat
    chosen_beat = random.choice(audio_files)
    print(f"Selected beat file: {chosen_beat['name']}")

    # Parse artist combination and title from filename
    artist_combo, beat_title = parse_filename(chosen_beat['name'])
    print(f"Detected Artist Combo: {artist_combo} | Beat Title: {beat_title}")

    # Match image by artist combo name (e.g., 'drake x travis scott.jpg')
    matched_image = image_files.get(artist_combo)
    if not matched_image and image_files:
        # Fallback to any random image if exact artist art isn't found
        matched_image = random.choice(list(image_files.values()))
        print(f"Exact cover art match for '{artist_combo}' not found. Using fallback image: {matched_image['name']}")
    elif not image_files:
        print("Error: No images found in Google Drive folder.")
        return

    # Download files locally
    audio_local = "input_audio.mp3"
    image_local = "input_image.jpg"
    download_file(drive_service, chosen_beat['id'], audio_local)
    download_file(drive_service, matched_image['id'], image_local)

    # Generate title, description, and tags
    title, description, tags = generate_metadata(artist_combo, beat_title)

    # Render video & upload
    output_video = "final_output.mp4"
    render_video(audio_local, image_local, output_video)
    upload_to_youtube(youtube_service, output_video, title, description, tags)

    # Clean up posted beat from Drive
    delete_drive_file(drive_service, chosen_beat['id'])
    print("Workflow finished successfully!")

if __name__ == "__main__":
    main()
