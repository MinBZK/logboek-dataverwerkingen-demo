from django.apps import AppConfig
from django.conf import settings

from logboek import init_processing_operator, Resource
from logboek.handlers import GrpcProcessingOperationHandler

from munera import __commit__, __version__


class MuneraConfig(AppConfig):
    name = "munera"
    verbose_name = "Munera"

    def ready(self) -> None:
        resource = Resource(self.name, f"{__version__}-{__commit__}")
        handler = GrpcProcessingOperationHandler(settings.MUNERA_LOGBOEK_ENDPOINT)
        init_processing_operator(resource, handler)
