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

        Extract every person (row) and their working hours for Monday through Sunday.

        Return ONLY valid JSON in exactly this shape:

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

        Rules for each day's value:
        - If the cell is a work shift, output it as a single string "HH:MM-HH:MM".
        - Use 24-hour time, zero-padded to two digits, a colon between hours and
          minutes, and a single hyphen between start and end. No spaces, no newlines.
          Examples: "7.00" above "16.00" becomes "07:00-16:00";
          "14:15" above "19:10" becomes "14:15-19:10".
        - Use null for anything that is not a work shift: an empty cell, or non-time
          text such as "ej anställd", "sjuk", "ledig", or "semester".
        - Do not invent times. Only use what is shown in the image.

        Return only the JSON, with no markdown fences or commentary.
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

