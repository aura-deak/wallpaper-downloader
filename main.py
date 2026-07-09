import sys
import json
import subprocess
import base64
from pathlib import Path

try:
    depotdownloader_config_file = Path("depotdownloader_file_path.txt")
    key_file = Path("key.json")
    if depotdownloader_config_file.read_text(encoding='utf-8').split() == "":
        raise FileNotFoundError

except FileNotFoundError:
    print("如果你的depotdownloader是通过包管理器安装的（如yay），则直接输入depotdownloader。否则输入绝对路径，无论系统。")
    depotdownloader_exec_file_path = input("请输入depotdownloader文件路径：")
    depotdownloader_config_file.write_text(depotdownloader_exec_file_path,encoding='utf-8')
    print("请重启")
    sys.exit()

keys = key_file.read_text(encoding='utf-8')
key_item = json.loads(keys)
for k,v in key_item.items():
    decoded_bytes = base64.b64decode(v)
    decoded_str = decoded_bytes.decode('utf-8')
    key_item[k] = decoded_str

print("depotdownloader_file_path:", depotdownloader_file_path)
subprocess.run([depotdownloader_exec_file_path, "--version"])
