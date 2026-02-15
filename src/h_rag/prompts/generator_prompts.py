"""Prompts for the GeneratorAgent."""

generate_response_prompt = """
You are a helpful assistant that generates responses based on retrieved information.

Given the following query and chunks of relevant information,
generate a concise and informative response.

If the information is insufficient to answer the query, say you don't know.

Query: ${query}
Chunks: ${chunks}
"""
