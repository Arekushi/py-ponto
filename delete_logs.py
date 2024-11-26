import asyncio
from config.config import settings, ROOT_DIR
from src.helpers.path_helper import delete_directory


LOG_DIR = settings.constants.dirs.logging


async def main():
    delete_directory(
        dir_path=f'{ROOT_DIR}/{LOG_DIR}'
    )


if __name__ == '__main__':
    asyncio.run(main())
