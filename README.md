# YORG AI

YORG AI connects large language model with Jupyter Notebook to complete versatile tasks. YORG AI provides a user-friendly, interactive way to understand existing codebases, write codes and documentation with the knowledge of the whole project, perform data analysis and generate complete reports, and more.

**License Notation**: YORG AI is constructed and distributed for personal and non-commercial use only. For commercial use of this project, please contact corresponding authors.

## Introduction

YORG AI provides a user-friendly platform that not only enhances code understanding and writing but also empowers users to perform data analysis and generate comprehensive reports effectively. With its interactive and guided approach, YORG AI is a robust tool for managing and navigating through diverse coding and data analysis projects.

## Features

- Turns feature request into codes and documentation based on the knowledge of the entire repository without an IDE.
- Interpret and extract insights from data, and turn them into complete reports.
- Chat with LLM models including OpenAI, Anthropic, and Hugging Face.

## Roadmap


## Installation
### Installation by Docker
Make sure you have Docker running and Run Command in terminal
- Build frontend and backend at the same time
```bash
docker-compose up --build
```

- Build frontend only
```bash
docker-compose up --build frontend
```

- Build backend only
```bash
docker-compose up --build backend
```

If you see: ``exec ./entrypoint.sh: no such file or directory``, try 
- **delete** the line ``entrypoint: ./entrypoint.sh in docker-compose.yml``
- **add** `CMD ["/bin/sh", "/app/entrypoint.sh"]` to the end of file `/backend/Dockerfile`
- rerun ``docker-compose up --build``

If you see: ``/app/entrypoint.sh: 3: set: Illegal option -``, try in console
- ``cd backend``
- ``sed -i 's/\r$//' entrypoint.sh`` 
- rerun ``docker-compose up --build``

### Usage
Go to http://localhost:8888/ and you will see a Jupyter Notebook.
- Create a new notebook with YKernel
- Wait until Ykernel is ready
- Click **+** next to the keyboard button to create a new cell to start
    - Software Engineer
    - OpenAI Chat
    - File Upload
    - Data Analysis
    - Python Code

