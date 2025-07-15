# RAG Chatbot with Ollama (Local LLM & Embeddings)

This project demonstrates a basic **Retrieval-Augmented Generation (RAG)** system implemented in Python. It leverages **Ollama** to run Large Language Models (LLMs) and embedding models **locally** on your machine, eliminating the need for cloud APIs or external services for inference.

The RAG pipeline works as follows:

1.  **Data Loading:** Facts about cats are loaded from a `cat-facts.txt` file, serving as our knowledge base.
2.  **Vector Database Creation:** Each fact is converted into a numerical **embedding** using a local embedding model (powered by Ollama's `bge-base-en-v1.5-gguf`). These embeddings, along with their corresponding text chunks, are stored in a simple in-memory "vector database."
3.  **Information Retrieval:** When a user asks a question, the query is also embedded. The system then calculates the **cosine similarity** between the query embedding and all fact embeddings to find the most **semantically relevant** chunks of information.
4.  **Augmented Generation:** The retrieved relevant facts are then used to **augment the prompt** sent to a local LLM (powered by Ollama's `Llama-3.2-1B-Instruct-GGUF`). This ensures the LLM's response is grounded in the provided factual context, reducing hallucinations and improving relevance.

This setup provides a powerful way to build intelligent, context-aware AI applications that can access and synthesize information beyond their initial training data, all while keeping model inference and data local.

## How to Run Locally

1.  **Install Ollama:** Follow the instructions at [ollama.com](https://ollama.com/) for your operating system.
2.  **Download Models:** In your terminal, pull the required models:
    ```bash
    ollama pull hf.co/CompendiumLabs/bge-base-en-v1.5-gguf
    ollama pull hf.co/bartowski/Llama-3.2-1B-Instruct-GGUF
    ```
    _(Note: Ensure the model names in `demo.py` match exactly what you see with `ollama list`)_
3.  **Install Python Client:**
    ```bash
    pip install ollama
    ```
4.  **Place Files:** Save `demo.py` and `cat-facts.txt` (which you can get [here](https://raw.githubusercontent.com/mlflow/mlflow-docs/master/docs/llms/llm-evaluate/notebooks/RAG/cat-facts.txt)) in the same directory.
5.  **Run:** Open your terminal, navigate to the directory where you saved the files, and run:
    ```bash
    python demo.py
    ```
    The chatbot will prompt you to ask a question.

**Example Query:** `How fast can a cat run?`
