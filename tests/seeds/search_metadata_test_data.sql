-- Drop the table if it exists
DROP TABLE IF EXISTS search_metadata CASCADE;

-- Create the updated search_metadata table
CREATE TABLE search_metadata (
    search_metadata_id SERIAL PRIMARY KEY,
    user_id INT,
    search_term VARCHAR(255) NOT NULL,
    searched_at TIMESTAMP DEFAULT NOW()
);

-- Insert some test data
INSERT INTO search_metadata (user_id, search_term, searched_at)
VALUES
    (1, 'test search term 1', '2025-01-28 14:30:00'),
    (2, 'test search term 2', '2025-01-28 15:00:00'),
    (1, 'test search term 3', '2025-01-28 16:15:00'),
    (3, 'test search term 4', '2025-01-29 10:45:00'),
    (2, 'test search term 5', '2025-01-29 11:30:00');