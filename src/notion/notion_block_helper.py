from src.helpers.text_helper import split_text_by_limit


def create_code_block(content, language = 'plain text'):
    texts = split_text_by_limit(content)
    
    def get_rich_texts():
        rich_texts = []
        
        for text in texts:
            rich_texts.append(
                {
                    'type': 'text',
                    'text': {
                        'content': text
                    }
                }
            )
        
        return rich_texts
    
    block = {
        'object': 'block',
        'type': 'code',
        'code': {
            'rich_text': get_rich_texts(),
            'language': language
        }
    }
    
    return block
