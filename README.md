# My RAG App

My RAG App is an AI-powered retrieval-augmented generation (RAG) application that indexes documents and allows users to interact with an AI agent to ask questions based on those documents. It leverages OpenAI's API along with libraries such as LangChain, PyPDF, ChromaDB, and others.

## Features

- **Document Indexing:** Automatically load, split, and embed text from provided PDF documents.
- **Interactive AI Agent:** Ask questions and get responses based on the indexed content.
- **Dockerized Application:** Build and run the application in a secure, minimal environment using a multi-stage Docker build.
- **Externalized Secrets:** The OpenAI API key is read from an environment variable, ensuring that sensitive information isn’t hard-coded.

## Prerequisites

- **Docker:** Ensure that Docker is installed and running on your machine.
- **OpenAI API Key:** Create an account at [OpenAI](https://platform.openai.com) and generate your API key.
- **Git:** (optional) To clone and manage the repository.

## Setup and Usage

### 1. Clone the Repository

If you haven't already cloned the repo, run:

```bash
git clone https://github.com/hsha/nka/simple-rag.git
cd my-rag-app
```

### 2. Build the Docker Image
```
docker build -t simple-rag .
```
This Dockerfile uses a multi-stage build:
	•	A builder stage using python:3.9-slim to compile and build wheels for required dependencies.
	•	A final stage using the secure Chainguard base image to run your application in a minimal environment.

### 3. Run the Application
```
docker run -it --rm -e OPENAI_API_KEY="your_openai_api_key_here" simple-rag
```
When the container starts, you should see output similar to:
```
Loading documents...
Splitting and embedding documents...
Documents successfully indexed.

AI Agent: Hello! I can answer questions based on your documents. Ask me anything!
You:
```

At that point, you can interact with the AI agent by typing your questions.


