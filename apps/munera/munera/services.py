from django.core.cache import cache

from logboek import StatusCode, get_processing_operator
from logboek.attributes import Core

from munera.models import User
from munera.remote import currus_client


_CACHE_TTL = 300

_CHANGE_REGISTRATION_NUMBER = "rva:0b1ff20a-3ecb-34bf-8cf5-e4cbacb046ab"
_FETCH_PARKING_PERMITS = "rva:982c9acc-4250-4721-9426-628a3baa3e15"

logboek_operator = get_processing_operator()


class ParkingService:
    def __init__(self, user: User):
        self._user = user
        self._cache_key = f"${user.pk}:{user.get_username()}"
        self._permits: dict = None

    def get_parking_permit(self, id):
        self._load()
        return self._permits.get(id, None)

    def list_parking_permits(self):
        self._load()
        return self._permits.values()

    def change_registration_number(self, permit_id: str, registration_number: str) -> bool:
        with logboek_operator.start_proccessing_as_current("change_registration_number") as op:
            op.set_attribute(Core.PROCESSING_ACTIVITY_ID, _CHANGE_REGISTRATION_NUMBER)

            success = currus_client.change_registration_number(self._user.bsn, permit_id, registration_number)
            op.set_status(StatusCode.OK)

        if success:
            cache.delete(self._cache_key)

        return success

    def _load(self):
        if self._permits is None:
            parking_permits = cache.get_or_set(self._cache_key, self._default, _CACHE_TTL)
            self._permits = {p.id: p for p in parking_permits}

        return self._permits

    def _default(self):
        with logboek_operator.start_proccessing_as_current("fetch_parking_permits") as op:
            op.set_attribute(Core.PROCESSING_ACTIVITY_ID, _FETCH_PARKING_PERMITS)
            permits = currus_client.get_parking_permits(self._user.bsn)
            op.set_status(StatusCode.OK)

        return permits
