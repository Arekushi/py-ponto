from pathlib import Path
from dynaconf import Dynaconf

settings = Dynaconf(
    load_dotenv=True,
    envvar_prefix=False,
    merge_enabled=True,
    settings_files=[
        './yaml/settings.yaml',
        './yaml/xpath.yaml',
        './yaml/notion.yaml',
        './yaml/.secrets.yaml',
    ]
)

ROOT_DIR = Path(__file__).parent.parent

# `envvar_prefix` = export envvars with `export DYNACONF_FOO=bar`.
# `settings_files` = Load these files in the order.
