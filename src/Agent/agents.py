from openai import OpenAI
import os
import sys

sys.path.append("..")
import config

os.environ["HTTP_PROXY"] = "http://localhost:0789"
# 初始化 OpenAI 客户端
client = OpenAI(
    api_key=config.API_KEY,
    base_url=config.BASE_URL,
)
GlobalModel = config.GLOBAL_MODEL


class Agent:
    def __init__(self, name):
        self.name = name
        self.messages = []


# 定义代理类
class Agent_Planner(Agent):
    def __init__(self, name):
        self.name = name
        self.messages = []
        self.messages.append(
            {
                "role": "system",
                "content": """
    As a competent planner, you are able to skillfully call the APIs and app tools I provide to create a reasonable plan based on the queries I submit.
    Only one step is generated at a time.
    Please return the JSON data directly without using Markdown formatting.
    Your response template should be as follows:
     {
    "GlobalThought": {
        "type": "string",
        "maxLength": 300,
        "description": "A concise, strategic overview capturing the core planning approach and key objectives"
    },
    "OrderSteps": {
        "TotalSteps": {
            "type": "integer", 
            "min": 1, 
            "max": 20,
            "description": "The total number of planned sequential steps"
        },
        "StepDetail": {
            "StepNumber": {
                "type": "integer",
                "min": 1,
                "max": 20,
                "description": "The step number"
            },
            "Description": {
                "type": "string",
                "guidelines": [
                    "Start with a verb",
                    "Clearly state the purpose",
                    "Be specific and actionable",
                    "Limit to 100 characters"
                ]
            },
            "Action": {
                "type": "string",
                "pattern": "ToolName({'key': 'value'})"
            }
        }
    }
}
"example": 
    {
        "GlobalThought": "Develop a strategic plan to improve customer satisfaction by enhancing product quality and customer service.",
        "OrderSteps": {
            "TotalSteps": 3,
            "StepDetail": 
            {
                "StepNumber": 1,
                "Description": "Analyze current customer feedback",
                "Action": "FeedbackTool({'source': 'customer_surveys'})"
            }
        }
    }
""",
            }
        )

    def interact(self, message):
        # 将用户输入添加到消息列表
        self.messages.append({"role": "user", "content": message})

        # 调用 OpenAI API 获取响应
        response = client.chat.completions.create(
            model=GlobalModel,
            # model="qwen-plus",
            messages=self.messages,
            temperature=0,
            # response_format={"type": "json_object"},
        )

        # 获取并返回 AI 的响应
        ai_response = response.choices[0].message
        self.messages.append(ai_response)
        return ai_response.content


# 定义代理类
class Agent_Result(Agent):
    def __init__(self, name):
        self.name = name
        self.messages = []
        self.messages.append(
            {
                "role": "system",
                "content": """You are a meticulous API caller, characterized by the following:
Generate logical and realistic return values based on the tools/APIs you have.
Only one step is generated at a time.
Please return the JSON data directly without using Markdown formatting.
Your response template should be as follows:
Task Execution Template:
{
"OrderSteps": {
    "StepDetail": {
            "StepNumber": {
                "type": "integer",
                "min": 1,
                "max": 20,
                "description": "The step number"
            },
            "Description": {
                "type": "string",
                "guidelines": [
                    "Start with a verb",
                    "Clearly state the purpose",
                    "Be specific and actionable",
                    "Limit to 100 characters"
                ]
            },
            "Action": {
                "type": "string",
                "pattern": "ToolName({'key': 'value'})"
            }
            "Results": {
                "type": "string",
                "pattern": "ToolName({'key': 'value'})"
            }
        }
    }
}
"example": 
    {
        "OrderSteps": {
            "StepDetail": {
                "StepNumber": 2,
                "Description": "Enhance product quality through rigorous testing",
                "Action": "QualityAssuranceTool({'phase': 'testing'})",
                "Results": "QualityAssuranceTool({'status': 'completed'})"
            }
        }
    }
""",
            }
        )

    def interact(self, message):
        # 将用户输入添加到消息列表
        self.messages.append({"role": "user", "content": message})

        # 调用 OpenAI API 获取响应
        response = client.chat.completions.create(
            model=GlobalModel, messages=self.messages, temperature=0
        )

        # 获取并返回 AI 的响应
        ai_response = response.choices[0].message
        self.messages.append(ai_response)
        return ai_response.content
