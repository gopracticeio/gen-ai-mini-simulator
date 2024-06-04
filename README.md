# GoPractice GenAI for Product Managers – Mini Simulator

This repository contains notebooks and code used in the [GenAI Mini Simulator](https://gopractice.io/course/genai/).
It is published mainly for illustrative purposes, not intended for any production use.

## What's inside

There are five notebooks that illustrate the steps of review analysis pipeline.
We try to keep them simple and do not use any frameworks

### How to start 
- Run `pip install -r requirements.txt` to install necessary libraries
- Input your OpenAI token in `run_ctx = RunCtx("<YOUR_TOKEN>")` cells
- Notebooks use `gpt-3.5-turbo` by default to avoid excessive costs
- Notebooks use small samples by default to avoid excessive costs
- Intermediate data is saved and can be inspected
- Run notebooks sequentially for 0 to 4

### Fetching reviews
Notebook: [0_fetch_reviews.ipynb](./src/0_fetch_reviews.ipynb)
Here we use a slightly patched `app_store_scraper` library to download a sample of app reviews

### Extracting topics and sentiments
Notebook: [1_extract_topics_and_sentiments.ipynb](./src/1_extract_topics_and_sentiments.ipynb)
Here we execute a pipeline for topic and sentiment extraction

### Categorizing topics
Notebook: [2_categorize_topics.ipynb](./src/2_categorize_topics.ipynb)
Here we execute a pipeline for finding main topic categories

### Mapping topics to the categories
Notebook: [3_map_topics_to_categories.ipynb](./src/3_map_topics_to_categories.ipynb)
Here we execute a pipeline to map topic into category

### Analyzing the results
Notebook: [4_analyze_results.ipynb](./src/4_analyze_results.ipynb)
Here we visualize the results of review analysis

## License

This project is licensed under the terms of the MIT License.

