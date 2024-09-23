from utils.openai import OpenAIModel, OpenAIConfig
from utils.state import LocalState
import asyncio

class RunCtx(object):
    def __init__(self, openai_token, data_dir="../data"):
        self.openai_cfg = OpenAIConfig(openai_token, debug=False)
        self.model_gpt4o_mini = OpenAIModel("gpt-4o-mini", self.openai_cfg)
        self.model_gpt4 = OpenAIModel("gpt-4", self.openai_cfg)
        self.data_dir = data_dir
        self.state = LocalState(self.data_dir)

    async def run_async(self, pipeline, tasks, num_concurrent_requests=50):
        semaphore = asyncio.Semaphore(num_concurrent_requests)
        async def wrapper(t):
            async with semaphore:
                return await t

        tasks = [wrapper(pipeline(task)) for task in tasks]
        return await asyncio.gather(*tasks)
