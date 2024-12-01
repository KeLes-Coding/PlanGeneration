"""
PLAN 生成器
"""

import copy
import json
import os
from Agent.agents import Agent_Planner, Agent_Result
import config


class plan_generater:
    def __init__(self, message_number, query, query_message):
        # 接收 query 编号
        self.message_number = message_number
        # query
        self.query = query
        self.query_message = query_message

        self.message_planner = []
        self.message_results = []
        self.message_total = []

    # Agent 初始化
    def AgentInit(self):
        agents = [Agent_Planner("Planner"), Agent_Result("Result")]
        return agents

    """
        信息处理模块
    """

    # Planner 打印器
    def PlannerJsonPrinter(self, json_data):
        formatted_json = {
            "GlobalThought": json_data["GlobalThought"],
            "OrderSteps": {
                "TotalSteps": json_data["OrderSteps"]["TotalSteps"],
                "StepDetail": {
                    "StepNumber": json_data["OrderSteps"]["StepDetail"]["StepNumber"],
                    "Description": json_data["OrderSteps"]["StepDetail"]["Description"],
                    "Action": json_data["OrderSteps"]["StepDetail"]["Action"],
                },
            },
        }
        self.message_planner.append(formatted_json)
        return formatted_json

    # Result 打印器
    def ResultJsonPrinter(self, json_data):
        formatted_json = {
            "OrderSteps": {
                # "TotalSteps": json_data["OrderSteps"]["TotalSteps"],
                "StepDetail": {
                    "StepNumber": json_data["OrderSteps"]["StepDetail"]["StepNumber"],
                    "Description": json_data["OrderSteps"]["StepDetail"]["Description"],
                    "Action": json_data["OrderSteps"]["StepDetail"]["Action"],
                    "Results": json_data["OrderSteps"]["StepDetail"]["Results"],
                },
            },
        }
        self.message_results.append(formatted_json)

        # 将 "Results" 拼接到相同 StepNumber 的 "OrderSteps" 中形成该 StepNumber 的 message_total
        messages_total = copy.deepcopy(self.message_planner[-1])
        messages_total["OrderSteps"]["StepDetail"]["Results"] = json_data["OrderSteps"][
            "StepDetail"
        ]["Results"]
        self.message_total.append(messages_total)
        return formatted_json

    """
        文件保存模块
    """

    # 文件保存函数
    def message_save(self):
        self.message_planner_save()
        self.message_results_save()
        self.message_total_save()
        print("文件保存成功！")

    # message_planner 保存到文件
    def message_planner_save(self):
        # 确保目录存在，如果不存在则创建
        json_data = config.JSON_DATA
        directory = f"{json_data}/{self.message_number}"
        if not os.path.exists(directory):
            os.makedirs(directory)

        file_name = self.message_number + "-message_planner.json"
        file_path = os.path.join(directory, file_name)

        data = {"MessageNumber": self.message_number, "Query": self.query_message}

        formatted_planner = []
        formatted_planner.append(data)
        for json_str in self.message_planner:
            formatted_planner.append(json_str)
        with open(file_path, "w") as json_file:
            json.dump(formatted_planner, json_file, indent=4)

    # message_results 保存到文件
    def message_results_save(self):
        # 确保目录存在，如果不存在则创建
        json_data = config.JSON_DATA
        directory = f"{json_data}/{self.message_number}"
        if not os.path.exists(directory):
            os.makedirs(directory)

        file_name = self.message_number + "-message_results.json"
        file_path = os.path.join(directory, file_name)

        data = {"MessageNumber": self.message_number, "Query": self.query_message}

        formatted_results = []
        formatted_results.append(data)
        for json_str in self.message_results:
            formatted_results.append(json_str)
        with open(file_path, "w") as json_file:
            json.dump(formatted_results, json_file, indent=4)

    # message_total 保存到文件
    def message_total_save(self):
        # 确保目录存在，如果不存在则创建
        json_data = config.JSON_DATA
        directory = f"{json_data}/{self.message_number}"
        directory_2 = f"{json_data}/message_total"
        if not os.path.exists(directory):
            os.makedirs(directory)
        if not os.path.exists(directory_2):
            os.makedirs(directory_2)

        file_name = self.message_number + "-message_total.json"
        file_path = os.path.join(directory, file_name)
        file_path_2 = os.path.join(directory_2, file_name)

        data = {"MessageNumber": self.message_number, "Query": self.query_message}

        formatted_total = []
        formatted_total.append(data)
        for json_str in self.message_total:
            formatted_total.append(json_str)
        with open(file_path, "w") as json_file:
            json.dump(formatted_total, json_file, indent=4)
        with open(file_path_2, "w") as json_file:
            json.dump(formatted_total, json_file, indent=4)

    """
        对话生成模块
    """

    # 对话生成器
    def PlanGenerater(self):
        # agents 初始化
        agents = self.AgentInit()

        # 第一个Agent(Planner)获取query，开始第一步规划
        ai_response = agents[0].interact(self.query)
        json_data = json.loads(ai_response)
        TotalSteps = json_data["OrderSteps"]["TotalSteps"]
        print(f"总步骤数：{TotalSteps}")
        ai_response_json = self.PlannerJsonPrinter(json_data)
        print(f"{agents[0].name}:")
        print(json.dumps(ai_response_json, indent=4))

        # 开始代理之间的对话：
        while True:
            # 当前代理的响应作为下一个代理的输入
            next_agent = agents[1]

            # 根据next_agent.name划分角色
            # 当角色为 Planner 是，将上一个代理 Result 的 Results 传输给 Planner
            if next_agent.name == "Planner":
                # ai_response初始化为json格式
                ai_response_json = json.loads(ai_response)
                # 获取当前代理的Results
                ai_response_Results = ai_response_json["OrderSteps"]["StepDetail"][
                    "Results"
                ]
                ai_response_step = ai_response_json["OrderSteps"]["StepDetail"][
                    "StepNumber"
                ]
                next_input = f"The execution result of step {ai_response_step} is:\n {ai_response_Results}\n Next, proceed to step {ai_response_step + 1}"
                print(next_input)
                ai_response = next_agent.interact(next_input)
                # 打印当前代理的响应
                ai_response_json = self.PlannerJsonPrinter(json.loads(ai_response))
                print(f"{next_agent.name}:")
                print(json.dumps(ai_response_json, indent=4))
            # 当角色为 Result 是，将上一个代理 Planner 的 Action 传输给 Result
            elif next_agent.name == "Result":
                # ai_response初始化为json格式
                ai_response_json = json.loads(ai_response)
                # 获取当前代理的Action
                ai_response_Action = ai_response_json["OrderSteps"]["StepDetail"][
                    "Action"
                ]
                ai_response_step = ai_response_json["OrderSteps"]["StepDetail"][
                    "StepNumber"
                ]
                # 将Results作为下一个代理的输入
                if ai_response_step == 1:
                    user_input = f"{ai_response_Action}\n Next, proceed to step {ai_response_step}'s result"
                    next_input = config.MESSAGE_RESULT[0] + user_input
                    # next_input = message_Result[0] + user_input
                else:
                    next_input = f"The execution Action of step {ai_response_step} is:\n {ai_response_Action}\n Next, proceed to step {ai_response_step}'s result"
                print(next_input)
                ai_response = next_agent.interact(next_input)
                # 打印当前代理的响应
                # 使用正则表达式匹配前后是否有 ```json 和 ```
                ai_response_json = self.ResultJsonPrinter(json.loads(ai_response))
                print(f"{next_agent.name}:")
                print(json.dumps(ai_response_json, indent=4))
                # 获取到 Result 的 Response 后，需要获取其 StepNumber 如果 StepNumber = TotalSteps 则退出循环
                step_number = json.loads(ai_response)["OrderSteps"]["StepDetail"][
                    "StepNumber"
                ]
                if step_number == TotalSteps:
                    print("生成结束！")
                    self.message_save()
                    break

            # 切换agent
            agents.reverse()
