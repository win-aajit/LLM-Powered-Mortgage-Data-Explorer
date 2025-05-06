import paramiko
from getpass import getpass
import requests
import json

def get_llm_response(prompt):
    response = requests.post(
    url="https://openrouter.ai/api/v1/chat/completions",
    headers={
        "Authorization": "Bearer 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",
        "Content-Type": "application/json"
    },
    data=json.dumps({
        "model": "qwen/qwen3-1.7b:free",
        "messages": [
        {
            "role": "user",
            "content": prompt
        }
        ],
        
    })
    )
    return response.json()['choices'][0]['message']['content']

def extract_sql(text):
    lines = text.strip().splitlines()
    collecting = False
    sql_lines = []

    for line in lines:
        stripped = line.strip()
        if not collecting and stripped.lower().startswith("select"):
            collecting = True
        if collecting:
            sql_lines.append(stripped)
            if stripped.endswith(";"):
                break

    return " ".join(sql_lines) if sql_lines else None


def send_query_over_ssh(sql, ssh_host, username, password):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(ssh_host, username=username, password=password)
    command = f'python3 ilab_script.py {username} "{sql}"'
    stdin, stdout, stderr = client.exec_command(command)
    print(command)
    output = stdout.read().decode()
    error = stderr.read().decode()
    client.close()
    return output, error

def main():
    ssh_host = "basic.cs.rutgers.edu"
    ssh_user = input("NetID: ")
    ssh_pass = getpass("iLab password: ")

    with open("schema_prompt.sql") as f:
        schema = f.read()

    while True:
        question = input("\nAsk a question (or type 'exit'): ")
        if question.strip().lower() == "exit":
            break

        prompt = f"""Respond with only the SQL query, do not give any reasoning, do all thinking in your head. Write a SELECT SQL query for the following schema and question:

SCHEMA:
{schema}

QUESTION:
{question}

SQL:"""
        llm_output = get_llm_response(prompt)
        sql = extract_sql(llm_output)
        if sql:
            print(f"[SQL Query]: {sql}")
            result, err = send_query_over_ssh(sql, ssh_host, ssh_user, ssh_pass)
            print(result if not err else err)
        else:
            print("Error")

if __name__ == "__main__":
    main()
