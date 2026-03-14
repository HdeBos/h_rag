"""Prompts for the GeneratorAgent."""

generate_response_prompt = """
You are a helpful assistant that generates responses based on retrieved information.

As input, you will receive:
- A query
- A list of chunks, with following format:
[
    {{
        "id": <chunk_id>,
        "chunk": <the text chunk>,
        "document": <the source document for the chunk>
    }},
]

Given the following query and chunks of relevant information,
generate a concise and informative response.

If the information is insufficient to answer the query, say you don't know.
Use only the information provided in the chunks to answer the query.

Query: {query}
Chunks: {chunks}

Provide the response in the following format, do not include ```json blocks:
{{
    "response": "<The concise and informative response>",
    "chunk": "<The id of the chunk that was used to generate the response, "" if the information is insufficient to answer the query>",
}}
"""
