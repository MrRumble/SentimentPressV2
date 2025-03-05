Documentation Overview
1. Introduction
Overview of the project and its purpose
Brief summary of how the system fetches, processes, and stores article data
2. Tech Stack
Programming languages and frameworks used
Database technologies
API integrations (e.g., NewsAPI)
Deployment plans (Amazon AWS goal)
3. System Architecture & Database
V1: Initially built using MongoDB (NoSQL)
Migration: Transitioned to PostgreSQL for more powerful SQL queries
Database Schema: Overview of tables and relationships
4. Data Processing Pipeline
Fetching article data
Cleaning and structuring data
Storing processed data in the database
5. Sentiment Analysis
Explanation of the sentiment analysis model used
Biases and potential drawbacks of the system
6. Features & Future Scalability
Potential for large-scale expansion using NewsAPI features (e.g., search by date, real-time news tracking)
Automatic data population scripts
Next Steps: Incorporating a User Service
7. UI & UX Considerations
Known Limitation: New search terms don’t load instantly onto the chart
Proposed Fix: Add a note to indicate that data is only available for previously searched terms due to limited API calls
8. Testing & CI/CD
Testing strategy and frameworks used
CI/CD setup in GitHub
Automated testing pipeline

Should have seperated the summarising and the sentiment scoring, currently processed at the same time causing lag.
Might have to introduce rate-limiting
