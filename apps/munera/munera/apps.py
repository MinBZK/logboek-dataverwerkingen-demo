from django.apps import AppConfig
from django.conf import settings

from logboek import init_processing_operator
from logboek.handlers import GrpcProcessingOperationHandler


class MuneraConfig(AppConfig):
    name = "munera"
    verbose_name = "Munera"

    def ready(self) -> None:
        handler = GrpcProcessingOperationHandler(settings.MUNERA_LOGBOEK_ENDPOINT)
        init_processing_operator(handler)
