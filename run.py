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
with open("message.txt", "r") as file:
    messages_list = []
    for line in file:
        parts = line.strip().split("\t", 1)  # 使用制表符分割编号和内容
        if len(parts) == 2:
            number, content = parts
            messages_list.append((int(number), content))

numbers = [item[0] for item in messages_list]
contents = [item[1] for item in messages_list]

numbers_message = []
result_message = []

for number, content in zip(numbers, contents):
    numbers_message.append(number)

    combined_messages = []
    combined_messages = content
    result_message.append(combined_messages)


def start_termainal(program_path, number, message):
    # 将 message 转换为 JSON 字符串
    message_json = json.dumps(message)
    # 使用 subprocess.Popen 来启动一个新的终端窗口并运行第二个程序，传递 message 作为参数
    subprocess.Popen(
        ["start", "cmd", "/k", "python", program_path, str(number), message_json],
        shell=True,
    )


def main():
    program_path = config.QUERY_RECEIVE

    for number, message in zip(numbers_message, result_message):
        start_termainal(program_path, number, message)


if __name__ == "__main__":
    main()
