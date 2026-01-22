import requests
from ics import Calendar, Event
from datetime import datetime
import pytz

# API endpoint
url = "https://comet.fsf.fo/data-backend/api/public/areports/run/0/50/?API_KEY=eae8bda57126f3cdffb4f29bb55bf4f0fbf7fca83a0b8118fe5a09630c1526b68f293e93abb6f4c407a1c42909ef8108871f92c2ec9c04aa626ebf90dab72c86"

response = requests.get(url, timeout=30)
response.raise_for_status()
data = response.json()

calendar = Calendar()
tz = pytz.timezone("Atlantic/Faroe")

INFO_URL = "https://www.fsf.fo/kappingar-og-urslit/menn/meistaradeildin-menn/"

for match in data.get("results", []):
    timestamp = match.get("matchDate")
    if not timestamp:
        continue

    description = match.get("matchDescription", "Ókend dystur")
    location = match.get("facility", "Ókend leikvøllur")
    round_number = match.get("round", "")
    competition = match.get("competitionType", "Meistaradeildin")

    start = datetime.fromtimestamp(timestamp / 1000, tz)

    event = Event()
    event.name = description
    event.begin = start
    event.duration = {"hours": 2}
    event.location = location

    # Clean description (no match status)
 event.description = (
    f"🏆 {competition}\n"
    f"🔁 Umfar: {round_number}\n"
    f"📅 Skrá & stigatalva: {INFO_URL}"
)

    calendar.events.add(event)

with open("meistaradeildin.ics", "w", encoding="utf-8") as f:
    f.write(str(calendar))
