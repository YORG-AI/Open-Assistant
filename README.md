# Y'ORG

![Overview](https://github.com/YORG-AI/YORG-AI/assets/20519290/86ed4e78-2fbe-4dee-81fc-eb503cae40b5)

Y'ORG connects large language model with Jupyter Notebook to complete various tasks. Y'ORG aims to provide a user-friendly, interactive way to (1) explore codebases, (2) draft implementation plans, (3) write codes and add new features. It also helps data scientists and analysts to (4) perform data analysis and (5) generate complete PhD-level reports. More features on the way!

**License Notation**: Y'ORG is constructed and distributed for personal and non-commercial use only. For commercial use of this project, please contact corresponding authors.

## Introduction

Y'ORG provides a user-friendly platform that not only enhances code understanding and writing but also empowers users to perform data analysis and generate comprehensive reports effectively -- with natural language! With its interactive and guided approach, YORG is a robust tool for managing and navigating through diverse coding and data analysis projects.

## Features

- Turns feature request into codes and documentation based on the knowledge of the entire repository without an IDE.
- Interpret and extract insights from data, and turn them into complete PhD-level reports.
  
## Roadmap


## Installation
### Add your API keys
- Add your API keys here:
```bash
backend/.env
```

backend/.env

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
 
## Contact

If you have any questions / feedback / comment, do not hesitate to contact us. 

Email: contact@yorg.ai

GitHub Issues: For more technical inquiries, you can also create a new issue in our GitHub repository.


