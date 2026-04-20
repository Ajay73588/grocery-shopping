# Precision Architect - AI Report Agent

## Project Overview
Precision Architect is a FastAPI-powered web app that researches a topic, synthesizes a structured report using the MiniMax model, and generates a downloadable `.docx` file with embedded images.

## Prerequisites
- Python 3.11+
- pip
- Outbound internet access (for web research and image downloads)

## Setup
1. Create a `.env` file in the project root:
   ```
   MINIMAX_API_KEY=your_key_here
   ```
2. Install dependencies:
   ```
   python -m pip install -r requirements_minmax.txt
   ```

## Run the Web App
```
python -m uvicorn app:app --reload
```
Open the UI at:
```
http://127.0.0.1:8000/
```

## Usage (UI)
1. Enter a report topic.
2. Provide an output filename (no extension needed; `.docx` is added automatically).
3. Confirm or edit the model ID (default is `MiniMax-M2.7`).
4. Click **Execute Generation** to generate the report.
5. Preview the report and download the `.docx`.

## Output Files
Generated reports are saved to the `output/` folder and can also be downloaded from the UI.

## Troubleshooting
- **Missing API key**: If you see `MINIMAX_API_KEY environment variable not set.`, verify the `.env` file exists in the project root and contains a valid key.
- **Pylance missing imports**: Ensure VS Code is using the same Python interpreter where dependencies are installed (e.g., `Python 3.11`). Use `Python: Select Interpreter` in the command palette.
- **Image embed failures**: Some image URLs may be blocked, invalid, or return non-image content. Check the server logs for the failing URL and retry with a different topic or network.
