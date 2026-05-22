import os
import time
from dotenv import load_dotenv
from google import genai
from google.genai import types

# =====================================================================
#  CHANGE YOUR VIDEO SCENARIO HERE
# =====================================================================
SCENARIO = "A glowing futuristic crystal cluster inside a dark stone cave, camera slowly panning around it"
OUTPUT_FILENAME = "agent_video.mp4"
# =====================================================================

load_dotenv()

def run_video_generation():
    client = genai.Client()
    
    print(f"Starting video generation for: '{SCENARIO}'...")
    print("Note: Video generation usually takes a few minutes.")
    
    try:
        # 1. Start the video generation job using Veo
        operation = client.models.generate_videos(
            model='veo-3.1-generate-preview',
            prompt=SCENARIO,
            config=types.GenerateVideosConfig(
                aspect_ratio="16:9"
            )
        )
        
        # 2. Loop and check the status every 10 seconds until finished
        while not operation.done:
            print("Rendering in progress... (checking again in 10s)")
            time.sleep(10)
            # Update the operation status
            operation = client.operations.get(operation)
            
        # 3. Extract, download, and save the final video
        generated_video = operation.response.generated_videos[0]
        
        # Download the file from Google's servers and save locally
        client.files.download(file=generated_video.video)
        generated_video.video.save(OUTPUT_FILENAME)
        
        print(f" Success! Your video has been saved as: {OUTPUT_FILENAME}")
        
    except Exception as e:
        print(f"\n API Error: {e}")

if __name__ == "__main__":
    run_video_generation()