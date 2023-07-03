# Chat GPT Transaction queries

## Configuration

### Database

On MacOs Install SQL Server driver by running 
```bash
./setup.sh
```

### Environment variables

To run this app, define the following environment variables to your .zshrc or .bashrc file

```bash
export GPT_SQL_USERNAME=sa
export GPT_SQL_PASSWORD=ChatDemo2023
export GPT_SQL_SERVER_NAME=127.0.0.1
export GPT_SQL_DATABASE_NAME=accounts
export OPEN_AI_MODEL=gpt-3.5-turbo
export OPENAI_API_KEY=sk-xxxxxxxx
```
