# H_RAG

Some RAG/GenAI related stuff.

## Requirements

- uv
- python

## Running the application

`uv run streamlit run src\h_rag\streamlit\main.py`

## Setup

Run `env_example cp .env`  
Replace relevant variables within `.env`

### Garage setup

With Garage's docker container running, run:
1. `docker exec -it garage /garage status`  
Copy the `ID` displayed
2. `docker exec garage /garage layout assign -z <arbitrary_zone_name> <ID> -c <Max_storage>`
3. `docker exec garage /garage layout apply --version 1`
4. `docker exec garage /garage bucket create hrag-bucket`
5. `docker exec garage /garage key create <key-name>`  
Store `Key ID` and `Secret key` in `.env`
6. `docker exec garage /garage bucket allow --read --write --owner <bucket-name> --key <key-name>`