-- Drop the table if it exists
DROP TABLE IF EXISTS search_results CASCADE;

-- Create the updated search_results table
CREATE TABLE search_results (
    search_result_id SERIAL PRIMARY KEY,
    search_term VARCHAR(255),
    mean_sentiment DECIMAL(5, 2),
    positive_article_count INT,
    negative_article_count INT,
    total_article_count INT,
    ratio_positive_vs_negative DECIMAL(5, 2),
    main_headline VARCHAR(4000),
    top_3_articles JSONB,
    bottom_3_articles JSONB,
    created_at TIMESTAMP DEFAULT NOW() -- New single timestamp column
);

-- Insert some test data
INSERT INTO search_results 
    (search_term, mean_sentiment, positive_article_count, negative_article_count, 
     total_article_count, ratio_positive_vs_negative, main_headline, 
     top_3_articles, bottom_3_articles)
VALUES
    ('test search term 1', 0.7, 5, 3, 10, 1.67, 'Main Headline 1', 
     '[{"title": "Top Article 1", "url": "https://example.com/1"}, 
       {"title": "Top Article 2", "url": "https://example.com/2"}, 
       {"title": "Top Article 3", "url": "https://example.com/3"}]',
     '[{"title": "Bottom Article 1", "url": "https://example.com/11"}, 
       {"title": "Bottom Article 2", "url": "https://example.com/12"}, 
       {"title": "Bottom Article 3", "url": "https://example.com/13"}]'
    ),
    ('test search term 2', -0.3, 2, 8, 10, 0.25, 'Main Headline 2', 
     '[{"title": "Top Article 1", "url": "https://example.com/4"}, 
       {"title": "Top Article 2", "url": "https://example.com/5"}]',
     '[{"title": "Bottom Article 1", "url": "https://example.com/14"}, 
       {"title": "Bottom Article 2", "url": "https://example.com/15"}]'
    ),
    ('test search term 3', 0.9, 7, 2, 10, 3.5, 'Main Headline 3', 
     '[{"title": "Top Article 1", "url": "https://example.com/6"}, 
       {"title": "Top Article 2", "url": "https://example.com/7"}]',
     '[{"title": "Bottom Article 1", "url": "https://example.com/16"}]'
    );
