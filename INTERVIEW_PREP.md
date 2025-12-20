# 🎙️ TalentScout Project Analysis & Interview Q&A

## ⚡ Quick Summary (Elevator Pitch)
**TalentScout** is an intelligent, containerized hiring assistant built with **Python**, **Streamlit**, and the **Groq API**. It automates the initial technical screening process by dynamically generating interview questions based on a candidate's tech stack (e.g., Python, Django, SQL) and saving the transcript for review. It solves the problem of manual, repetitive screenings by providing an instant, 24/7 interactive assessment tool.

---

## 🧠 Technical Deep Dive: Interview Q&A

### 1. Architecture & Design
**Q: Can you walk me through the architecture?**
**A:** The app uses a simple client-server architecture wrapper in a container.
-   **Frontend/Backend:** Built with **Streamlit**, which handles both the UI and the Python logic in a single run loop.
-   **AI Engine:** Integrates with **Groq's API** (using the `llama-3.3-70b-versatile` model) for high-speed inference.
-   **State Management:** Uses `st.session_state` to maintain the chat history, as Streamlit apps re-run the entire script on every interaction.
-   **Persistence:** JSON transcripts are saved to a local volume mounted via Docker.

**Q: Why did you choose Groq over OpenAI or Gemini?**
**A:** We initially used Google Gemini but migrated to **Groq** for its superior latency (LPU architecture). For a real-time chat interface, the speed of token generation is critical for a natural "conversation" feel. It also offered a compatible `chat.completions` API (OpenAI-style), making the migration straightforward.

### 2. Implementation Details
**Q: How do you handle the conversation state?**
**A:** Since LLM REST APIs are stateless, we manually manage the conversation history list (`st.session_state.messages`). For every new user input, we append it to this list and send the *entire* history back to the API so the model maintains context.

**Q: How does the "Dynamic Tech Stack" feature work?**
**A:** I implemented a keyword detection layer in `utils.py`. Before sending the user's message to the AI, the code scans for keywords like "Python", "Django", or "SQL". If found, it injects a "system note" (hidden from the user) into the prompt instructions, explicitly telling the model to ask deeper questions about that specific topic.

**Q: You mentioned Docker. Why containerize a simple Python script?**
**A:** Docker ensures consistency ("works on my machine, works on yours"). It handles dependency isolation (Python versions, pip packages) and simplifies deployment. We use `docker-compose` to map the local `data/` directory to the container, ensuring interview transcripts persist even if the container is destroyed.

### 3. Challenges & Solutions
**Q: What was the hardest bug you faced?**
**A:** Handling the **Quota Exceeded** errors. We faced `429` rate limits with the initial Gemini model.
-   *Solution:* We implemented try-except blocks to catch `ClientError`, giving the user a friendly "Quota Exceeded" message instead of crashing the app. We eventually migrated to Groq which had better availability for our use case.

**Q: How did you fix the Streamlit "Client Closed" error?**
**A:** We ran into `RuntimeError: client has been closed` because Streamlit re-initializes objects on every run.
-   *Solution:* We used the `@st.cache_resource` decorator on the API client initialization. This tells Streamlit to create the client once and reuse it across reruns, keeping the connection alive.
