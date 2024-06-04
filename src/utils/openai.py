import json
import math
import traceback
from time import sleep

import json5
import openai
from openai.error import RateLimitError, Timeout, APIError, ServiceUnavailableError, APIConnectionError


class OpenAIConfig(object):
    def __init__(self, api_key, max_retries=200, debug=False, timeout=30):
        self.api_key = api_key
        self.max_retries = max_retries
        self.debug = debug
        self.timeout = timeout

class OpenAIModel(object):
    def __init__(self, model, config):
        self.model = model
        self.config = config

    async def async_get_completion(self, prompt):
        cfg = self.config
        openai.api_key = cfg.api_key
        messages = prompt.to_messages()

        if cfg.debug:
            print(json.dumps(messages, indent=4))

        for attempt in range(cfg.max_retries):
            try:
                response = await openai.ChatCompletion.acreate(
                    model=self.model,
                    messages=messages,
                    temperature=0,  # this is the degree of randomness of the model's output
                    timeout=cfg.timeout
                )
                resp = response.choices[0].message["content"]
                if cfg.debug:
                    print(resp)
                return resp
            except (Timeout, APIError, ServiceUnavailableError, APIConnectionError) as e:
                sleep(0.001)
                if cfg.debug or (attempt > 0 and attempt % 10 == 0):
                    print(traceback.format_exc())
                if attempt == cfg.max_retries - 1:
                    raise e
                continue
            except RateLimitError as e:
                sleep(min(5., 0.05 * math.pow(2, attempt)))
                continue

def parse_json_response(response, raise_on_error=False, default_value=None):
    if response is None or not len(response.strip()):
        return default_value
    try:
        return json5.loads(response)
    except:
        c_start = "{" in response
        c_end = "}" in response
        b_start = "[" in response
        b_end = "]" in response
        resp_len = len(response)

        if (c_start and c_end) or (b_start and b_end):
            try:
                json_start = min(response.index("{") if c_start else resp_len, response.index("[") if b_start else resp_len)
                json_end = max(response.rindex("}") if c_end else -1, response.rindex("]") if b_end else -1)
                if json_start != -1 and json_end != -1:
                    sub_json = response[json_start:json_end + 1]
                    return json5.loads(sub_json)
                else:
                    if raise_on_error:
                        raise Exception("Broken json: %s" % response)
            except:
                if raise_on_error:
                    raise Exception("Broken sub json: %s" % response)
                else:
                    print("Broken sub json: %s" % response)
        if raise_on_error:
            raise Exception("Broken json: %s" % response)
    return default_value
