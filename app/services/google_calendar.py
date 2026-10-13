from functools import lru_cache
from pathlib import Path

from fastapi import HTTPException
from google.oauth2 import service_account
from googleapiclient.discovery import build

from app.config import settings

SCOPES = ["https://www.googleapis.com/auth/calendar"]


@lru_cache(maxsize=1)
def calendar_service():
    credentials_path = settings.google_calendar_credentials_file
    if not credentials_path or not Path(credentials_path).is_file():
        raise HTTPException(
            status_code=503,
            detail="Google Calendar não configurado. Defina GOOGLE_CALENDAR_CREDENTIALS_FILE.",
        )

    credentials = service_account.Credentials.from_service_account_file(
        credentials_path, scopes=SCOPES
    )
    return build("calendar", "v3", credentials=credentials, cache_discovery=False)


def calendar_id() -> str:
    if not settings.google_calendar_id:
        raise HTTPException(
            status_code=503,
            detail="Defina GOOGLE_CALENDAR_ID nas variáveis de ambiente.",
        )
    return settings.google_calendar_id


def freebusy(start_iso: str, end_iso: str) -> list[dict]:
    service = calendar_service()
    result = service.freebusy().query(
        body={
            "timeMin": start_iso,
            "timeMax": end_iso,
            "items": [{"id": calendar_id()}],
        }
    ).execute()
    calendar = result.get("calendars", {}).get(calendar_id(), {})
    if calendar.get("errors"):
        raise HTTPException(status_code=502, detail="Não foi possível consultar a agenda Google.")
    return calendar.get("busy", [])


def create_event(summary: str, description: str, start_iso: str, end_iso: str) -> str:
    service = calendar_service()
    event = service.events().insert(
        calendarId=calendar_id(),
        body={
            "summary": summary,
            "description": description,
            "start": {"dateTime": start_iso, "timeZone": settings.app_timezone},
            "end": {"dateTime": end_iso, "timeZone": settings.app_timezone},
        },
    ).execute()
    return event["id"]


def delete_event(event_id: str) -> None:
    service = calendar_service()
    service.events().delete(calendarId=calendar_id(), eventId=event_id).execute()
