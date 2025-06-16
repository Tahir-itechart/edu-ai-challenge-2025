import sys
import os
from typing import Optional, Dict
from dotenv import load_dotenv
import openai

MODEL_NAME = "gpt-4.1-mini"
PROMPT_TEMPLATE = (
    "You are an expert product analyst. Given the following service or product, generate a concise, markdown-formatted report with the following sections: "
    "\n- Brief History: Founding year, milestones, etc."
    "\n- Target Audience: Primary user segments"
    "\n- Core Features: Top 2–4 key functionalities"
    "\n- Unique Selling Points: Key differentiators"
    "\n- Business Model: How the service makes money"
    "\n- Tech Stack Insights: Any hints about technologies used"
    "\n- Perceived Strengths: Mentioned positives or standout features"
    "\n- Perceived Weaknesses: Cited drawbacks or limitations"
    "\nEach section should be clearly labeled as a markdown heading (## Section Name)."
    "\nIf information is not available, state 'Not enough public information.'"
)

def get_input() -> str:
    """Prompt the user for service name or description."""
    print("Enter a known service name (e.g., 'Spotify', 'Notion') or paste a raw service description. Press Enter when done:")
    lines = []
    while True:
        try:
            line = input()
            if line.strip() == '' and lines:
                break
            lines.append(line)
        except EOFError:
            break
    return '\n'.join(lines).strip()

def prompt_output_mode() -> str:
    """Prompt the user to select output mode."""
    output_mode = ''
    while output_mode not in ['1', '2']:
        print("Choose output mode:")
        print("1. Print report to console")
        print("2. Write report to file")
        output_mode = input("Enter 1 or 2: ").strip()
    return output_mode

def prompt_filename() -> str:
    """Prompt the user for a filename."""
    filename = input("Enter filename to save report (e.g., output.md): ").strip()
    if not filename:
        print("No filename provided. Exiting.", file=sys.stderr)
        sys.exit(1)
    return filename

def generate_report_with_openai(system_prompt: str, user_content: str, api_key: str) -> str:
    """Generate a report using OpenAI's chat completion API."""
    client = openai.OpenAI(api_key=api_key)
    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_content}
            ],
            max_tokens=900,
            temperature=0.7,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error generating report: {e}", file=sys.stderr)
        return f"**Error generating report:** {e}"

def analyze_service(service_info: str, api_key: str) -> Dict[str, str]:
    """Analyze the service and return the markdown report."""
    analysis = generate_report_with_openai(PROMPT_TEMPLATE, service_info, api_key)
    return {"service": service_info, "report": analysis}

def generate_markdown_report(analysis_dict: Dict[str, str]) -> str:
    """Format the analysis as a markdown report."""
    report = [
        "# Service Analysis Report\n",
        analysis_dict["report"].strip(),
        ""
    ]
    return '\n'.join(report)

def main():
    """Main entry point for the application."""
    load_dotenv()
    api_key = os.getenv('TOKEN')
    if not api_key:
        print("OpenAI API token not found in .env as TOKEN. Exiting.", file=sys.stderr)
        sys.exit(1)

    output_mode = prompt_output_mode()
    filename: Optional[str] = None
    if output_mode == '2':
        filename = prompt_filename()

    service_info = get_input()
    if not service_info:
        print("No input provided. Exiting.", file=sys.stderr)
        sys.exit(1)
    print("\nGenerating AI-powered analysis. Please wait...\n")
    analysis = analyze_service(service_info, api_key)
    report = generate_markdown_report(analysis)

    if output_mode == '1':
        print("\n--- Markdown Report ---\n")
        print(report)
    else:
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(report)
            print(f"Report saved to {filename}")
        except Exception as e:
            print(f"Failed to save file: {e}", file=sys.stderr)

if __name__ == "__main__":
    main() 