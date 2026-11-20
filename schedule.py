import html
import os
from datetime import datetime
from zoneinfo import ZoneInfo
import requests

BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]
TIMEZONE = "Asia/Kolkata"

TIMETABLE = {
    "Monday": [
        ("09:00 AM - 10:00 AM", "Data Structures", "Room 204"),
        ("10:00 AM - 11:00 AM", "Operating Systems", "Room 102"),
        ("11:15 AM - 01:00 PM", "DS Lab", "Lab 3"),
    ],
    "Tuesday": [
        ("09:00 AM - 10:00 AM", "Database Systems", "Room 201"),
        ("10:00 AM - 11:00 AM", "Computer Networks", "Room 204"),
        ("02:00 PM - 03:00 PM", "Discrete Mathematics", "Room 105"),
    ],
    "Wednesday": [
        ("09:00 AM - 10:00 AM", "Operating Systems", "Room 102"),
        ("10:00 AM - 11:00 AM", "Software Engineering", "Room 301"),
    ],
    "Thursday": [
        ("09:00 AM - 10:00 AM", "Computer Networks", "Room 204"),
        ("11:00 AM - 12:00 PM", "Database Systems", "Room 201"),
        ("02:00 PM - 04:00 PM", "DBMS Lab", "Lab 2"),
    ],
    "Friday": [
        ("09:00 AM - 10:00 AM", "Discrete Mathematics", "Room 105"),
        ("10:00 AM - 11:00 AM", "Software Engineering", "Room 301"),
    ],
    "Saturday": [],
    "Sunday": [],
}


def format_message(day_name: str, classes: list[tuple[str, str, str]]) -> str:
    safe_day = html.escape(day_name)
    if not classes:
        return (
            f"☀️ <b>Good Morning!</b>\n"
            f"Today is <b>{safe_day}</b> — No classes scheduled."
        )

    lines = [f"📚 <b>Today's Schedule — {safe_day}</b>"]
    for idx, (time_slot, subject, room) in enumerate(classes, start=1):
        safe_time = html.escape(time_slot)
        safe_subject = html.escape(subject)
        room_part = f" • 📍 {html.escape(room)}" if room else ""
        lines.append(f"<b>{idx}. {safe_subject}</b>\n🕒 {safe_time}{room_part}")

    return "\n\n".join(lines)


def send_telegram_message(text: str) -> None:
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "HTML",
    }
    response = requests.post(url, json=payload, timeout=15)
    response.raise_for_status()
    data = response.json()
    if not data.get("ok"):
        raise RuntimeError(f"Telegram API error: {data.get('description', 'Unknown error')}")


def main() -> None:
    now = datetime.now(ZoneInfo(TIMEZONE))
    day_name = now.strftime("%A")
    classes = TIMETABLE.get(day_name, [])
    message = format_message(day_name, classes)
    send_telegram_message(message)


if __name__ == "__main__":
    main()
  
