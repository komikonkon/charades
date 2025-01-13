import json
import os
import sys
from pathlib import Path

# カレントディレクトリパス
BASE_DIR = os.path.dirname(__file__)
# BASE_DIR = Path(sys.executable).resolve().parent    # exe化用

# JSONファイル読み込み
json_file = open(BASE_DIR + '/settings.json', 'r', encoding='utf-8')
JSON_DATA = json.load(json_file)
