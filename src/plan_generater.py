"""
PLAN 生成器
"""

import json
from Agent.agents import Agent_Planner, Agent_Result
import config


class plan_generater:
    def __init__(self, query):
        self.query = query

    # Agent 初始化
    def AgentInit(self):
        agents = [Agent_Planner("Planner"), Agent_Result("Result")]
        return agents

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
        return formatted_json

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
                    break

            # 切换agent
            agents.reverse()
