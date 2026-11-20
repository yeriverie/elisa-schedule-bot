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
        ("09:00 AM - 10:00 AM", "DSA (Data Science & Its Applications)", "LH-15"),
        ("10:00 AM - 11:00 AM", "DBMS (Database Management System)", "LH-15"),
        ("11:15 AM - 12:15 PM", "ES (Environmental Studies)", "LH-15"),
        ("12:15 PM - 01:15 PM", "PML (Principles of Machine Learning)", "LH-15"),
        ("02:15 PM - 04:15 PM", "AIML Lab (B1) / DBMS Lab (B2)", "Lab"),
    ],
    "Tuesday": [
        ("09:00 AM - 10:00 AM", "DSA (Data Science & Its Applications)", "LH-15"),
        ("10:00 AM - 11:00 AM", "DBMS (Database Management System)", "LH-15"),
        ("11:15 AM - 01:15 PM", "Mini-Project (B2)", ""),
        ("02:15 PM - 04:15 PM", "AIML Lab (B2) / DBMS Lab (B1)", "Lab"),
    ],
    "Wednesday": [
        ("09:00 AM - 10:00 AM", "DSA (Data Science & Its Applications)", "LH-15"),
        ("10:00 AM - 11:00 AM", "DBMS (Database Management System)", "LH-15"),
        ("11:15 AM - 12:15 PM", "ES (Environmental Studies)", "LH-15"),
        ("12:15 PM - 01:15 PM", "HCI (Human Computer Interface)", "LH-15"),
        ("02:15 PM - 03:15 PM", "RMIPR (Research Methodology & IPR)", "LH-15"),
        ("04:15 PM - 05:15 PM", "NSS / PHY / YOGA", ""),
    ],
    "Thursday": [
        ("09:00 AM - 11:00 AM", "COE", ""),
        ("11:15 AM - 01:15 PM", "Mini-Project (B1)", ""),
        ("02:15 PM - 03:15 PM", "PML (Principles of Machine Learning)", "LH-15"),
        ("03:15 PM - 04:15 PM", "HCI (Human Computer Interface)", "LH-15"),
    ],
    "Friday": [
        ("09:00 AM - 10:00 AM", "HCI (Human Computer Interface)", "LH-15"),
        ("10:00 AM - 11:00 AM", "PML (Principles of Machine Learning)", "LH-15"),
        ("11:15 AM - 01:15 PM", "COE", ""),
        ("02:15 PM - 03:15 PM", "RMIPR (Research Methodology & IPR)", "LH-15"),
    ],
    "Saturday": [
        ("09:00 AM - 10:00 AM", "PML (Principles of Machine Learning)", "LH-15"),
        ("10:00 AM - 11:00 AM", "DSA (Data Science & Its Applications)", "LH-15"),
        ("11:15 AM - 12:15 PM", "RMIPR (Research Methodology & IPR)", "LH-15"),
    ],
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
    
