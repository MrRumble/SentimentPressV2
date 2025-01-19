# SentimentPress News Processing Pipeline

## Overview
This document describes the data processing workflow for news articles in the SentimentPress application.

## Processing Components

### 1. NewsFetcher (`news_fetcher.py`)
- **Responsibility**: Fetch raw news articles from NewsAPI
- **Key Functions**:
  - Retrieve articles based on query parameters
  - Use API key from `.env`
  - Support date range and language filtering

### 2. ArticleProcessor (`article_processor.py`)
- **Responsibility**: Process and analyze individual articles
- **Key Functions**:
  - Extract article metadata (title, description, date, source)
  - Perform sentiment analysis using Transformer pipeline
  - Validate article content
  - Transform articles into standardized format

### 3. ArticleSummariser (`article_summariser.py`)
- **Responsibility**: Summarize article collections
- **Key Functions**:
  - Generate summaries for top and bottom articles
  - Use text generation pipeline
  - Support advanced summarization with OpenAI (optional)

### 4. NewsProcessor ([news_processor.py](cci:7://file:///Users/rumble/SentimentPress/app/services/news_processor.py:0:0-0:0))
- **Responsibility**: Coordinate news processing workflow
- **Key Functions**:
  - Orchestrate article fetching and processing
  - Create and sort DataFrame of processed articles
  - Extract top and bottom articles by sentiment

### 5. QueryProcessor ([process_query.py](cci:7://file:///Users/rumble/SentimentPress/app/services/process_query.py:0:0-0:0))
- **Responsibility**: High-level query processing
- **Key Functions**:
  - Calculate sentiment metrics
  - Prepare data for frontend and database
  - Generate comprehensive query insights

### 6. SentimentAnalyser ([sentiment_analyser.py](cci:7://file:///Users/rumble/SentimentPress/app/services/sentiment_analyser.py:0:0-0:0))
- **Responsibility**: Perform statistical sentiment analysis
- **Key Functions**:
  - Calculate average sentiment
  - Count positive and negative articles
  - Compute sentiment ratio

## Typical Workflow
1. User submits a query
2. Fetch articles from NewsAPI
3. Process and analyze each article
4. Sort and filter articles
5. Generate insights and summaries
6. Prepare response for frontend

## Dependencies
- NewsAPI
- Transformers (Hugging Face)
- Pandas
- Optional: OpenAI GPT

## Best Practices
- Validate and clean article data
- Handle API rate limits
- Implement robust error handling
- Use efficient data structures

## Future Improvements
- Enhance summarization techniques
- Implement caching mechanisms
- Add more advanced sentiment analysis
- Support multiple languages