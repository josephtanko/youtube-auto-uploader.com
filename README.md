# youtube-auto-uploader.com

This python codebase utilizes GitHub Actions to schedule automatic script runs using cron. The script grabs files from a designated google drive folder; in this case a random .mp3 file and uses the files name to randomly pick from a variety of corresponding images - used as the video image/thumbnail.

# SETTING UP YOUR CREDENTIALS

For this script to run successfully, you have to authourize it by providing your API credentials for the google drive and YouTube account. Additionally, the AI powered SEO optimizer will also need authourization credentials before it can begin to successfully optimize your video titles.

The credentials required for this script to function correctly are named below, ensure you name them EXACTLY as stated when configuring your enviroment secrets.
- DRIVE_FOLDER_ID
- GEMINI_API_KEY
- GOOGLE_CLIENT_ID
- GOOGLE_CLIENT_SECRET
- GOOGLE_REFRESH_TOKEN

1. **DRIVE_FOLDER_ID** - Create a new folder in the google drive under the same account as the destination channel. Open the new folder and click on your browser address bar to copy the ID string (The string of values after the last "/") e.g: https://drive.google.com/drive/folders/*1YGb...id string...fx08* . Save this string somewhere you will require it later.

2. **GEMINI_API_KEY** - This script uses gemini-3.8-flash which is a light weight free-tier language model. To get your gemini API credentials head on over to *https://aistudio.google.com/* .
After you sign-in, on the bottom of the left sidebar, click on the key 🔑 icon to access your api keys then click on "Create API Key", leave the default settings, create and copy your API key. Save this key somewhere you will require it later.

3. **GOOGLE_CLIENT_ID & GOOGLE_CLIENT_SECRET** - Head on to *https://console.cloud.google.com* and sign in with the same account as the destination channel. On the top bar click on "Select a project" and create a "New project", Name your project 'YouTube-Uploader.com' and click create. 
**!NOTE** - if you're asked to do MFA (Multi Factor Authentication) do so before continuing this step.
Click on the notification bell icon on the top right of the page and then click "Select project". 
On the left sidebar hover over "APIs and services" and click on "OAuth consent screen". Click on "Get started" and name your App "youtube-uploader.com", under "User support email", select your email and click on "Next", then select "External", click on "Next" and input your email address then check the agree box and click "continue" then create.
After creating, on the left sidebar, click on "Audience", scroll down under Test users and click to add a user, ensure you put the gmail account tied to the destination youtube channel and click on "Save".
Now, go back to "Overview" on the left sidebar and click on the first option "Create OAuth Client ID". Fill in the required fields as follows:
- Under "Application type" select WebApp
- Name: WebRunner
- Under "Authorized redirect URLs" paste this URL: https://developers.google.com/oauthplayground
Click on "Create"
**WARNING**: DO NOT close the pop up screen that appears immediately after clicking on Create, this is a view-once only screen!
Copy both the Client ID & Client Secret appearing on the pop-up and store them somewhere safe, as you will require them later. (Alternatively, you can click on "Download JSON" to download a .json copy of the credentials to store on your pc locally)

4. **GOOGLE_REFRESH_TOKEN** - To generate a refresh token that allows the script have unlimited access to your google APIs, head on to *https://developers.google.com/oauthplayground* , Once on the site click on the gear icon (settings) on the top right of the page and check the "Use your own OAuth credentials" box. Paste the Client ID & Client Secret that you copied earlier into the appropriate fields and close. 
On the left panel, scroll and look for: "Drive API vX", expand the dropdown and select (https://www.googleapis.com/auth/drive), then scroll down further and look for "YouTube Data API vX vX" expand the dropdown and select (https://www.googleapis.com/auth/youtube.upload).
Click the blue "Authorize APIs" button, and log into the same account as the destination channel. Click on "continue" when prompted with the "Google has not authorized..." screen, then check all options and continue. You will be redirected back to the page where you can now click on the "Exchange authorization code for tokens" button, once exchanged copy the 'Refresh token' from the box below and save it somewhere as you will require it later. 

# PUSHING TO GITHUB

If you're already familiar with github you can push this repo directly; 'requirements.txt' & 'upload.py' exist in the main branch together with .github/workflows/'upload.yml'. 
If you're completely new to GitHub however don't worry, start by creating an account on *https://github.com/* . 
After creating your account, click on the "+" icon on the top right and create a new repository, name your repo 'youtube-uploader.com' and enable the "Add README" option, then click on "Create Repository"
After creating, click on Add file > Create new file and name it 'uploader.py'. 
Copy the entire code template from 'upload.py' and paste it directly in the file then click on "Commit changes".
On the left sidebar, click on the '+' icon again and create a new file, name it 'requirements.txt', then copy all the contens of the 'requirements.txt' file here and paste it directly in the new file and then click on "Commit changes".
On the left sidebar, click on the '+' icon again and create a new file, in the name field type: 
'.github/workflows/upload.yml', and then copy all the contens of the 'upload.yml' file here and paste it directly in the new file and then click on "Commit changes".

# TAILORING THE SCRIPT TO FIT YOUR NICHE

If you're already familiar with python the script is pretty straight forward, with comments made where necessary. Feel free to adjust where you feel like. However, If you are not familiar with python don't worry, this step by step guide will show you how you can use AI to customize the script and tailor it to you specific niche.

1. **Customizing your tags and artist database** #Line 19

Paste this prompt directly into your AI chat model: 
'''Help me lookup SEO friendly tags for the following artist(s) on my youtube type beat channel; 
*insert your artist combinations here e.g: drake x travis scott, future x young thug,..., etc - you can also use single artists* And append each of them into an 'ARTIST_TAGS' python dict, using this format:

```
ARTIST_TAGS = {
    "artist 1 x artist 2": {
        "tags": [
            "#tag 1", "#tag 2", "#tag 3"
        ],
        "genre": "genre description"
    },

    "default": {
        "tags": [
            "#defaultTag1", "#defaultTag2", "#defaultTag3"
        ],
        "genre": "default genre"
    }
}
```
Return a python dict that follows the format in the guide I provided exactly, containing the artist(s) mentioned and their respective tags and genre'''

Copy the code snippet the AI model generates and replace the old ARTIST_TAGS code block (lines 20 - 34). 
**!NOTE**: It is highly unlikely that the AI model messes this up, but it is advisable to cross-check and make sure the code snippet generated follows the exact same structure as the one provided.

2. **AI title optimization & SEO** #Line 78

- System prompt : This one is pretty straight forward. Simply adjust the language models system prompt to control how it optimizes your video titles.
- Model configuration : Change if you have a preferred optimization model you would like to use. Adjust the temperature based on how expressive or creative you want to model to be when it comes to title generation.

3. **Customizing Video Metadata & Upload settings** #Line 141

- You can customize how the video metadata is processed such as it's description, as well as how the title is formatted after optimization. 
- You can adjust the visibility of published videos by changing the "privacyStatus" parameter to "private" for private releases or "unlisted" (quotes included)

# CONFIGURING ENVIRONMENT SECRETS & SCHEDULED UPLOADS

1. **Configuring Environment secrets** 

Make sure the 'upload.py' script is fully tailored to your niche and has all the necessary fields adjusted based on your info. Still on GitHub, click on "Settings" at the top bar and under "Secrets & Variables" click on "Actions". Click add a "New Repository Secret" and add all your Enviroment secrets one after the other (in no particular order).

These secrets are the credetial keys you stored earlier:

- DRIVE_FOLDER_ID -> your 'id string' copied from the https://drive.google.com/drive/folders/1YGb...id string...fx08 link
*it should look like this: 1LJ1SALJmTJCWf3_ZpC_LBsLEf3EEofGi*

- GEMINI_API_KEY -> your gemini api key gotten from https://aistudio.google.com/
*it should look like this: AIzaSyDummyKey_2026_DemoExampleXyZ789abc*

- GOOGLE_CLIENT_ID -> your 'Client ID' gotten from https://console.cloud.google.com
*it should look like this: "7XXX077XXXX-xxxx2xx1cgpmkxxxaaxxxsas5ms9gtv1043.apps.googleusercontent.com"*

- GOOGLE_CLIENT_SECRET -> your 'Client Secret' gotten from https://console.cloud.google.com
*it should look like this: GOCSPX-a4000000000005Q5pxxxXXXxjbDS*

- GOOGLE_REFRESH_TOKEN -> your 'Refresh token' gotten from https://developers.google.com/oauthplayground
*it should look like this: 1//04sigbqx0x0x0CgYIAXXXXNwF-M9ntLVhtCmUxxXx2bx_aDQb30A--YcKin9K8K_Mp00000000000000000000xxxxx9SjmY*

**!NOTE** Ensure that YOUR_SECRET_NAME matches the secret names written here EXACTLY, the credentials shown here are for example purposes only, you should never share your API keys with anyone.

2. **Scheduling uploads**

Now all thats left is to pick a time we want the script to auto-run, and set it in the 'upload.yml' file located in '.github/workflows/' We can easily do this using, Cron - a time-based job scheduler. Cron is very useful for scheduling repetitive tasks.

Open the 'upload.yml' file, and under; #Line 3
```
on:
  schedule:
    - cron: '0 1 * * *'  # adjust the cron schedule as needed (this example runs daily at 1 AM UTC)
  workflow_dispatch: 
```
As you can see, the default time is set to run the script daily at 1 AM UTC, cron time is equivalent to 24hr time in UTC, so changing the second cron value to:
```
    - cron: '17 * * *' # means the script will run every day at 17:00 UTC or 5PM every day.
```
You can try different cron expressions to choose/skip some days allowing the script to run only on weekdays, bi weekly, or every other day.

            ┌───────────── minute (0 - 59)
            │ ┌─────────── hour (0 - 23)
            │ │ ┌───────── day of the month (1 - 31)
            │ │ │ ┌─────── month (1 - 12)
            │ │ │ │ ┌───── day of the week (0 - 6) (Sunday to Saturday)
            │ │ │ │ │
    - cron: * * * * *

If scheduling get's too technical, you can always ask an AI chat model to give you the cron expression for a particular schedule you would like to follow, the options are limitless.

# TIPS FOR UPLOADING TO GOOGLE DRIVE

Great! You're all set. Now you can start uploading your files to the google drive folder you created earlier, here are some helpful tips to ensure that the beat selection, image and tag pairing goes smoothly!

1. When uploading your files to the google drive, ensure that you begin naming the audio file with the artist(s) name first, so: 
'artist x artist type beat - BEAT NAME.mp3' so that it is easier for the script to parse the file name and correctly match it to it's corresponding tags.
2. You can upload multiple images for a particular artist or artist(s), the script will pick one at random each time. When uploading multiple images for the same artist(s), ensure that you use an identifier to separate the files with duplicate names so that google drive doesn't overwrite them, e.g: 'artist x artist v1.jpg' so a file named 'drake x travis scott v1.jpg' can be in the same folder with another file named 'drake x travis scott v2.jpg'
3. The beats are picked at random, if you'd like for there to be an ordered selection process for the mp3 files, do well to reach out to me on X @josephtanko98 or via email: josephtanko98@gmail.com



