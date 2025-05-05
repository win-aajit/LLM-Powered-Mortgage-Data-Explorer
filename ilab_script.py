import sys
import subprocess

def run_query(query, netid):
    cmd = ["psql","-h", "postgres.cs.rutgers.edu","-U", netid, "-d", "group31", "-c", query]
    try:
        result = subprocess.run(cmd, text=True, capture_output=True, check=True)
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print("Error executing SQL:")
        print(e.stderr)
if __name__ == "__main__":
    if len(sys.argv) > 1:
        query = sys.argv[2]
        netid = sys.argv[1]
    else:
        query = sys.stdin.read()
    run_query(query,netid)
