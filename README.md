# CSV Q/A ChatBot POC

## Project Overview

CSV Q/A ChatBot is a web-based application that enables users to upload CSV files and interact with their data through a conversational chat interface. Powered by Streamlit for the frontend and LangChain for LLM orchestration, the app supports natural language queries, data analysis, and visualization using OpenAI, Google Gemini, or Groq LLMs. The chatbot can answer questions, generate data slices, and create interactive Plotly charts based on user prompts.

---

## Directory Structure

```
TITANIC_PROJECT/
  ├── agents_handler/
  │   ├── __init__.py
  │   └── agents.py
  ├── custom_css/
  │   ├── __init__.py
  │   └── apply_custom_css.py
  ├── ui_components/
  │   ├── __init__.py
  │   ├── chat_analysis.py
  │   ├── data_preview.py
  │   ├── extras.py
  │   ├── file_loader.py
  │   ├── file_upload.py
  │   ├── header.py
  │   └── sidebar.py
  ├── main.py
  ├── requirements.txt
  ├── pyproject.toml
  └── README.md
```

---

## Module & File Descriptions

### main.py
- **Entry point of the application.**
- Initializes environment, session state, and applies custom CSS.
- Handles the main Streamlit layout: sidebar, header, file upload, data preview, and chat analysis tabs.
- Orchestrates the flow between UI components and backend logic.

### agents_handler/
- **agents.py**: Contains `get_dynamic_agent`, which dynamically creates a LangChain agent for a given DataFrame using the selected LLM (OpenAI, Gemini, or Groq). Handles API key management and agent instantiation, now supporting user-supplied keys from the sidebar.
- **__init__.py**: (empty, for package recognition)

### custom_css/
- **apply_custom_css.py**: Provides a function to inject custom CSS for styling the Streamlit app, including chat bubbles, cards, tabs, and file uploader.
- **__init__.py**: (empty)

### ui_components/
- **chat_analysis.py**: Implements the chat interface logic. Handles user/assistant/plot messages, processes user prompts, sends them to the LLM agent, parses responses, executes code for visualizations, and displays results. Ensures all analysis uses the uploaded DataFrame only.
- **data_preview.py**: Renders a tab for previewing the uploaded data and column statistics (types, unique values, missing values).
- **extras.py**: Displays feature cards highlighting the app's capabilities (natural language queries, AI-powered analysis, data visualization).
- **file_loader.py**: Provides the file uploader UI component for CSV files.
- **file_upload.py**: Handles file upload logic, reads CSVs into DataFrames, updates session state, and initializes the LLM agent. The uploader is now disabled until a valid API key is entered for the selected provider.
- **header.py**: Renders the main app header and description.
- **sidebar.py**: Implements the sidebar UI, allowing LLM provider selection, session info, dataset KPIs, and data clearing. Now includes advanced API key management and onboarding features (see below).
- **__init__.py**: (empty)

---

## API Key Management & User Experience

- **API Key Required**: Users must enter their own API key for the selected LLM provider (OpenAI, Gemini, or Groq) in the sidebar if no environment variable is set. The app will not allow data upload or chat until a valid key is provided.
- **Sidebar Enhancements**:
  - Status icon (success/warning) next to the API key input for the selected provider.
  - Masked display of the API key after entry, with a "Change" button to edit and a "Done Editing" button to confirm.
  - Provider-specific help links for obtaining an API key.
  - Info box on first load about API key privacy and usage.
  - "Reset Session" button to clear all data and API keys from the session.
- **File Upload Disabled**: The file uploader is disabled and a warning is shown until a valid API key is entered for the selected provider.
- **Privacy**: API keys are only stored in your browser session and are never sent to any server except the LLM provider. They are not persisted or shared.

---

## How It Works

1. **User selects an LLM provider** in the sidebar and enters their API key (if not set in environment variables).
2. The file uploader is enabled once a valid key is present.
3. The user uploads a CSV file, which is read into a pandas DataFrame, and a LangChain agent is created for the data using the selected LLM provider and API key.
4. The user can preview the data and column info in the "Data Preview" tab.
5. In the "Chat Analysis" tab, the user can ask questions or request visualizations in natural language.
6. The agent processes the prompt, analyzes the DataFrame, and returns either a textual answer or Python code for a Plotly chart.
7. If code is returned, it is executed in a sandboxed environment and the resulting chart is displayed.
8. All chat history and state are managed in Streamlit's session state.

---

## Usage Instructions

### 1. **Environment Setup**
- Install Python 3.10+ (recommended).
- Clone the repository:
  ```bash
  git clone https://github.com/Mabdullahatif/CSV-QA-ChatBot.git
  cd CSV-QA-ChatBot
  ```
- Install dependencies:
  ```bash
  pip install -r requirements.txt
  ```
- Set up your `.env` file with the following keys (optional, for default API key):
  ```env
  OPENAI_API_KEY=your_openai_key
  GOOGLE_API_KEY=your_gemini_key
  GROQ_API_KEY=your_groq_key
  ```

### 2. **Running the App**
```bash
streamlit run main.py
```

### 3. **Using the App**
- Select your preferred LLM provider in the sidebar.
- Enter your API key for the selected provider (if not set in environment variables). The sidebar will show a status icon and mask your key for privacy.
- The file uploader will be enabled once a valid key is present.
- Upload a CSV file.
- Explore your data in the "Data Preview" tab.
- Switch to "Chat Analysis" to ask questions or request visualizations.
- Use the "Reset Session" button in the sidebar to clear all data and API keys if needed.

---

## Features
- **CSV File Upload**: Upload and analyze any CSV file (enabled only after API key entry).
- **Interactive Chat**: Ask questions in natural language about your data.
- **Multi-LLM Support**: Choose between OpenAI, Gemini, or Groq for analysis.
- **Data Visualization**: Generate interactive Plotly charts from chat prompts.
- **Custom Styling**: Modern, user-friendly interface.
- **Robust Error Handling**: Handles missing keys, file errors, and code execution issues.
- **Advanced API Key Management**: Secure, user-friendly onboarding and privacy for API keys.

---

## API Key Privacy & Troubleshooting

- **Privacy**: Your API key is only used in your browser session and never sent to any server except the LLM provider. It is not stored or shared.
- **Troubleshooting**: If you see a warning about a missing or invalid API key, enter a valid key for the selected provider in the sidebar. The file uploader will remain disabled until a valid key is present.
- **Provider Links**:
  - [OpenAI API Keys](https://platform.openai.com/account/api-keys)
  - [Google Gemini API Keys](https://aistudio.google.com/app/apikey)
  - [Groq API Keys](https://console.groq.com/keys)

---

## Architecture Diagram

```
User
 │
 ▼
Streamlit UI (main.py, ui_components/)
 │
 ▼
File Upload → DataFrame (pandas)
 │
 ▼
LLM Agent (LangChain, agents_handler/)
 │
 ▼
LLM Provider (OpenAI, Gemini, Groq)
 │
 ▼
Response (Text/Code)
 │
 ▼
UI (Answer/Plot)
```

---

## Contributing

1. Fork the repo and create a new branch.
2. Make your changes with clear commit messages.
3. Ensure code is well-documented and tested.
4. Submit a pull request describing your changes.

---

## License

MIT License (add LICENSE file if not present)

---

## Acknowledgements
- [Streamlit](https://streamlit.io/)
- [LangChain](https://www.langchain.com/)
- [OpenAI](https://openai.com/)
- [Google Gemini](https://ai.google/discover/gemini/)
- [Groq](https://groq.com/)
- [Plotly](https://plotly.com/)

---

## Connect with Me
<p align="center">
    <a href="https://www.linkedin.com/in/mabdullahatif/">
        <img height="50" src="https://cdn2.iconfinder.com/data/icons/social-icon-3/512/social_style_3_in-306.png"/>
    </a>
    &nbsp;&nbsp;&nbsp;
    <a href="https://www.facebook.com/abdullahatif362/">
        <img height="50" src="https://cdn0.iconfinder.com/data/icons/social-flat-rounded-rects/512/facebook-64.png"/>
    </a>
    &nbsp;&nbsp;&nbsp;
    <a href="https://www.instagram.com/abdullah._.atif/">
        <img height="50" src="https://cdn2.iconfinder.com/data/icons/social-media-applications/64/social_media_applications_3-instagram-64.png"/>
    </a>
    &nbsp;&nbsp;&nbsp;
    <a href="https://www.twitter.com/abd_allah_atif/">
        <img height="50" src="https://cdn3.iconfinder.com/data/icons/2018-social-media-logotypes/1000/2018_social_media_popular_app_logo_twitter-64.png"/>
    </a>
</p>
