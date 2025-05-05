# ilab_script.py

import sys
import subprocess

def run_query(query):
    cmd = [
        "psql",
        "-h", "postgres.cs.rutgers.edu",
        "-U", "your_netid",             # 🔁 Replace with your NetID
        "-d", "your_database_name",     # 🔁 Replace with your database name
        "-c", query
    ]

    try:
        result = subprocess.run(cmd, text=True, capture_output=True, check=True)
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print("Error executing SQL:")
        print(e.stderr)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        query = sys.argv[1]
    else:
        query = sys.stdin.read()
    run_query(query)
