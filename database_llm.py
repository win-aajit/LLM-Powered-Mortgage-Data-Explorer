import subprocess
import paramiko
import getpass
from llama_cpp import Llama
import re

# === CONFIGURATION ===
MODEL_PATH = "Phi-3.5-mini-instruct-Q4_K_M.gguf"  # Replace with your actual model path
SCHEMA_FILE = "llm_schema_subset.sql"
ILAB_HOST = "ilab.rutgers.edu"
ILAB_SCRIPT_PATH = "python3 ilab_script.py"

# === Load the schema for the prompt ===
def load_schema():
    with open(SCHEMA_FILE, "r") as f:
        return f.read()

# === Build the prompt for the LLM ===
def generate_prompt(schema_text, user_question):
    return f"""You are a helpful SQL assistant.
Using the following database schema:

{schema_text}

Write a SQL SELECT query to answer this question:
{user_question}

Only output the SQL query and nothing else.
"""

# === Extract SQL query from LLM response ===
def extract_sql(response_text):
    # First try to extract from inside a ```sql ... ``` block
    match = re.search(r"```sql(.*?)```", response_text, re.DOTALL | re.IGNORECASE)
    if match:
        return match.group(1).strip()

    # Next try to find the first SELECT statement
    match = re.search(r"(SELECT\s.+?;)", response_text, re.IGNORECASE | re.DOTALL)
    if match:
        return match.group(1).strip()

    # Fallback to returning raw response
    return response_text.strip()

# === Connect to ILAB via SSH and run the SQL query ===
def run_query_over_ssh(query, username, password):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ILAB_HOST, username=username, password=password)

    # Escape quotes in query
    safe_query = query.replace('"', '\\"')

    command = f'{ILAB_SCRIPT_PATH} "{safe_query}"'
    stdin, stdout, stderr = ssh.exec_command(command)

    output = stdout.read().decode()
    error = stderr.read().decode()
    ssh.close()

    if error:
        print("[!] Error from ILAB script:")
        print(error)
    return output

# === Main Program Loop ===
def main():
    schema = load_schema()
    username = input("Enter your ILAB username: ")
    password = getpass.getpass("Enter your ILAB password (hidden): ")

    print("Loading local LLM... please wait")
    llm = Llama(model_path=MODEL_PATH)

    while True:
        question = input("\nAsk a question (or type 'exit'): ")
        if question.lower() == "exit":
            break

        prompt = generate_prompt(schema, question)
        print("\n[LLM Prompting...]\n")

        response = llm(prompt, max_tokens=200)
        llm_output = response["choices"][0]["text"]

        print("\n[Raw LLM Output]:")
        print(llm_output)

        sql_query = extract_sql(llm_output)
        print("\n[Extracted SQL Query]:")
        print(sql_query)

        if not sql_query.lower().startswith("select"):
            print("\n[!] Only SELECT queries are allowed. Try again.")
            continue

        print("\n[Querying ILAB server...]\n")
        result = run_query_over_ssh(sql_query, username, password)
        print("[Result from ILAB]:\n")
        print(result)

if __name__ == "__main__":
    main()
