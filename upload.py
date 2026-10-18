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

# Artist Tag Database (808 Mafia Theme)
ARTIST_TAGS = {
    "808 mafia x drake": {
        "tags": [
            "#808MafiaTypeBeat", "#SouthsideTypeBeat", "#DrakeTypeBeat", "#TravisScottTypeBeat", 
            "#808Mafia", "#Southside", "#DarkTrap", "#MelodicTrap", "#FLStudio",
            "#SickoModeTypeBeat", "#HerLossTypeBeat", "#AstroworldTypeBeat", "#UtopiaTypeBeat",
            "#AmbientTrap", "#RnbTrap", "#DarkMelodicTrap", "#OVOTypeBeat", "#CactusJackTypeBeat",
            "#DrakeInstrumental", "#TravisScottInstrumental", "#HardTrapBeat",
            "#TrapBeat2026", "#TypeBeat2026", "#Beatmaker", "#Producer", "#HipHopInstrumental",
            "#DrakeTypeBeats", "#NightVibes", "#TM88TypeBeat"
        ],
        "genre": "808 Mafia Dark Melodic Trap"
    },
    "808 mafia x lil baby": {
        "tags": [
            "#808MafiaTypeBeat", "#LilBabyTypeBeat", "#GunnaTypeBeat", "#808Mafia", "#Southside", 
            "#HardTrap", "#WaveRunner", "#FLStudio", "#DripHarder", "#GuitarTrap", "#DripTooHard", 
            "#WheezyTypeBeat", "#TurboTypeBeat", "#AtlantaTrap", "#MelodicHardTrap", "#PianoTrap", 
            "#LilBabyInstrumental", "#GunnaInstrumental", "#HardInstrumental", "#RapBeat",
            "#TrapBeat2026", "#TypeBeat2026", "#4PFTypeBeat", "#YSLTypeBeat", "#FreeTypeBeat",
            "#DripTrap", "#Beatmaker", "#TM88"
        ],
        "genre": "808 Mafia Hard Trap"
    },
    "808 mafia x ken carson": {
        "tags": [
            "#808MafiaTypeBeat", "#KenCarsonTypeBeat", "#OsamasonTypeBeat", "#808Mafia", "#Southside",
            "#FreeHardLuckiTypeBeat", "#HardLuckiTypeBeat", "#ChiefKeefTypeBeat", "#LuckiTypeBeat", 
            "#VeezeTypeBeat", "#RichAmiriTypeBeat", "#FreeLuckiTypeBeat", "#LuckiBeat", 
            "#HardTypeBeat", "#UndergroundTypeBeat", "#MelodicTypeBeat", "#WaveTypeBeat", 
            "#LuckiTypebeet", "#Osamasonbeet", "#HardlukiTypeBeat", "#ChiefeefTypeBeat", "#RageBeat"
        ],
        "genre": "808 Mafia Rage / Opium Trap"
    },
    "808 mafia x playboi carti": {
        "tags": [
            "#808MafiaTypeBeat", "#PlayboiCartiTypeBeat", "#808Mafia", "#Southside", "#TypeBeat", 
            "#TrapBeat", "#RapInstrumental", "#UndergroundHipHop", "#MelodicRap", "#NewWave", 
            "#AtlantaRap", "#Vibes", "#Beatmaker", "#HipHopBeats", "#FreeTypeBeat", "#HardBeats", 
            "#YoungRapper", "#MusicProduction", "#PlayboiTyte", "#AWGE", "#Alanta", "#TM88"
        ],
        "genre": "808 Mafia Pluggnb / Minimalist Trap"
    },
    "808 mafia x future": {
        "tags": [
            "#808MafiaTypeBeat", "#FutureTypeBeat", "#SouthsideTypeBeat", "#808Mafia", "#Southside", 
            "#TM88", "#DarkTrap", "#HardTrap", "#FLStudio", "#FutureSouthsideTypeBeat", 
            "#808MafiaTypeBeat", "#AtlantaTrap", "#HardFutureTypeBeat", "#DarkTrapBeat", 
            "#TrapInstrumental", "#FutureInstrumental", "#SouthsideOnTheBeat", "#MetroBoominTypeBeat", 
            "#DirtySpriteTypeBeat", "#TypeBeat2026", "#FreeTypeBeat"
        ],
        "genre": "808 Mafia Dark Atlanta Trap"
    },
    "808 mafia x lil uzi vert": {
        "tags": [
            "#808MafiaTypeBeat", "#FutureTypeBeat", "#LilUziVertTypeBeat", "#808Mafia", "#Southside", 
            "#MelodicTrap", "#SpaceTrap", "#FLStudio", "#LilUziTypeBeat", "#FuturisticBeat", 
            "#SynthTrap", "#HyperpopTrap", "#MelodicRapBeat", "#UziTypeBeat", "#FutureInstrumental", 
            "#LilUziInstrumental", "#FreeTypeBeat", "#TrapBeat2026", "#SpaceyTrap"
        ],
        "genre": "808 Mafia Futuristic Melodic Trap"
    },
    "808 mafia x young thug": {
        "tags": [
            "#808MafiaTypeBeat", "#FutureTypeBeat", "#YoungThugTypeBeat", "#808Mafia", "#Southside", 
            "#SuperSlimey", "#MelodicTrap", "#AtlantaTrap", "#FLStudio", "#YoungThugInstrumental", 
            "#FutureInstrumental", "#YSLTypeBeat", "#FreeThuggerTypeBeat", "#FreeTypeBeat", 
            "#TrapInstrumental", "#SlimeTypeBeat", "#TypeBeat2026", "#AtlantaTypeBeat"
        ],
        "genre": "808 Mafia Melodic Trap"
    },
    "808 mafia x gunna": {
        "tags": [
            "#808MafiaTypeBeat", "#GunnaTypeBeat", "#YoungThugTypeBeat", "#808Mafia", "#Southside", 
            "#YSLTypeBeat", "#DripTrap", "#GuitarTrap", "#FLStudio", "#SlimeLanguage", 
            "#MelodicTrapBeat", "#WheezyTypeBeat", "#TurboTypeBeat", "#YSLBeat", 
            "#YoungThugInstrumental", "#GunnaInstrumental", "#FreeTypeBeat", "#GuitarMelodicTrap"
        ],
        "genre": "808 Mafia Drip / Melodic Trap"
    },
    "default": {
        "tags": [
            "#808MafiaTypeBeat", "#SouthsideTypeBeat", "#TypeBeat", "#Instrumental", "#BeatStash", 
            "#FLStudio", "#NewBeat", "#FreeTypeBeat", "#TrapBeat", "#RapBeat", "#Beatmaker", 
            "#Producer", "#MusicProducer", "#TypeBeats", "#HipHopBeats", "#InstrumentalBeat", 
            "#TypeBeat2026", "#FreeBeat", "#BuyBeats", "#BeatStore", "#808Mafia"
        ],
        "genre": "808 Mafia Instrumental"
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
    Parses: '808 mafia x drake type beat - Midnight.mp3'
    Returns: artist_combo ('808 mafia x drake'), beat_title ('Midnight')
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
    and individual artist fallbacks by mixing tags dynamically under the 808 Mafia theme.
    """
    # 1. Check for an exact match first
    if artist_combo in ARTIST_TAGS:
        config = ARTIST_TAGS[artist_combo]
    else:
        # 2. Check for reversed combination (e.g. 'drake x 808 mafia')
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
    
    # Collect images into lists grouped by base name (supports variant naming like v1, v2)
    image_files = {}
    for f in files:
        if f['name'].lower().endswith(('.jpg', '.jpeg', '.png')):
            key = os.path.splitext(f['name'])[0].lower()
            if key not in image_files:
                image_files[key] = []
            image_files[key].append(f)

    if not audio_files:
        print("No beats found in the Google Drive folder. Exiting.")
        return

    # Pick ONE random beat
    chosen_beat = random.choice(audio_files)
    print(f"Selected beat file: {chosen_beat['name']}")

    # Parse artist combination and title from filename
    artist_combo, beat_title = parse_filename(chosen_beat['name'])
    print(f"Detected Artist Combo: {artist_combo} | Beat Title: {beat_title}")

    # Match image by artist combo prefix (supports variants starting with the artist combo)
    matching_variants = [
        img for key, img_list in image_files.items() if key.startswith(artist_combo) for img in img_list
    ]

    if matching_variants:
        matched_image = random.choice(matching_variants)
        print(f"Matched variant cover art for '{artist_combo}' (Selected: {matched_image['name']})")
    elif image_files:
        # Fallback to any random image if no matching art starts with the artist combo
        all_images = [img for sublist in image_files.values() for img in sublist]
        matched_image = random.choice(all_images)
        print(f"Exact prefix match for '{artist_combo}' not found. Using fallback image: {matched_image['name']}")
    else:
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
