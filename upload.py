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
        "tags": [
            "#DrakeTypeBeat", "#TravisScottTypeBeat", "#DarkTrap", "#MelodicTrap", "#FLStudio",
            "#SickoModeTypeBeat", "#HerLossTypeBeat", "#AstroworldTypeBeat", "#UtopiaTypeBeat",
            "#AmbientTrap", "#RnbTrap", "#DarkMelodicTrap", "#OVOTypeBeat", "#CactusJackTypeBeat",
            "#DrakeInstrumental", "#TravisScottInstrumental", "#DrakexTravisScott", "#HardTrapBeat",
            "#TrapBeat2026", "#TypeBeat2026", "#Beatmaker", "#Producer", "#HipHopInstrumental",
            "#DrakeTypeBeats", "#TravisScottTypeBeats", "#NightVibes"
        ],
        "genre": "Dark Melodic Trap"
    },
    "lil baby x gunna": {
        "tags": [
            "#LilBabyTypeBeat", "#GunnaTypeBeat", "#HardTrap", "#WaveRunner", "#FLStudio",
            "#DripHarder", "#GuitarTrap", "#DripTooHard", "#WheezyTypeBeat", "#TurboTypeBeat",
            "#AtlantaTrap", "#MelodicHardTrap", "#PianoTrap", "#LilBabyInstrumental", "#GunnaInstrumental",
            "#LilBabyxGunna", "#LilBabyxGunnaTypeBeat", "#HardInstrumental", "#RapBeat",
            "#TrapBeat2026", "#TypeBeat2026", "#4PFTypeBeat", "#YSLTypeBeat", "#FreeTypeBeat",
            "#DripTrap", "#Beatmaker"
        ],
        "genre": "Hard Trap"
    },
    "ken carson x osamason": {
        "tags": [
            "#KenCarsonTypeBeat", "#OsamasonTypeBeat", "#FreeHardLuckiTypeBeat", "#HardLuckiTypeBeat",
            "#ChiefKeefTypeBeat", "#LuckiTypeBeat", "#VeezeTypeBeat", "#RichAmiriTypeBeat",
            "#FreeLuckiTypeBeat", "#LuckiBeat", "#KenCarsonXOsamason", "#HardTypeBeat",
            "#UndergroundTypeBeat", "#MelodicTypeBeat", "#WaveTypeBeat", "#LuckiTypebeet",
            "#Osamasonbeet", "#HardlukiTypeBeat", "#ChiefeefTypeBeat"
        ],
        "genre": "Rage / Opium Trap"
    },
    "playboi carti x unotheactivist": {
        "tags": [
            "#PlayboiCarti", "#UnoTheActivist", "#TypeBeat", "#TrapBeat", "#RapInstrumental",
            "#UndergroundHipHop", "#MelodicRap", "#NewWave", "#AtlantaRap", "#Vibes",
            "#Beatmaker", "#HipHopBeats", "#FreeTypeBeat", "#HardBeats", "#YoungRapper",
            "#MusicProduction", "#PlayboiTyte", "#Unoartivist", "#Unotheactivistt",
            "#PlayboiCartii", "#AWGE", "#Alanta"
        ],
        "genre": "Pluggnb / Minimalist Trap"
    },
    "future x southside": {
        "tags": [
            "#FutureTypeBeat", "#SouthsideTypeBeat", "#808Mafia", "#DarkTrap", "#HardTrap", "#FLStudio",
            "#FutureSouthsideTypeBeat", "#808MafiaTypeBeat", "#AtlantaTrap", "#HardFutureTypeBeat",
            "#DarkTrapBeat", "#TrapInstrumental", "#FutureInstrumental", "#SouthsideOnTheBeat",
            "#MetroBoominTypeBeat", "#DirtySpriteTypeBeat", "#TypeBeat2026", "#FreeTypeBeat"
        ],
        "genre": "Dark Atlanta Trap"
    },
    "future x lil uzi vert": {
        "tags": [
            "#FutureTypeBeat", "#LilUziVertTypeBeat", "#PlutoxBabyPluto", "#MelodicTrap", "#SpaceTrap", "#FLStudio",
            "#LilUziTypeBeat", "#FuturexLilUzi", "#FuturisticBeat", "#SynthTrap", "#HyperpopTrap",
            "#MelodicRapBeat", "#UziTypeBeat", "#FutureInstrumental", "#LilUziInstrumental",
            "#FreeTypeBeat", "#TrapBeat2026", "#SpaceyTrap"
        ],
        "genre": "Futuristic Melodic Trap"
    },
    "future x young thug": {
        "tags": [
            "#FutureTypeBeat", "#YoungThugTypeBeat", "#SuperSlimey", "#MelodicTrap", "#AtlantaTrap", "#FLStudio",
            "#FuturexYoungThug", "#YoungThugInstrumental", "#FutureInstrumental", "#YSLTypeBeat",
            "#FreeThuggerTypeBeat", "#FreeTypeBeat", "#TrapInstrumental", "#SlimeTypeBeat",
            "#TypeBeat2026", "#AtlantaTypeBeat"
        ],
        "genre": "Melodic Trap"
    },
    "gunna x young thug": {
        "tags": [
            "#GunnaTypeBeat", "#YoungThugTypeBeat", "#YSLTypeBeat", "#DripTrap", "#GuitarTrap", "#FLStudio",
            "#GunnaxYoungThug", "#SlimeLanguage", "#MelodicTrapBeat", "#WheezyTypeBeat",
            "#TurboTypeBeat", "#YSLBeat", "#YoungThugInstrumental", "#GunnaInstrumental",
            "#FreeTypeBeat", "#GuitarMelodicTrap", "#TypeBeat2026"
        ],
        "genre": "Drip / Melodic Trap"
    },
    "default": {
        "tags": [
            "#TypeBeat", "#Instrumental", "#BeatStash", "#FLStudio", "#NewBeat",
            "#FreeTypeBeat", "#TrapBeat", "#RapBeat", "#Beatmaker", "#Producer",
            "#MusicProducer", "#TypeBeats", "#HipHopBeats", "#InstrumentalBeat",
            "#TypeBeat2026", "#FreeBeat", "#BuyBeats", "#BeatStore"
        ],
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
        parts = re.split(r' type beat - ', name_without_ext, flags=re.IGNORECASE)
        artist_combo = parts[0].strip().lower()
        beat_title = parts[1].strip()
    else:
        artist_combo = "default"
        beat_title = name_without_ext.strip()
        
    return artist_combo, beat_title

def generate_metadata(artist_combo, beat_title):
    """
    Intelligently generates metadata, handling exact matches, reversed artist combinations,
    and individual artist fallbacks by mixing tags dynamically.
    """
    # 1. Check for an exact match first
    if artist_combo in ARTIST_TAGS:
        config = ARTIST_TAGS[artist_combo]
    else:
        # 2. Check for reversed combination (e.g. 'travis scott x future')
        artists = [a.strip() for a in artist_combo.split('x')]
        reversed_combo = " x ".join(reversed(artists))
        
        if reversed_combo in ARTIST_TAGS:
            config = ARTIST_TAGS[reversed_combo]
            print(f"Matched reversed artist combo: '{reversed_combo}'")
        else:
            # 3. Dynamic Individual Fallback: Collect tags for each artist found in our database
            collected_tags = set(ARTIST_TAGS["default"]["tags"])
            matched_genres = []
            
            for artist in artists:
                found_match = False
                for key, data in ARTIST_TAGS.items():
                    if artist in key and key != "default":
                        collected_tags.update(data["tags"])
                        matched_genres.append(data["genre"])
                        found_match = True
                
                # If individual artist isn't explicitly in keys, generate a clean tag dynamically
                if not found_match and len(artist) > 1:
                    formatted_tag = f"#{artist.title().replace(' ', '')}TypeBeat"
                    collected_tags.add(formatted_tag)

            genre = " / ".join(list(set(matched_genres))) if matched_genres else ARTIST_TAGS["default"]["genre"]
            config = {
                "tags": list(collected_tags),
                "genre": genre
            }
            print(f"Dynamic fallback tags generated for custom combination: '{artist_combo}'")

    title = f"{artist_combo.title()} Type Beat - \"{beat_title}\" | the random stash free beat"
    
    description = (
        f"🎧 Stream & download '{beat_title}' ({config['genre']}).\n\n"
        f"Produced by $oulesssK.\n"
        f"📩 For leasing or custom beats: dm @soulesssk on IG or @1soulesssk on tiktok.\n\n"
        f"{' '.join(config['tags'])}"
    )
    
    return title, description, config['tags']

def render_video(audio_path, image_path, output_video_path="final_output.mp4"):
    print("Rendering video with FFmpeg...")
    cmd = [
        'ffmpeg', '-y',
        '-loop', '1',
        '-i', image_path,
        '-i', audio_path,
        '-vf', 'scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2',
        '-c:v', 'libx264',
        '-tune', 'stillimage',
        '-c:a', 'aac',
        '-b:a', '192k',
        '-pix_fmt', 'yuv420p',
        '-shortest',
        output_video_path
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

    # Generate title, description, and tags dynamically
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
