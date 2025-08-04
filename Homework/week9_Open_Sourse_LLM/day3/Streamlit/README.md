Mistral AI Chatbot with Streamlit
This is a simple yet powerful chatbot application built with Streamlit, leveraging the Mistral AI API for large language model (LLM) capabilities. It allows for interactive conversations with a Mistral AI model, displaying responses in a real-time streaming fashion.

Features
Interactive Chat Interface: A user-friendly web interface powered by Streamlit's st.chat_input and st.chat_message components.

Mistral AI Integration: Communicates with the Mistral AI API to generate dynamic responses.

Streaming Responses: Utilizes st.write_stream for a smooth, character-by-character "typing" effect as the AI generates its reply.

Session State Management: Maintains conversation history using Streamlit's st.session_state, ensuring continuous dialogue.

Secure API Key Handling: Safely loads the Mistral AI API key from Streamlit's secrets.toml file.

Setup and Installation
Follow these steps to get your Mistral AI Chatbot up and running.

1. Prerequisites
Python 3.8+ installed on your system.

A Mistral AI API key. You can obtain one from the Mistral AI Platform.

2. Clone the Repository (or create your project directory)
If you're starting from scratch, create a new folder for your project:

Bash

mkdir mistral-chatbot
cd mistral-chatbot
3. Install Dependencies
It's highly recommended to use a virtual environment to manage dependencies.

Bash

# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows:
.\venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install required Python packages
pip install streamlit mistralai==0.4.2  # Pinning to 0.4.2 for compatibility with the provided code
Note: We are pinning the mistralai library version to 0.4.2 to ensure compatibility with the provided code, as newer versions might have breaking API changes.

4. Configure Your Mistral AI API Key
Streamlit uses a secrets.toml file to securely store sensitive information like API keys.

Create a folder named .streamlit (note the dot at the beginning) in your project's root directory:

Bash

mkdir .streamlit
Inside the .streamlit folder, create a file named secrets.toml:

.streamlit/secrets.toml
Open secrets.toml and add your Mistral AI API key:

Ini, TOML

MISTRAL_API_KEY = "YOUR_MISTRAL_API_KEY_HERE"
Replace "YOUR_MISTRAL_API_KEY_HERE" with your actual Mistral AI API key.

Running the Chatbot
Once you have completed all the setup steps:

Open your terminal or command prompt.

Navigate to your project's root directory (cd mistral-chatbot).

Ensure your virtual environment is activated.

Run the Streamlit application:

Bash

streamlit run mistral_chatbot.py
Streamlit will open the application in your default web browser. You can now interact with your Mistral AI Chatbot!

Troubleshooting
If you encounter issues, here are some common problems and solutions:

ModuleNotFoundError: No module named 'mistralai.types.chat' or similar:
This typically means the mistralai library version has changed its internal structure.

Solution: Ensure you've removed all explicit from mistralai.types.chat import ChatMessage lines from your code. The provided code assumes mistralai can convert dictionaries ({"role": ..., "content": ...}) into its internal ChatMessage objects automatically. Also, ensure you have exactly mistralai==0.4.2 installed.

streamlit.errors.StreamlitSecretNotFoundError: No secrets found.:
Streamlit cannot find your secrets.toml file.

Solution: Double-check that you have a folder named .streamlit (with a leading dot) directly inside your project directory, and inside it, a file named secrets.toml. Verify the content format (MISTRAL_API_KEY = "YOUR_KEY").

NotImplementedError: This client is deprecated.:
This indicates a version mismatch with the mistralai library.

Solution: As per the instructions, ensure you explicitly installed mistralai==0.4.2 using pip install mistralai==0.4.2 --force-reinstall. Newer versions might require a completely different API client syntax.

Raw JSON/Object Output in Chat (pydantic_core...ValidationError or similar):
The model is sending more than just raw text (e.g., internal thinking tokens, tool calls) and Streamlit is trying to display the raw object.

Solution: The provided get_mistral_response_content function is designed to robustly extract only the text parts from the MistralClient's stream, ignoring other metadata like thinking tokens or complex structured outputs. Ensure you have the latest version of the code provided in the mistral_chatbot.py file. If the issue persists, consider trying a simpler model (e.g., open-mistral-7b if compatible with 0.4.2, but it's older) to see if the output format is simpler.

Feel free to customize this README.md further with your own notes or additional features you might add!

Let me know if you'd like any adjustments or have more questions!



