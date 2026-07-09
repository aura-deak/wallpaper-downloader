import sys
import json
import subprocess
import base64
import re
from pathlib import Path

def download(depotdownloader,pubfile,username,password,dir):

    if not dir.exists():
        dir.mkdir(parents=True)

    cmd = [
        depotdownloader,
        "-app", "431960",
        "-pubfile", pubfile,
        "-verify-all",
        "-username", username,
        "-password", password,
        "-dir", dir
    ]


    process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )

    for line in process.stdout:
        print(line)
    process.stdout.close()
    process.wait()

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

depotdownloader_exec_file_path = depotdownloader_config_file.read_text(encoding='utf-8')

print("depotdownloader_file_path:", depotdownloader_exec_file_path)
subprocess.run([depotdownloader_exec_file_path, "--version"])

pubfiles = []
while True:
    pubfile = input("请输入链接（输入q退出）：")
    if pubfile == "q":
        break
    pubfile = re.search(r'\b\d{8,10}\b', pubfile)
    if pubfile:
        pubfiles.append(pubfile.group())

keys = key_file.read_text(encoding='utf-8')
key_item = json.loads(keys)
for k,v in key_item.items():
    decoded_bytes = base64.b64decode(v)
    decoded_str = decoded_bytes.decode('utf-8')
    key_item[k] = decoded_str

username=""
passwd = ""
for pubfile in pubfiles:
    if username == "" or passwd == "":
        for u,p in key_item.items():
            download(
                depotdownloader=depotdownloader_exec_file_path,
                pubfile=pubfile,
                username=u,
                password=p,
                dir=Path(__file__).resolve().parent / "output"
            )
            if input("可以使用这个账号下载吗？(Y/n)") != "n":
                username = u
                passwd = p
                break
    else:
        download(
            depotdownloader=depotdownloader_exec_file_path,
            pubfile=pubfile,
            username=username,
            password=passwd,
            dir=Path(__file__).resolve().parent / "output"
        )
