from datetime import date
from typing import NamedTuple

from django.conf import settings

from munera.http import create_http_client


class ParkingPermit(NamedTuple):
    id: str
    permit_number: str
    owner_bsn: str
    registration_number: str
    valid_from: date
    valid_to: date


class CurrusClient:
    def __init__(self, base_url: str):
        self._session = create_http_client(base_url)

    def get_parking_permits(self, bsn: str) -> list[ParkingPermit]:
        response = self._session.get(f"/parking-permits/{bsn}")
        if response.status_code == 404:
            return []

        response.raise_for_status()

        return [ParkingPermit(**item) for item in response.json()]

    def change_registration_number(self, bsn: str, permit_id: str, registration_number: str) -> bool:
        response = self._session.patch(
            f"/parking-permits/{bsn}/{permit_id}", {"registration_number": registration_number}
        )
        if response.status_code == 422:
            return False

        response.raise_for_status()

        return True


currus_client = CurrusClient(settings.MUNERA_CURRUS_URL)
