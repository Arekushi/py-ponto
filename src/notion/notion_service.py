from notion_client import AsyncClient


class NotionService:
    def __init__(self, notion_api_key):
        self.client = AsyncClient(auth=notion_api_key)

    async def get_database_data(self, database_id, filter=None):
        try:
            params = {'database_id': database_id}
            
            if filter:
                params['filter'] = filter
            
            response = await self.client.databases.query(**params)
            
            return response['results']
        except Exception as e:
            raise Exception(f'Erro ao obter dados do banco de dados: {e}')

    async def add_database_row(self, database_id, properties):
        try:
            response = await self.client.pages.create(
                parent={'database_id': database_id},
                properties=properties
            )
            
            return response
        except Exception as e:
            raise Exception(f'Erro ao adicionar linha no banco de dados: {e}')
    
    async def update_database_row(self, page_id, properties):
        try:
            response = await self.client.pages.update(
                page_id,
                properties=properties
            )
            
            return response
        except Exception as e:
            raise Exception(f'Erro ao atualizar linha no banco de dados: {e}')

    async def get_database_properties(self, database_id):
        try:
            response = await self.client.databases.retrieve(database_id=database_id)
            return response.get('properties', {})
        except Exception as e:
            raise Exception(f'Erro ao obter propriedades do banco de dados: {e}')
    
    async def create_code_block(self, parent_id, content, language = 'plain text'):
        block = {
            'object': 'block',
            'type': 'code',
            'code': {
                'rich_text': [
                    {
                        'type': 'text',
                        'text': {
                            'content': content
                        }
                    }
                ],
                'language': language
            }
        }
        
        try:            
            response = await self.client.blocks.children.append(
                block_id=parent_id,
                children=[block]
            )
            
            return response
        except Exception as e:
            raise Exception(f'Erro ao criar um code block: {e}')
    
    async def update_code_block(self, block_id, content, language = 'plain text'):
        updated_block = {
            'object': 'block',
            'type': 'code',
            'code': {
                'rich_text': [
                    {
                        'type': 'text',
                        'text': {
                            'content': content
                        }
                    }
                ],
                'language': language
            }
        }
        
        try:
            response = await self.client.blocks.update(
                block_id=block_id,
                **updated_block
            )
            
            return response
        except Exception as e:
            raise Exception(f'Erro ao atualizar o code block: {e}')
    
    async def search_blocks(self, parent_id, filter=None):
        try:
            params = {'block_id': parent_id}
        
            if filter:
                params['filter'] = filter
            
            response = await self.client.blocks.children.list(**params)
            return response.get('results', [])
        except Exception as e:
            raise Exception(f'Erro ao buscar o bloco: {e}')
