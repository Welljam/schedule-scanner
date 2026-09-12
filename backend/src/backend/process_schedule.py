from google import genai
from dotenv import load_dotenv
from PIL import Image
import os
import json
import io

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

prompt = """
        Analyze this schedule image.

        Extract every person/row and their working hours for Monday through Sunday.

        Return ONLY JSON in this format:

        {
          "people": [
            {
              "row": 1,
              "name": "John",
              "monday": "08:55-13:30",
              "tuesday": null,
              "wednesday": "10:00-16:00",
              "thursday": null,
              "friday": "08:55-13:30",
              "saturday": null,
              "sunday": null
            }
          ]
        }

        Use null when a cell is empty.
        Preserve the times exactly as written in the image.
"""

def analyze_schedule(image_bytes):
  img = Image.open(io.BytesIO(image_bytes))

  response = client.models.generate_content(
    model="gemini-3.5-flash-lite",
    contents=[img, prompt],
  )

  raw_text = response.text
  print(raw_text)

  raw_text = response.text.strip()

  if raw_text.startswith("```json"):
      raw_text = raw_text[7:]
  if raw_text.endswith("```"):
      raw_text = raw_text[:-3]

  print("\n", raw_text)
  return raw_text.strip()

