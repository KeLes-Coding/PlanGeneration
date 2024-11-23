"""
在此文件接收query并处理
"""

import copy
import json
import sys
from plan_generater import plan_generater
import config

message_Planner = config.MESSAGE_PLANNER
message_Result = config.MESSAGE_RESULT


def receive():
    # 从命令行参数中获取 message
    message_number = sys.argv[1]
    message_json = sys.argv[2]
    query_message = json.loads(message_json)

    # 打印message
    print("Received message:")
    print(message_number)
    print(query_message)
    print()

    # 拼接传输给 Planner 的 message
    combined_messages = copy.deepcopy(message_Planner)
    combined_messages = combined_messages[0] + query_message
    # combined_messages[-1]["content"] += query_message
    # 打印传输给 Planner 的 message
    print(combined_messages)
    print()

    executor = plan_generater(message_number, combined_messages, query_message)
    executor.PlanGenerater()


receive()
