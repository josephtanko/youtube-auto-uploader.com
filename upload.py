import os
import random
import re
import subprocess
import io
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from google import genai
from google.genai import types

# Environment Variables
DRIVE_FOLDER_ID = os.environ.get("DRIVE_FOLDER_ID")
CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID")
CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET")
REFRESH_TOKEN = os.environ.get("GOOGLE_REFRESH_TOKEN")
# GEMINI_API_KEY -> genai.Client()

ARTIST_TAGS = {
    "808 mafia x moneybagg yo": {
        "tags": [
            "#808MafiaTypeBeat", "#MoneybaggYoTypeBeat", "#SouthsideTypeBeat", "#808Mafia", "#Southside",
            "#MemphisTrap", "#ESTGeeTypeBeat", "#KeyGlockTypeBeat", "#PoohShiestyTypeBeat", "#HardTrap",
            "#HeavyTrap", "#StreetTrap", "#42DuggTypeBeat", "#YoGottiTypeBeat", "#MoneybaggYoInstrumental",
            "#HardInstrumental", "#FLStudio", "#TrapBeat2026", "#TypeBeat2026", "#Beatmaker",
            "#RapBeat", "#DarkTrapBeat", "#TM88TypeBeat", "#FreeTypeBeat", "#HardRapBeat"
        ],
        "genre": "808 Mafia Memphis Street Trap"
    },
    "808 mafia x osamason": {
        "tags": [
            "#808MafiaTypeBeat", "#OsamasonTypeBeat", "#KenCarsonTypeBeat", "#808Mafia", "#Southside",
            "#RageBeat", "#UndergroundTypeBeat", "#FlexMusic", "#OpiumTypeBeat", "#HardRageBeat",
            "#CheTypeBeat", "#NettspendTypeBeat", "#RichAmiriTypeBeat", "#OsamasonInstrumental",
            "#FLStudio", "#SynthTrap", "#DarkRage", "#HyperpopTrap", "#TypeBeat2026",
            "#TrapBeat2026", "#FreeTypeBeat", "#Beatmaker", "#OsamasonBeats"
        ],
        "genre": "808 Mafia Underground Rage Trap"
    },
    "808 mafia x lil durk": {
        "tags": [
            "#808MafiaTypeBeat", "#LilDurkTypeBeat", "#SouthsideTypeBeat", "#808Mafia", "#Southside",
            "#OTFTypeBeat", "#KingVonTypeBeat", "#ChicagoDrill", "#DarkAtlantaTrap", "#ChiraqTypeBeat",
            "#FutureTypeBeat", "#ATLJacobTypeBeat", "#LilDurkInstrumental", "#OTFBeats", "#HardDrillBeat",
            "#HardTrap", "#MelodicDrill", "#TrapBeat2026", "#TypeBeat2026", "#FLStudio",
            "#Beatmaker", "#Producer", "#FreeTypeBeat", "#RapInstrumental"
        ],
        "genre": "808 Mafia OTF Chicago Trap / Drill"
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
    name_without_ext = os.path.splitext(filename)[0]
    
    if " type beat - " in name_without_ext.lower():
        parts = re.split(r' type beat - ', name_without_ext, flags=re.IGNORECASE)
        artist_combo = parts[0].strip().lower()
        beat_title = parts[1].strip()
    else:
        artist_combo = "default"
        beat_title = name_without_ext.strip()
        
    return artist_combo, beat_title

def get_optimized_title(raw_context: str) -> str:
    client = genai.Client()
    
    system_instruction = (
        "You are VidIQ - an expert YouTube SEO engine. Generate optimized YouTube type beat titles for an 808 mafia producers type beat channel from the raw file name"
        "titles must have high-CTR, & be click-compelling. All artists mentioned in the raw file name must be preserved in the final title\n"
        "Strict operational rules:\n"
        "1. Length: The final string must be under 60 characters to prevent truncation on mobile screens.\n"
        "2. Keywords: DO NOT IGNORE any artist in the raw file name, position the highest-volume search keyword at the beginning of the title.\n"
        "3. Engagement: Always create highly engaging hooks, for example you can add 'prod by $oulesss(808 mafia)' at the end of a title or start with '808 mafia producer made...type beat', get creative but always personalize the producer to at least one of the artistes stated in the raw file name.\n"
        "4. Output format: Return ONLY the raw final title text string. Do not wrap it in quotes, do not include markdown, and do not provide conversational text or explanations.")
    
    try:
        response = client.models.generate_content(
            model='gemini-3.8-flash',
            contents=f"{raw_context}",
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=0.7
            )
        )
        return response.text.strip()
    except Exception as e:
        print(f"AI Optimization failed: {e}. Falling back to a safe character truncation.")
        return raw_context[:60]

def generate_metadata(artist_combo, beat_title):
    if artist_combo in ARTIST_TAGS:
        config = ARTIST_TAGS[artist_combo]
    else:
        artists = [a.strip() for a in artist_combo.split('x')]
        reversed_combo = " x ".join(reversed(artists))
        
        if reversed_combo in ARTIST_TAGS:
            config = ARTIST_TAGS[reversed_combo]
            print(f"Matched reversed artist combo: '{reversed_combo}'")
        else:
            collected_tags = set(ARTIST_TAGS["default"]["tags"])
            matched_genres = []
            
            for artist in artists:
                found_match = False
                for key, data in ARTIST_TAGS.items():
                    if artist in key and key != "default":
                        collected_tags.update(data["tags"])
                        matched_genres.append(data["genre"])
                        found_match = True
                
                if not found_match and len(artist) > 1:
                    formatted_tag = f"#{artist.title().replace(' ', '')}TypeBeat"
                    collected_tags.add(formatted_tag)

            genre = " / ".join(list(set(matched_genres))) if matched_genres else ARTIST_TAGS["default"]["genre"]
            config = {
                "tags": list(collected_tags),
                "genre": genre
            }
            print(f"Dynamic fallback tags generated for custom combination: '{artist_combo}'")


    raw_base_title = f"{artist_combo.title()} Type Beat - {beat_title}"
    

    print("Optimizing video title with Gemini 3.8 Flash...")
    optimized_core_title = get_optimized_title(raw_base_title)
    

    title = f"(free) {optimized_core_title}"
    
    description = (
        f"🎧 Name: '{beat_title}' ({config['genre']}).\n\n"
        f"Produced by $oulesss(808 mafia).\n"
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
            "privacyStatus": "public"  # "unlisted" | "private"
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

  
    chosen_beat = random.choice(audio_files)
    print(f"Selected beat file: {chosen_beat['name']}")


    artist_combo, beat_title = parse_filename(chosen_beat['name'])
    print(f"Detected Artist Combo: {artist_combo} | Beat Title: {beat_title}")

    all_images = [f for f in files if f['name'].lower().endswith(('.jpg', '.jpeg', '.png'))]
    
    matching_variants = [
        img for img in all_images 
        if img['name'].lower().startswith(artist_combo.lower())
    ]

    if matching_variants:
        matched_image = random.choice(matching_variants)
        print(f"Found {len(matching_variants)} variant(s) for '{artist_combo}'. Randomly picked: {matched_image['name']}")
    elif all_images:
        all_flat_images = [img for sublist in image_files.values() for img in sublist]
        matched_image = random.choice(all_flat_images)
        print(f"Exact prefix match for '{artist_combo}' not found. Using fallback image: {matched_image['name']}")
    else:
        print("Error: No images found in Google Drive folder.")
        return

    audio_local = "input_audio.mp3"
    image_local = "input_image.jpg"
    download_file(drive_service, chosen_beat['id'], audio_local)
    download_file(drive_service, matched_image['id'], image_local)


    title, description, tags = generate_metadata(artist_combo, beat_title)


    output_video = "final_output.mp4"
    render_video(audio_local, image_local, output_video)
    upload_to_youtube(youtube_service, output_video, title, description, tags)


    delete_drive_file(drive_service, chosen_beat['id'])
    print("Workflow finished successfully!")

if __name__ == "__main__":
    main()
