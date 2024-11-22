"""
程序入口：
    * 按行读取message.txt中query
    * 每个query打开不同终端执行Query_Receive.py
"""

import json
import subprocess
import src.config as config


messages_list = []

# 读取message.txt 文件内容
with open(config.MESSAGE_PATH, "r") as file:
    messages_list = [line.strip().split("\n") for line in file.readlines()]

result_message = []

for i, message in enumerate(messages_list):
    combined_messages = []
    combined_messages = message[0]
    result_message.append(combined_messages)


def start_termainal(program_path, message):
    # 将 message 转换为 JSON 字符串
    message_json = json.dumps(message)
    # 使用 subprocess.Popen 来启动一个新的终端窗口并运行第二个程序，传递 message 作为参数
    subprocess.Popen(
        ["start", "cmd", "/k", "python", program_path, message_json], shell=True
    )


def main():
    program_path = config.PROGRAM_PATH

    for message in result_message:
        start_termainal(program_path, message)


if __name__ == "__main__":
    main()
