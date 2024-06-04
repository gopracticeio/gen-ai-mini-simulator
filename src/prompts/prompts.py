from .base import Prompt

def make_extraction_prompt_v1(review):
    return Prompt(
        "You are a product manager who has to research user experience of your app",
        f"""
    Your task is to analyze a review and extract main topics (maximum 3 topics).
    For each topic extract related sentiment – positive/negative/neutral.

    Here is a text of a review.
    
    ===
    {review["review"]}
    ===
    
    Output a RAW json with format
    {{
        "topic_name": "sentiment", ...
    }}
    """)

def make_extraction_prompt_v2(review):
    return Prompt(
        "You are a product manager who has to research user experience of your app",
        f"""
        Your task is to analyze a review and extract main topics (maximum 3 topics).
        
        Each topic has to describe an exact feature or issue of the app.
        
        It should be actionable for a product manager.
        
        For each topic extract related sentiment – positive/negative/neutral.
        
        Sentiment has to be related to the user’s current sentiment; words such as "now" could describe the current sentiment.
        
        Here is a text of a review.
        ===
        {review["review"]}
        ===
           
        Solve this task step by step.
        Output a RAW json array with format
        [{{
            "explanation": "explain your decision here",
            "topic_name": "extracted_name",
            "sentiment": "extracted_sentiment"
        }}, ...]        
    """)

def make_categorization_prompt_v1(topics):
    instr = "\n".join(topics)
    return Prompt("You are a product manager who has to research user experience of your app", f"""
    Your task is to categorize a list of topics mentioned in user reviews.
    
    Here is a list of topics
    ===
    {instr}
    ===
    
    Please output only a RAW json of following structure:
    [
        "$topic_category_name", ...
    ]
    """)


def make_categorization_prompt_v2(topics):
    instr = "\n".join(topics)
    return Prompt("You are a product manager who has to research user experience of your app", f"""
    Your task is to extract main categories in a list of topics mentioned in user reviews.
    
    Category should be related to a single business feature.
    Categories must not intersect in meanings.
    
    Here is a list of topics
    ===
    {instr}
    ===
    
    Include each topic in a single category.
    
    Solve this problem step by step:
    - First extract major categories
    - Map each topic to a single best matching category
    
    Please output only a RAW json of following structure:
    {{
        "$topic_category_name": one-sentence summary of the category
    }}
    """)

def map_category_v1(categories, topic):
    import json

    return Prompt("You are a product manager who has to research user experience of your app", f"""
    Your task is to map a topic into one most suitable category from a given categories. 
    Use only the given list of categories.
    
    Here is a json with category names and their explanations 
    ===
    {json.dumps(categories, indent=4)}
    ===
    
    Here is a topic
    ===
    {topic}
    ===
    
    Solve this problem step by step.
    
    Please output only a RAW json of following structure:
    {{
        "$topic": "$category_from_list_above" 
    }}
    """)


