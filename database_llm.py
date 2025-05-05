import paramiko
from getpass import getpass
from llama_cpp import Llama

def get_llm_response(prompt, llm):
    result = llm(prompt, max_tokens=200, stop=["\n"])
    return result['choices'][0]['text']

def extract_sql(text):
    for line in text.strip().splitlines():
        if line.strip().lower().startswith("select"):
            return line.strip().rstrip(";") + ";"
    return None

def send_query_over_ssh(sql, ssh_host, username, password):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(ssh_host, username=username, password=password)
    print("connected")
    command = f'python3 ilab_script.py {username} "{sql}"'
    stdin, stdout, stderr = client.exec_command(command)
    print(command)
    print("executed")
    output = stdout.read().decode()
    error = stderr.read().decode()
    print("response")
    client.close()
    return output, error

def main():
    llm = Llama.from_pretrained(repo_id="bartowski/Phi-3.5-mini-instruct-GGUF", filename="Phi-3.5-mini-instruct-IQ2_M.gguf",)
    #llm = Llama(model_path="Phi-3.5-mini-instruct-Q4_K_M.gguf")

    ssh_host = "basic.cs.rutgers.edu"
    ssh_user = input("NetID: ")
    ssh_pass = getpass("iLab password: ")

    with open("schema_prompt.sql") as f:
        schema = f.read()

    while True:
        question = input("\nAsk a question (or type 'exit'): ")
        if question.strip().lower() == "exit":
            break

        prompt = f"""Write a SELECT SQL query for the following schema and question:

SCHEMA:
{schema}

QUESTION:
{question}

SQL:"""
        llm_output = get_llm_response(prompt, llm)
        sql = extract_sql(llm_output)

        if sql:
            print(f"\n[SQL Query]: {sql}")
            result, err = send_query_over_ssh(sql, ssh_host, ssh_user, ssh_pass)
            print(result if not err else err)
        else:
            print("Could not extract SQL from LLM output.")

if __name__ == "__main__":
    main()
