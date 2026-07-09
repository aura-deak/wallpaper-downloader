import sys
import json
import subprocess
import base64
import re
from pathlib import Path

def init():
    print("如果你的depotdownloader是通过包管理器安装的（如yay），则直接输入depotdownloader。否则输入绝对路径，无论系统。")
    depotdownloader_exec_file_path = input("请输入depotdownloader文件路径：")

    config = {
        "depotdownloader_file_path": depotdownloader_exec_file_path,
        "username": "",
        "password": ""
    }

    config_file.write_text(json.dumps(config, indent=4), encoding='utf-8')
    print("请重启")

def get_pubfiles_from_input():
    pubfiles = []
    while True:
        pubfile = input("请输入链接/ID（可以连续输入，输入q退出）：")
        if pubfile == "q":
            break
        pubfile = re.search(r'\b\d{8,10}\b', pubfile)
        if pubfile:
            pubfiles.append(pubfile.group())
    return pubfiles

def unbase64passwd(keys):
    key_item = json.loads(keys)
    for k,v in key_item.items():
        decoded_bytes = base64.b64decode(v)
        decoded_str = decoded_bytes.decode('utf-8')
        key_item[k] = decoded_str
    return key_item

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
    config_file = Path("config.json")

    config = json.loads(config_file.read_text(encoding='utf-8'))
    depotdownloader_exec_file_path = config["depotdownloader_file_path"]
    # 如果第一次经过这里，则username和password为""
    username = config["username"]
    passwd = config["password"]

    key_file = Path("key.json")
    keys = key_file.read_text(encoding='utf-8')

except FileNotFoundError:
    init()
    sys.exit()

pubfiles = get_pubfiles_from_input()
key_item = unbase64passwd(keys)
for pubfile in pubfiles:
    if username == "" or passwd == "":
        for u,p in key_item.items():
            # 先尝试下载，如果可以成功，则后续下载项目直接使用
            # username和passwd为可用账号。u和p存放临时账号进行实验
            # 如果发现u和p可行，则更新username和passwd
            download(
                depotdownloader=depotdownloader_exec_file_path,
                pubfile=pubfile,
                username=u,
                password=p,
                dir=Path(__file__).resolve().parent / "output" / pubfile
            )
            if input("可以使用这个账号下载吗？(Y/n)") != "n":
                username = u
                passwd = p
                config["username"] = username
                config["password"] = passwd
                config_file.write_text(json.dumps(config, indent=4), encoding='utf-8')
                break
    else:
        download(
            depotdownloader=depotdownloader_exec_file_path,
            pubfile=pubfile,
            username=username,
            password=passwd,
            dir=Path(__file__).resolve().parent / "output" / pubfile
        )
