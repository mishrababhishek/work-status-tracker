# Work Status Tracker

A Python application to automate the generation of professional daily work status emails by summarizing code changes from multiple Git repositories. The app uses LLMs (Large Language Models) to compose a well-formatted email based on the day's commits and diffs.

## Features
- Scans multiple Git repositories and branches for today's commits
- Summarizes commit messages and diffs (truncated for readability)
- Uses LLMs (DeepSeek, Groq, or others via LangChain) to generate a polished work status email
- Outputs the email to a text file for easy copy-paste or sending
- Modular, extensible, and well-logged for debugging

## Project Structure
```
├── src/
│   ├── app.py                # Main entry point
│   ├── tracker.py            # Gathers today's changes from configured repos
│   ├── email_generator.py    # Generates the work status email using LLM
│   └── utils/
│       ├── logger.py         # Structured logging utility
│       ├── model_manager.py  # LLM model selection and abstraction
│       └── settings.py       # Loads configuration from settings.json
├── settings.json             # Configuration for repos and models
├── requirements.txt          # Python dependencies
├── output/email.txt          # Generated email output
└── README.md                 # Project documentation
```

## Setup
1. **Clone the repository**
2. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```
3. **Configure your repositories and LLM API keys** in `settings.json`:
   - List your Git repositories and branches
   - Add your LLM provider API keys and select a default model

## Usage
Run the main application:
```sh
python src/app.py
```
- The app will scan the configured repositories for today's commits, generate a work status email, and save it to `output/email.txt`.

## Configuration (`settings.json`)
Example structure:
```json
{
  "repos": [
    {"path": "C:/path/to/repo1", "branch": "main"},
    {"path": "C:/path/to/repo2", "branch": "develop"}
  ],
  "models": [
    {"name": "Groq", "model_name": "llama3-70b-8192", "api_key": "YOUR_GROQ_API_KEY"},
    {"name": "DeepSeek", "api_key": "YOUR_DEEPSEEK_API_KEY"}
  ],
  "default_model": "Groq"
}
```

## Extending
- Add new LLM providers by extending `utils/model_manager.py`
- Adjust prompt templates in `email_generator.py`
- Add more logging or error handling as needed

## License
Apache-2.0