# Smart Product Assistant

A sleek, AI-powered conversational web application that helps users get detailed information and reviews about various products. Built with Python and Flask, this application leverages a modern glassmorphism UI to provide an engaging and interactive user experience.

## Features

- **Conversational Interface:** Natural language interactions for general queries.
- **Product Reviews & Info:** Ask for product specifications, price details, and review summaries, neatly formatted using Markdown and tables.
- **Modern UI:** A beautiful, responsive glassmorphism design with dynamic gradients and smooth animations.
- **Secure API Key Management:** Utilizes environment variables to keep sensitive configuration safe.

## Prerequisites

- Python 3.8+
- [Google Gemini API Key](https://aistudio.google.com/app/apikey)

## Installation

1. Clone the repository:
   ```bash
   git clone <repository_url>
   cd "Product Review Aggregator"
   ```

2. Create a virtual environment and activate it:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows, use: .venv\Scripts\activate
   ```

3. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   - Copy `.env.example` to `.env`:
     ```bash
     cp .env.example .env
     ```
   - Open `.env` and replace the placeholder with your actual Gemini API Key:
     ```
     GEMINI_API_KEY=your_api_key_here
     ```

## Usage

Start the Flask development server:

```bash
python main.py
```

Open your web browser and navigate to `http://127.0.0.1:5000` to start chatting with the Smart Product Assistant.

## Technologies Used

- **Backend:** Flask (Python)
- **AI Integration:** Google GenAI SDK
- **Frontend:** HTML, CSS (Glassmorphism), Vanilla JavaScript (Marked.js, DOMPurify)
