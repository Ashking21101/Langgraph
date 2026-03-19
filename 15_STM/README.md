0. Keep Running Docker in background throughout
1. create Postgres DB using Docker-compose
2. "docker compose up -d"
3. check it by "docker ps"


4. run these (very imp)
    4.1. import sys
         !{sys.executable} -m ensurepip --upgrade
    4.2. !{sys.executable} -m pip install -U langgraph langgraph-checkpoint-postgres "psycopg[binary,pool]" langchain-openai