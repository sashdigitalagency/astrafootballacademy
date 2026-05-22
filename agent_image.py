import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

# =====================================================================
#  CHANGE YOUR SCENARIO HERE
# =====================================================================
SCENARIO = "A glowing futuristic crystal cluster inside a dark stone cave"
OUTPUT_FILENAME = "agent_output.png"
# =====================================================================

# Automatically load the GEMINI_API_KEY from your .env file
load_dotenv()

def run_generation():
    # Initialize the Gemini client
    client = genai.Client()
    
    print(f"Starting generation for scenario: '{SCENARIO}'...")
    
    try:
        # NEW METHOD: Use generate_content with the updated image model
        response = client.models.generate_content(
            model='gemini-2.5-flash-image',
            contents=SCENARIO,
            config=types.GenerateContentConfig(
                # Explicitly tell the model to return an image, not text
                response_modalities=["IMAGE"],
                image_config=types.ImageConfig(
                    aspect_ratio="16:9"
                )
            )
        )
        
        # The new SDK returns the image directly in the response parts
        for part in response.parts:
            if part.inline_data:
                # The SDK automatically converts it to a PIL Image format
                image = part.as_image()
                image.save(OUTPUT_FILENAME)
                print(f" Success! Your image has been saved as: {OUTPUT_FILENAME}")
                break
                
    except Exception as e:
        print(f"\n API Error: {e}")
        print("Please check your .env file or internet connection.")

if __name__ == "__main__":
    run_generation()