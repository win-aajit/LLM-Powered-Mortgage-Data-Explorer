CS336 Project 2 Group 31 Readme 

Group Members: Gilad Bejarano (gb534), Ashwin Ajit (aa2484), Pranav Ambulkar (pa468)

Overall this project was the most challenging out of the three. We found it challenging to integrate the LLM with the sql script. Throughout the project, we were facing errors with the LLM due to issues with the download, it was very difficult to overcome this and we had to consult ChatGPT in order to find solutions for this issue. We ended up opting for an LLM through Open Router called Qwen: Qwen3 1.7B (free). Additionally, we found it somewhat challenging to perfect the query sent to the LLM. It was also fairly challenging to integrate the ilab database into this program and make sure that the database is populated with information as for some reason it was not before, however we were able to solve these issues quickly and without any assistance from external sources, simply debugging. Overall we found it interesting how the LLM was able to create SQL queries only from natural language, and looking at the database's schema. We did not do the extra credit, however the code successfully fulfills all other requirements. The three questions we tested on were: "How many mortgages have a loan value greater than the applicant income?", "What is the average income of owner occupied applications?", and "What sex has the highest average loan amount and what is that amount?". This project uses paramiko, getpass as recommended in the instructions. It also uses Qwen3 from OpenRouter which was discovered upon research of free LLM APIs, it also uses python requests and json libraries which we had prior knowledge on.

Submitted files:
readme.txt (this file)
populate_db.sql (sql script used to populate the database with all relevant data, assumed original csv file is in working directory)
database_llm.py (locally run file which handles llm and ssh tunneling)
ilab_script.py (run on ilab machine, queries database and returns response to database_llm.py)
schema_subset.sql (schema of the database to be fed to the LLM to give context for better SQL queries)

References:
ChatGPT (all chat transcript screenshots included in submission) for help with configuring the LLM as well as explaining the instructions more simply.
LLM API: https://openrouter.ai/qwen/qwen3-1.7b:free/api
