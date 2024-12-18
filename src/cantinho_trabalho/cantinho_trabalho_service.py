from src.helpers.date_helper import now_date_str, now_datetime_str
from src.exceptions.notion_pipeline_exception import NotionException
from src.notion.notion_service import NotionService


class CantinhoTrabalhoService:
    def __init__(
        self,
        notion_service: NotionService,
        databases
    ):
        self.notion_service = notion_service
        self.databases = databases

    async def get_active_company(self):
        empresas = self.databases.empresas
        status = empresas.properties.status

        response = await self.notion_service.get_database_data(
            database_id=empresas.id,
            filter={
                'property': status.name,
                status.type: {
                    'equals': status.options.ativo
                }
            }
        )

        return response[0]

    async def today_is_day_off(self):
        folgas = self.databases.folgas
        dia_de_folga = folgas.properties.dia_de_folga

        response = await self.notion_service.get_database_data(
            database_id=folgas.id,
            filter={
                'property': dia_de_folga.name,
                dia_de_folga.type: {
                    'equals': now_date_str()
                }
            }
        )

        return response != []

    async def register_time_entry(self):
        today_time_entry = await self.get_today_time_entry()

        if not today_time_entry:
            return await self.add_time_entry()

        next_entry = self.get_next_entry(today_time_entry)

        if next_entry:
            return await self.update_time_entry(
                page_id=today_time_entry['id'],
                properties=next_entry
            )
        else:
            raise NotionException(
                'Não há mais entradas disponíveis para registro!'
            )

    async def add_log_time_entry(self, time_entry_id, log_content):
        return await self.notion_service.create_code_block(
            parent_id=time_entry_id,
            content=log_content
        )

    async def add_time_entry(self):
        marcacao_ponto = self.databases.marcacao_ponto
        empresa = marcacao_ponto.properties.empresa
        entrada_1 = marcacao_ponto.properties.entrada_1

        active_company = await self.get_active_company()
        time_entry_properties = {
            'Nome': {
                'title': [
                    {
                        'text': {
                            'content': now_date_str('%d/%m/%Y')
                        }
                    }
                ]
            },
            empresa.name: {
                empresa.type: [
                    {
                        'id': active_company['id']
                    }
                ]
            },
            entrada_1.name: {
                entrada_1.type: {
                    'start': now_datetime_str()
                }
            }
        }

        response = await self.notion_service.add_database_row(
            database_id=marcacao_ponto.id,
            properties=time_entry_properties
        )

        return response

    async def get_today_time_entry(self):
        marcacao_ponto = self.databases.marcacao_ponto
        data = marcacao_ponto.properties.data

        response = await self.notion_service.get_database_data(
            database_id=marcacao_ponto.id,
            filter={
                'property': data.name,
                data.type: {
                    'equals': now_date_str()
                }
            }
        )

        try:
            return response[0]
        except IndexError:
            return None

    async def update_time_entry(self, page_id, properties):
        response = await self.notion_service.update_database_row(
            page_id=page_id,
            properties=properties
        )

        return response

    def get_next_entry(self, time_entry_row):
        entries = {
            key: value for key, value in time_entry_row['properties'].items()
            if (key.startswith('Entrada ') and value['type'] == 'date')
        }

        for entry in sorted(entries.keys()):
            registry = entries[entry]
            date = registry.get('date')

            if date:
                if date.get('start') and not date.get('end'):
                    date['end'] = now_datetime_str()
                    return {
                        entry: registry
                    }
            else:
                registry['date'] = {
                    'start': now_datetime_str(),
                    'end': None
                }

                return {
                    entry: registry
                }

        return None
