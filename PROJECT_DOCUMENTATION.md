# 📚 TalentScout Project Documentation

## 1. Executive Summary
TalentScout is a containerized, AI-powered hiring assistant designed to automate initial technical screening. It interacts with candidates in real-time, adapting its questions based on their disclosed tech stack (e.g., Python, Django, SQL) and persisting interview transcripts for human review.

## 2. System Architecture

### High-Level Overview
The application follows a simple monolithic architecture wrapped in Docker.

```mermaid
graph TD
    User[Candidate] -->|Input| Streamlit[Streamlit Frontend]
    Streamlit -->|Logic Check| Utils[Utils Helper Logic]
    Utils -->|Keywords| TechStack[Tech Stack Detection]
    Utils -->|Save| Persistence[File System (JSON)]
    Streamlit -->|Context + Prompt| GroqAPI[Groq AI Inference]
    GroqAPI -->|Response| Streamlit
    subgraph Docker Container
        Streamlit
        Utils
    end
    subgraph Host Machine
        Persistence -->|Mount| DataVolume[./data/interviews]
    end
```

### Key Components
1.  **Frontend/Backend (`app.py`)**: A Streamlit application that handles the UI rendering and orchestration of the conversation flow.
2.  **Logic Layer (`utils.py`)**: Contains stateless business logic for:
    -   Detecting keywords (tech stack steering).
    -   Handling interaction signals ("exit", "bye").
    -   Persisting data to JSON.
3.  **AI Engine**: Uses **Groq Cloud API** (`llama-3.3-70b-versatile`) for LLM inference.
4.  **Persistence Layer**: A Docker volume mount that maps `/app/data` inside the container to `./data` on the host machine.

## 3. Data Flow

1.  **Initialization**:
    -   Application starts and initializes the Groq client (cached via `@st.cache_resource`).
    -   Session state (`messages` list) is created if empty.

2.  **Interaction Loop**:
    -   User types a message.
    -   **Tech Detection**: `utils.get_tech_stack_note` scans input. If "Python" is found, a system instruction is appended to the context: *"[System: Ask specific questions about Python generators...]"*.
    -   **Response Generation**: The user input + conversation history + system prompts are sent to Groq.
    -   **Display**: The AI response is appended to the session state and displayed.

3.  **Termination & Save**:
    -   User types "exit".
    -   `utils.save_interview` dumps the `messages` list to `data/interviews/interview_TIMESTAMP.json`.
    -   Session terminates.

## 4. Environment & Configuration

| Variable | Description | Required | Default |
| :--- | :--- | :--- | :--- |
| `GROQ_API_KEY` | API Key for Groq Cloud | Yes | None |
| `PORT` | Port for Streamlit app | No | 8501 |

## 5. Directory Structure

```text
/
├── app.py              # Application Entry Point
├── utils.py            # Business Logic & Helpers
├── prompts.py          # LLM System Prompts
├── requirements.txt    # Python Dependencies
├── Dockerfile          # Container Definition
├── docker-compose.yml  # Orchestration Config
├── Makefile            # Command shortcuts
└── data/               # HOST MOUNTED VOLUME
    └── interviews/     # JSON Transcripts
```

## 6. Future Roadmap

-   [ ] **Database Integration**: Migrate from JSON files to PostgreSQL for structured candidate storage.
-   [ ] **RAG Implementation**: Upload resumes (PDF) and have the AI ask questions based on specific resume content.
-   [ ] **Admin Dashboard**: A separate view for recruiters to browse and score transcripts.
-   [ ] **Voice Interface**: Add Speech-to-Text (STT) and Text-to-Speech (TTS) for voice interviews.
