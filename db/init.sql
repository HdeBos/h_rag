CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE knowledge_base (
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE NOT NULL
);

CREATE TABLE document (
    id SERIAL PRIMARY KEY,
    title TEXT,
    checksum BYTEA UNIQUE
);

CREATE TABLE knowledge_base_document (
    knowledge_base_id INTEGER REFERENCES knowledge_base(id) ON DELETE CASCADE,
    document_id INTEGER REFERENCES document(id) ON DELETE CASCADE,
    PRIMARY KEY (knowledge_base_id, document_id)
);

CREATE TABLE chunk (
    id SERIAL PRIMARY KEY,
    document_id INTEGER REFERENCES document(id) ON DELETE CASCADE,
    content TEXT,
    embedding VECTOR(768),
    page_number INTEGER
);
