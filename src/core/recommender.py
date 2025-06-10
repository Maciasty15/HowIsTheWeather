from google import genai
from dotenv import load_dotenv
import os

load_dotenv()
AI_GEMINI_KEY = os.getenv("AI_GEMINI_KEY")

client = genai.Client(api_key=AI_GEMINI_KEY)

def get_recommendation(location, weather_description):
    prompt = (
        f"Lokalizacja: {location}\n"
        f"Pogoda: {weather_description}\n\n"
        "Na podstawie powyższej pogody zaproponuj:\n"
        "- 3 aktywności, które można wykonać na zewnątrz lub w środku opierając się o lokalizacje\n"
        "- Jakie ubranie będzie odpowiednie\n"
        "- Ewentualne porady\n"
    )

    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt,
        )
        return response.text
    except Exception:
        return "Wystąpił błąd podczas uzyskiwania rekomendacji od GeminiAI."