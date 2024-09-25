import zipfile
import json
import os

from dotenv import load_dotenv

env_file = '.env'
load_dotenv()


# Функция для разбора списков из строки
def parse_list(env_value):
    return env_value.split(',') if env_value else []

# Функция для получения формата пакета по версии Minecraft
def get_pack_format(version):
    version_mapping = {
        "1.6.1-1.8.9": 1,
        "1.9-1.10.2": 2,
        "1.11-1.12.2": 3,
        "1.13-1.14.4": 4,
        "1.15-1.16.1": 5,
        "1.16.2-1.16.5": 6,
        "1.17-1.17.1": 7,
        "1.18-1.18.2": 8,
        "1.19-1.19.2": 9,
        "1.19.3": 12,
        "1.19.4": 13,
        "1.20-1.20.1": 15,
        "1.20.2": 18,
        "1.20.3-1.20.4": 22,
        "1.20.5-1.20.6": 32,
        "1.21-1.21.1": 32
    }

    for range_key, pack_format in version_mapping.items():
        start_version, end_version = range_key.split('-') if '-' in range_key else (range_key, range_key)
        if start_version <= version <= end_version:
            return pack_format

    return None

def get_supported_formats(versions):
    formats = []
    for version in versions:
        pack_format = get_pack_format(version)
        if pack_format is not None:
            formats.append(pack_format)
    return formats

# Получение данных из .env
minecraft_version = os.getenv("MINECRAFT_VERSION")
description = os.getenv("DESCRIPTION")
supported_versions = parse_list(os.getenv("SUPPORTED_VERSIONS"))
min_versions = parse_list(os.getenv("min_version"))
max_versions = parse_list(os.getenv("max_version"))
version_type = str(parse_list(os.getenv("VERSION_TYPE")))

include_language = os.getenv("INCLUDE_LANGUAGE") == 'True'
include_credits = os.getenv("INCLUDE_CREDITS") == 'True'
include_animation = os.getenv("INCLUDE_ANIMATION") == 'True'
include_textures = os.getenv("INCLUDE_TEXTURES") == 'True'
include_sounds = os.getenv("INCLUDE_SOUNDS") == 'True'

# Получение данных для языка
languages = parse_list(os.getenv("LANGUAGES"))
language_names = parse_list(os.getenv("LANGUAGE_NAMES"))
language_regions = parse_list(os.getenv("LANGUAGE_REGIONS"))
language_bidi = parse_list(os.getenv("LANGUAGE_BIDI"))

# Получение данных для кредитов
author = os.getenv("AUTHOR")
contributors = parse_list(os.getenv("CONTRIBUTORS"))
license = os.getenv("LICENSE")

# Получение данных для анимации
frame_time = int(os.getenv("FRAME_TIME", 10))
interpolate = os.getenv("INTERPOLATE") == 'True'

# Получение данных для текстур
block_textures = parse_list(os.getenv("BLOCK_TEXTURES"))
item_textures = parse_list(os.getenv("ITEM_TEXTURES"))
block_texture_paths = parse_list(os.getenv("BLOCK_TEXTURE_PATHS"))
item_texture_paths = parse_list(os.getenv("ITEM_TEXTURE_PATHS"))

# Получение данных для звуков
sound_categories = parse_list(os.getenv("SOUND_CATEGORIES"))
sound_names = parse_list(os.getenv("SOUND_NAMES"))
sound_paths = parse_list(os.getenv("SOUND_PATHS"))


# Получение формата пакета
pack_format = get_pack_format(minecraft_version)
if pack_format is None:
    print("Ошибка: Неверная версия Minecraft для определения формата пакета!")
    exit(1)


supported_formats = get_supported_formats(supported_versions)


pack_data = {
    "pack": {
        "pack_format": pack_format,
        "description": description,
        "supported_formats": supported_formats
        }
    }




# Добавляем поддержку языков, если она включена
if include_language:
    pack_data["language"] = {}
    for i in range(len(languages)):
        lang_key = languages[i]
        pack_data["language"][lang_key] = {
            "name": language_names[i],
            "region": language_regions[i],
            "bidirectional": language_bidi[i].lower() == 'true'
        }

# Добавляем кредиты, если они включены
if include_credits:
    pack_data["credits"] = {
        "author": author,
        "contributors": contributors,
        "license": license
    }

# Добавляем анимацию, если она включена
if include_animation:
    pack_data["animation"] = {
        "frame_time": frame_time,
        "interpolate": interpolate
    }

# Добавляем текстуры, если они включены
if include_textures:
    pack_data["textures"] = {
        "block": dict(zip(block_textures, block_texture_paths)),
        "item": dict(zip(item_textures, item_texture_paths))
    }

# Добавляем звуки, если они включены
if include_sounds:
    pack_data["sounds"] = {
        sound_categories[i]: {
            "name": sound_names[i],
            "path": sound_paths[i]
        } for i in range(len(sound_names))
    }

# Путь к файлу в папке, где находится скрипт
script_dir = os.path.dirname(os.path.abspath(__file__))  # Получаем путь к скрипту
file_path = os.path.join('pack.mcmeta')

# Запись данных в JSON файл
try:
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(pack_data, f, ensure_ascii=False, indent=4)
    print(f'Файл {file_path} успешно создан.')

except Exception as e:
    print(f'Ошибка при записи файла: {e}')



print("pack.mcmeta completen")
