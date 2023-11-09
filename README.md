# Y'ORG

Y'ORG AI provides a local implementation of OpenAI's assistant.

## Introduction
OpenAI's Assistant API is awesome: channeling the power of **Code interpreter** and **Retrieval** and thereby helping developers build powerful AI assistants capable of performing various tasks. However, it executes codes within an online sandbox and requires us to upload our files to OpenAI's platform -- which does not sound that awesome...

Y'ORG AI thus introduces the Open Assistant, which allows you to run your codes locally, retrieve knowledge from local files (without sendding them to OpenAI), and access more developer-friendly tools!

## Key Advantages
Our platform is designed with the developer and data analyst in mind, offering unparalleled advantages:

- **Fortified Data Privacy**: Your sensitive information never leaves your own secure servers.
- **Boundless Document Handling**: Wave goodbye to restrictions on file size or quantity.
- **Cost Efficiency**: Eliminate session and retrieval costs associated with cloud-based services.
- **Local LLM Flexibility**: Opt for the Large Language Model of your choice and maintain all operations in-house.

## Tools and pre-built assistants
Y'ORG provide additional tools for developers:
- Understand codebases.
- Draft development specification.
- Introduce new features into existing projects.

And for data analyst:
- Conduct data analysis.
- Create reports for diverse audiences.

We also provide pre-built assistants for our users:

**SDE assistant**: Transform feature requests into executable code and documentation by harnessing the collective intelligence of your entire code repository—no IDE required.

**Data assistant**: Analyze datasets, distill insights, and convert them into comprehensive reports for varied stakeholders.

## Roadmap
TBD (Your thoughts and suggestions are highly welcomed! Create an issue or email contact@yorg.ai)

## Installation
### Add your API keys
- Add your API keys here:
```bash
backend/.env
```

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
- Click ``+`` next to the keyboard button to create a new cell to start
    - Software Engineer
    - OpenAI Chat
    - File Upload
    - Data Analysis
    - Python Code
 
## Contact

If you have any questions / feedback / comment, do not hesitate to contact us. 

Email: contact@yorg.ai

GitHub Issues: For more technical inquiries, you can also create a new issue in our GitHub repository.


