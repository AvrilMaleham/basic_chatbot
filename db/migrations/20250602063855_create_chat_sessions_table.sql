-- migrate:up
CREATE TABLE IF NOT EXISTS chat_sessions (
    id SERIAL PRIMARY KEY,
    session_id TEXT NOT NULL,
    message TEXT NOT NULL,
    role VARCHAR(50) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_chat_sessions_session_created_at ON chat_sessions(session_id, created_at);

-- migrate:down
DROP INDEX IF EXISTS idx_chat_sessions_session_created_at;
DROP TABLE IF EXISTS chat_sessions;