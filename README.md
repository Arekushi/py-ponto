<h1 align="center">
    Py-Ponto
</h1>

<p align="center">
    <a href="#" target="blank">
        <img
            src="./assets/py-ponto.svg"
            width="300"
            title="Py-Ponto Logo"
            alt="Py-Ponto Logo"
        />
    </a>
</p>

<p align="center">
    Projeto de marcador automático de ponto universal usando o <a href="https://selenium-python.readthedocs.io/">Selenium</a> com integração com o <a href="https://notion.so">Notion</a>.
</p>

## 🔨 Construído com
- [Python v3.10][python]

## Primeiros passos
Se quiser o projeto para desenvolver, alguns pré-requisitos são necessários.

### Pré-requisitos (Windows)
* Python
  1. Você pode baixar aqui: [Python][python_url]
  2. Aqui tem um tutorial passo-a-passo. [(Tutorial)][python_tutorial_url]
     1. Tutorial com Miniconda. [(Tutorial)][miniconda_tutorial]
* Poetry
  1. Você pode instalar aqui: [Poetry][poetry_url]

## Variáveis sensíveis
Eu guardo algumas variáveis sensíveis em alguns arquivos, estes deverão estar na pasta `config/yaml`

### .secrets.toml
Algumas informações de login, tokens e chaves
```yaml
login:
    user: '...' # Email ou username
    password: '...' # Código de acesso, senha, etc
urls:
    portal: '...' # URL inicial do endereço onde é realizado a marcação de ponto
chrome:
    userdata: '...' # Diretório onde fica o UserData do Chrome
```

### notion.yaml
Aqui, caso queira uma integração com o Notion, recomendo criar em uma página alguns databases com as seguintes propriedades. Aqui também fica a `api_key` da integração, que pode ser obtida [aqui][notion_integration].

Você pode criar sua própria integração com o Notion, basta criar um serviço que use o `NotionService` e realize seus registros a maneira que quiser.

**NÃO** é um elemento obrigatório, caso não queira a integração com o Notion.

O modelo abaixo auxilia na construção desse serviço [aqui][cantinho_trabalho_service].

```yaml
notion:
    api_key: '...' # API Key da sua Integração com o Notion
    cantinho_trabalho:
        databases:
            marcacao_ponto:
                id: '...'
                properties:
                    empresa:
                        name: 'Empresa'
                        type: 'relation'
                    data:
                        name: 'Data'
                        type: 'date'
                    entrada_1:
                        name: 'Entrada 1'
                        type: 'date'
                    entrada_2:
                        name: 'Entrada 2'
                        type: 'date'
                    entrada_3:
                        name: 'Entrada 3'
                        type: 'date'
            empresas:
                id: '...'
                properties:
                    status:
                        name: 'Status'
                        type: 'select'
                        options:
                            ativo: 'Ativo'
                            desligado: 'Desligado'

            folgas:
                id: '...'
                properties:
                    dia_de_folga:
                        name: 'Dia de Folga'
                        type: 'date'
```

### xpath.toml
XPATH dos elementos do site. Não há uma maneira padrão para criar, então é possível criar a sua maneira, aqui está apenas um exemplo.
```yaml
pages:
    login:
        confirm_preferences_a: "..."
        goto_portal_input: "..."
        user_input: "..."
        next_input: "..."
        password_input: "..."
        login_span_button: "..."
        stay_connected_yes_input: "..."
    portal:
        register_img: "..."
        mark_a: "..."
```

## Outras variáveis dos arquivos `.toml`
Eu guardo algumas informações em arquivos `.toml` dentro da pasta `config`.

### settings.toml
Algumas configurações de customização da aplicação.
```yaml
constants:
    start_minutes_delay: 5 # Delay de tempo para iniciar o processo
    random_clocking_minutes_delay: 2 # Tempo aleatório de tempo para marcação do ponto
    timeout_notification_minutes: 3 # Tempo de timeout para as interações das notificações
    dirs:
        logging: 'logs' # Diretório de logs a partir da raíz do projeto
```

## Actions
Para organizar melhor o projeto, decidi criar um dicionário onde é definido ações que serão realizadas em ordem, e aplicar os métodos em uma classe com os métodos implementados.

Essas ações são definidas da seguinte forma:
```python
ACTIONS = [
    {
        'type': AT.INPUT, #Irá inputar algum dado em um input
        'xpath': '...',
        'value': '...'
    },
    {
        'type': AT.CLICK, # Irá clicar em um elemento
        'xpath': '...'
    },
    {
        'type': AT.SLEEP, # Fará a thread dormir por um tempo estipulado
        'time': 3 * 60 # 3 minutos
    },
    {
        'type': AT.WAIT_FOR, # Ele irá aguardar até esse elemento ficar visível
        'xpath': '...'
    },
    {
        'type': AT.KEYBOARD_SHORTCUT, # Realizará um comando do teclado
        'keys': ['ctrl', 'alt', '0'], # Teclas a serem pressionadas
        'redo_time': 10 # OPCIONAL: Tempo de cooldown para realizar a mesma combinação de teclas
    }
    {
        'type': AT.CUSTOM, # Irá executar uma ação customizada
        'callback': callback # Esse método receberá o driver e o WebDriverWait
    }
]
```

## 👨‍💻 Contribuidores
| [<div><img width=115 src="https://avatars.githubusercontent.com/u/54884313?v=4"><br><sub>Alexandre Ferreira de Lima</sub><br><sub>alexandre.ferreira1445@gmail.com</sub></div>][arekushi] <div title="Code">💻</div> |
| :---: |

<!-- [Build With] -->
[python]: https://www.python.org/downloads/release/python-3100/

<!-- [Some links] -->
[selenium]: https://selenium-python.readthedocs.io/
[python_url]: https://www.python.org/downloads/
[python_tutorial_url]: https://www.digitalocean.com/community/tutorials/install-python-windows-10
[miniconda_tutorial]: https://katiekodes.com/setup-python-windows-miniconda/
[poetry_url]: https://python-poetry.org/docs/#installation
[notion_integration]: https://www.notion.so/profile/integrations
[cantinho_trabalho_service]: https://github.com/Arekushi/py-ponto/blob/main/src/cantinho_trabalho/cantinho_trabalho_service.py

<!-- [Constributors] -->
[arekushi]: https://github.com/Arekushi
