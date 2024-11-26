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

## Sobre
A principal motivação para este projeto? `Preguiça`. Sim, isso mesmo: *preguiça*. Esta aplicação foi desenvolvida para automatizar o processo de registro de ponto, tornando a vida mais prática para quem, como eu, esquece facilmente das coisas ou simplesmente prefere simplificar tarefas repetitivas.

Além de automatizar o registro de ponto, este projeto **também** se destaca por oferecer uma funcionalidade essencial: a documentação própria das marcações. Isso significa que você terá um histórico organizado e acessível das suas marcações de ponto, independente do sistema da empresa. Nesse contexto, o [Notion][notion] se encaixa perfeitamente, oferecendo a possibilidade de utilizá-lo como um banco de dados intuitivo e de fácil uso.

A aplicação utiliza [Selenium][selenium], portanto, é necessário que o registro de ponto possa ser feito através de um site.

Em atualizações futuras, pretendo incluir suporte para autenticação em duas etapas, usando emulador de Android por exemplo, ampliando as possibilidades de manter a automatização do processo.

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

### .secrets.yaml
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

### xpath.yaml
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

## Outras variáveis dos arquivos `.yaml`
Eu guardo algumas informações em arquivos `.yaml` dentro da pasta `config/yaml`.

### settings.yaml
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

## Configurando Scheduling Tasks
Preparei alguns scripts e configurações prontos para uso, mas também é possível criar configurações personalizadas conforme sua necessidade. O processo envolve executar o script `main.py` para registrar o ponto e, eventualmente, usar o `delete_logs.py` para apagar os arquivos de log.

### Windows
No Windows, o processo é simples. Primeiro, será necessário criar os arquivos `start.bat` e `delete_logs.bat`. Você encontrará versões de exemplo desses arquivos com a extensão `.dist`, localizadas no diretório `scripts/windows`.

> Edite o caminho completo para apontar para o ambiente Python com as dependências e o script `main.py`. O mesmo procedimento se aplica ao `delete_logs.bat`.

#### Exemplo de `start.bat`
```bat
@echo off
"C:\Users\user\miniconda3\envs\pyponto\python.exe" "C:\Users\user\Workspaces\Python\pyponto\main.py"
```

Depois disso, crie o arquivo `create-tasks.ps1` com base no arquivo `create-task.ps1.dist`. Modifique o caminho dos arquivos `.bat` no final do script para que ele aponte para os locais corretos:

#### Exemplo de `create-task.ps1`
```ps1
Register-MultipleTasks -BatFilePath "C:\Scripts\start.bat" -TaskSchedules $taskSchedules
Register-DeleteLogsTask -BatFilePath "C:\Scripts\delete_logs.bat"
```

### Linux (cron)
Para agendar a execução dos scripts no Linux, utilizamos o `cron`. Crie os arquivos `start.sh` e `delete_logs.sh` com base nos exemplos `.dist`. Todos localizados no diretório `scripts/linux`

#### Exemplo de `start.sh`
> Certifique-se de ajustar os caminhos corretamente e garantir que os arquivos sejam executáveis.
```sh
#!/bin/bash

main_script="/path/to/main.py"
python_dir="/path/to/python"

$python_dir "$main_script"
```

Depois disso, torne os `.sh` executáveis
```sh
chmod +x /path/to/start.sh
chmod +x /path/to/delete_logs.sh
```

Por fim, abrir o `crontab` e adicionar no arquivo as tasks.

* Executar este comando no terminal
    ```sh
    crontab -e
    ```
* Abrir e colar o conteúdo do arquivo `create_tasks.sh.dist`. Lembar de modificar o caminho para o executável `.sh` para o caminho completo em sua máquina.
    ```sh
    # Executar script às 9:00 de segunda a sexta-feira
    0 9 * * 1-5 /path/to/your/start.sh

    # Executar script às 12:00 de segunda a sexta-feira
    0 12 * * 1-5 /path/to/your/start.sh

    # Executar script às 13:00 de segunda a sexta-feira
    0 13 * * 1-5 /path/to/your/start.sh

    # Executar script às 18:00 de segunda a sexta-feira
    0 18 * * 1-5 /path/to/your/start.sh

    # Executar script para limpar logs às 13:00 todo sábado
    0 13 * * 6 /path/to/your/delete_logs.sh
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
[notion]: https://www.notion.so/

<!-- [Constributors] -->
[arekushi]: https://github.com/Arekushi
