import json
import subprocess

try:
    with open('depotdownloader_file_path.txt', 'r') as f:
        depotdownloader_file_path = f.read().strip()
        if depotdownloader_file_path == "":
            raise FileNotFoundError
except FileNotFoundError:
    with open('depotdownloader_file_path.txt', 'w') as f:
        print("如果你的depotdownloader是通过包管理器安装的（如yay），则直接输入depotdownloader。否则输入绝对路径，无论系统。")
        depotdownloader_file_path = input("请输入depotdownloader文件路径：")
        f.write(depotdownloader_file_path)
else:
    print("depotdownloader_file_path:", depotdownloader_file_path)
    subprocess.run([depotdownloader_file_path, "--version"])

with open('key.json', 'r') as f:
    key = json.load(f)

