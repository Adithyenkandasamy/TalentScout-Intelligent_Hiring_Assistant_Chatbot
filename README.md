# 🤖 TalentScout: Intelligent Hiring Assistant

![TalentScout Banner](https://img.shields.io/badge/Status-Active-success)
![Python](https://img.shields.io/badge/Python-3.10+-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.32+-red)
![Groq](https://img.shields.io/badge/AI-Groq%20Llama%203-orange)

TalentScout is an intelligent chatbot designed to streamline the technical screening process. It engages candidates, identifies their tech stack, and generates tailored technical interview questions in real-time.

## ✨ Features

-   **Dynamic Tech Stack Detection**: Automatically identifies keywords (Python, Django, SQL, etc.) and steers the conversation to deeper technical topics.
-   **Conversation Persistence**: Automatically saves interview transcripts to `data/interviews/` when the session ends.
-   **Powered by Groq**: Utilizes the ultra-fast `llama-3.3-70b-versatile` model for instant responses.
-   **User Controls**: Clean sidebar interface to clear chat history or manually download transcripts.
-   **Dockerized**: Fully containerized for easy deployment.

## 🚀 Quick Start

### Prerequisites

-   Docker & Docker Compose
-   [Groq API Key](https://console.groq.com)

### Installation

1.  **Clone the repository** (if applicable) or navigate to the project directory.

2.  **Configure Environment**:
    Create a `.env` file in the root directory:
    ```bash
    GROQ_API_KEY=your_groq_api_key_here
    ```

3.  **Run with Docker**:
    We provide a `Makefile` for convenience.
    ```bash
    make docker-build
    make docker-up
    ```

    The application will be available at [http://localhost:8501](http://localhost:8501).

### Manual Setup (No Docker)

If you prefer running locally with Python:

```bash
# Install dependencies
make install

# Run the app
make run
```

## 📂 Project Structure

```
├── app.py              # Main Streamlit application
├── utils.py            # Helper functions (logic, saving)
├── prompts.py          # AI prompts & system instructions
├── requirements.txt    # Python dependencies
├── Dockerfile          # Docker configuration
├── docker-compose.yml  # Container orchestration
├── Makefile            # Automation shortcuts
└── data/               # Persistent data storage
    └── interviews/     # Saved interview transcripts
```

## 🛠️ Usage Guide

1.  **Start the Interview**: Open the app and introduce yourself.
2.  **Tech Screening**: Mention your skills (e.g., "I know Python and Django"). The bot will ask relevant technical questions.
3.  **End Session**: Type "exit" or "bye" to end the interview. The transcript acts as a record for the hiring team.
4.  **Download**: Use the "Download Transcript" button in the sidebar to get a JSON copy of the chat.

## 🤝 Contributing

Contributions are welcome! Please ensure you verify your changes using `make run` before submitting.

## 📄 License

[MIT License](LICENSE)