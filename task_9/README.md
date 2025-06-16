# edu-ai-challenge-2025

## Project Overview

This project provides a lightweight console application that generates comprehensive, markdown-formatted reports for digital services or products. The report includes business, technical, and user-focused perspectives, and is powered by OpenAI's GPT-4.1-mini model.

## Features

- Accepts either a known service name or a raw description as input
- Produces a multi-section markdown report with:
  - Brief History
  - Target Audience
  - Core Features
  - Unique Selling Points
  - Business Model
  - Tech Stack Insights
  - Perceived Strengths
  - Perceived Weaknesses
- Output can be printed to the console or written to a file
- Uses OpenAI API for AI-driven analysis

## Setup Instructions

1. **Clone the repository and navigate to the project directory:**
   ```bash
   git clone <repo-url>
   cd edu-ai-challenge-2025/task_9
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Add your OpenAI API key to a `.env` file:**
   ```
   TOKEN=sk-...your_openai_api_key...
   ```

## Usage Instructions

Run the application:
```bash
python app.py
```
- Choose output mode: print the report to the console or write it to a file
- Enter a service name (e.g., `Spotify`) or paste a description
- View the generated markdown report in your terminal, or open the file you specified

## Sample Output

See `sample_outputs.md` for example reports.

## Configuration

- The OpenAI model and prompt template can be adjusted in `app.py`.
- The API key is read from the `.env` file.

## Dependencies

- Python 3.8+
- openai
- python-dotenv
