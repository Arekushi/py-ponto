from dependency_injector import containers, providers
from config.config import settings

from src.cantinho_trabalho.cantinho_trabalho_service import CantinhoTrabalhoService
from src.notion.notion_service import NotionService


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    notion_service = providers.Factory(
        NotionService,
        notion_api_key=settings.notion.api_key
    )
    
    cantinho_trabalho_service = providers.Factory(
        CantinhoTrabalhoService,
        notion_service=notion_service,
        databases=settings.notion.cantinho_trabalho.databases
    )
