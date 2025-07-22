# CSV Q/A ChatBot POC

## Introduction

This project is a Proof of Concept (POC) for a CSV Question & Answering ChatBot. It's a web-based application built with Streamlit that allows users to upload a CSV file and interact with the data through a chat interface. The chatbot leverages the power of Large Language Models (LLMs) through LangChain to understand and answer questions about the uploaded data. It can provide textual answers, sliced dataframe and generate data visualizations in the form of Plotly charts.

## Features

- **CSV File Upload**: Users can easily upload their CSV files through a simple web interface.
- **Interactive Chat Interface**: A user-friendly chat interface to ask questions about the data in natural language.
- **Dual LLM Support**: The application supports two powerful LLMs for processing queries through API keys:
    - OpenAI's GPT models
    - Google's Gemini models
- **Data Visualization**: Capable of generating Plotly charts and graphs based on user prompts for visualizing the data.
- **Custom Styling**: A custom-styled chat interface for a better user experience.
- **Error Handling**: Includes error handling for issues like missing API keys and code execution errors.

## Requirements

The project relies on the following Python libraries:

- `streamlit`: For building the web application and user interface.
- `pandas`: For data manipulation and analysis.
- `tabular`: For working with tabular data.
- `plotly`: For creating interactive data visualizations.
- `openai`: Python client for the OpenAI API.
- `langchain`: For building applications with LLMs.
- `langchain-community`: Community-contributed components for LangChain.
- `langchain-experimental`: Experimental components for LangChain.
- `langchain-google-genai`: LangChain integration for Google's Generative AI models.
- `python-dotenv`: For managing environment variables.
- `ChatGoogleGenerativeAI`: Python client for the Gemini API.

## Tools

- **Python**: The core programming language used for the project.
- **Visual Studio Code**: The recommended IDE for development.
- **Git & GitHub**: For version control and repository management.

## Tech Stack

- **Frontend**: Streamlit
- **Backend/Core Logic**: Python
- **Data Handling**: pandas
- **LLM Orchestration**: LangChain
- **LLM Providers**: OpenAI, Google AI
- **Visualization**: Plotly
