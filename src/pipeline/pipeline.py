from utils.openai import parse_json_response

def async_review_topic_pipeline(model, prompt_fn):
    async def _impl(r):
        res = await model.async_get_completion(prompt_fn(r))
        if res == "No topics":
            return []

        response = parse_json_response(res, raise_on_error=False, default_value=[])
        try:
            results = []
            for topic in response:
                if type(topic) != dict:
                    continue
                results.append({
                    "review_text": r["review"],
                    "topic": topic.get("topic_name", ""),
                    "sentiment": topic.get("sentiment", ""),
                    "explanation": topic.get("explanation", "")
                })
            return results
        except:
            import traceback
            print(traceback.format_exc())
    return _impl

def async_topic_categorization_pipeline(model, categorization_prompt_fn):
    async def _impl(topics):
        res = await model.async_get_completion(categorization_prompt_fn(topics))
        return parse_json_response(res, default_value={})
    return _impl

def async_topic_mapping_pipeline(model, categories, map_prompt_fn):
    async def _impl(r):
        res = await model.async_get_completion(map_prompt_fn(categories, r))
        if res == "No topics":
            return []

        return parse_json_response(res, default_value=[])
    return _impl
