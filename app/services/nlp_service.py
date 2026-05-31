from datetime import datetime
from app.schemas.nlp import TaskCommandParseResponse
from app.llm.llm import create_task_chain,query_task_chain,general_chain

class NLPService:

    CREATE_TASK = "create_task"
    QUERY_TASK = "query_task"
    UNKNOWN = "unknown"

    CREATE_KEYWORDS = [
        "创建任务",
        "新建任务",
        "建任务",
        "安排任务",
        "分配任务",
        "给",
        "安排",
        "创建",
        "新建",
        "建",
        "分配"
    ]

    QUERY_KEYWORDS = [
        "查询任务",
        "查任务",
        "查看任务",
        "看看任务",
        "查一下",
        "查询",
        "查看",
        "看看",
        "看",
        "查",
        "找",
        "找一下"
    ]



    def normalize_punctuation(self,text: str) -> str:
        """将中文标点转换为英文标点"""
        replacements = {
            "：": ":",   # 冒号
            "；": ";",   # 分号
            "，": ",",   # 逗号
            "。": ".",   # 句号
            "！": "!",   # 感叹号
            "？": "?",   # 问号
            "（": "(",   # 左括号
            "）": ")",   # 右括号
            "【": "[",   # 左方括号
            "】": "]",   # 右方括号
            "《": "<",   # 左书名号
            "》": ">",   # 右书名号
            "“": "\"",  # 左双引号
            "”": "\"",  # 右双引号
            "‘": "'",   # 左单引号
            "’": "'",   # 右单引号
            "…": "...", # 省略号
            "—": "-",   # 破折号
            "～": "~",  # 波浪号
        }

        for cn, en in replacements.items():
            text = text.replace(cn, en)
        return text

    def detect_intent(self, text: str):

        text = self.normalize_punctuation(text)

        query_prefixes = ( "查询任务",
        "查任务",
        "查看任务",
        "看看任务",
        "查一下",
        "查询",
        "查看",
        "看看",
        "看",
        "查",
        "找",
        "找一下")
        create_prefixes = (
        "创建任务",
        "新建任务",
        "建任务",
        "安排任务",
        "分配任务",
        "给",
        "安排",
        "创建",
        "新建",
        "建",
        "分配")

        if text.startswith(query_prefixes):
            return self.QUERY_TASK

        if text.startswith(create_prefixes):
            return self.CREATE_TASK

        if "创建的任务" in text and any(word in text for word in query_prefixes):
            return self.QUERY_TASK

        for word in self.CREATE_KEYWORDS:
            if word in text:
                return self.CREATE_TASK

        for word in self.QUERY_KEYWORDS:
            if word in text:
                return self.QUERY_TASK

        return self.UNKNOWN


    async def parse_create_task_command(self, text: str) -> TaskCommandParseResponse:
        """解析创建任务命令"""
        result = await create_task_chain.ainvoke({
            "current_time": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
            "text": text,
        })

        data = TaskCommandParseResponse.model_validate(result)

        return data

    async def parse_query_task_command(self, text: str) -> TaskCommandParseResponse:
        """解析查询任务命令"""
        result = await query_task_chain.ainvoke({
            "current_time": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
            "text": text,
        })

        data = TaskCommandParseResponse.model_validate(result)

        return data

    async def normal_parse_task_command(self, text: str) -> TaskCommandParseResponse:
        """普通解析任务命令"""
        result =await general_chain.ainvoke({
            "current_time": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
            "text": text,
        })

        data = TaskCommandParseResponse.model_validate(result)

        return data


    async def router(self,text: str):

        intent = self.detect_intent(text)

        if intent == self.CREATE_TASK:
            return await self.parse_create_task_command(text)

        elif intent == self.QUERY_TASK:
            return await self.parse_query_task_command(text)

        else:
            return await self.normal_parse_task_command(text)







