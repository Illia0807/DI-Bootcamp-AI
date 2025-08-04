import streamlit as st
from mistralai.client import MistralClient

st.title("Mistral AI Chatbot Clone")

# Получаем API-ключ Mistral из Streamlit secrets
try:
    client = MistralClient(api_key=st.secrets["MISTRAL_API_KEY"])
except KeyError:
    st.error("Mistral API key not found in .streamlit/secrets.toml. Please add it.")
    st.stop() # Останавливаем выполнение приложения, если ключа нет

# Устанавливаем модель Mistral по умолчанию
if "mistral_model" not in st.session_state:
    # Используй актуальную модель из документации Mistral AI, например, "magistral-small-latest"
    st.session_state["mistral_model"] = "magistral-small-latest"

# Инициализируем историю чата
if "messages" not in st.session_state:
    st.session_state.messages = []

# Отображаем сообщения из истории чата при каждом запуске приложения
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Принимаем ввод пользователя
if prompt := st.chat_input("What is up?"):
    # Добавляем сообщение пользователя в историю чата
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Отображаем сообщение пользователя в контейнере чата
    with st.chat_message("user"):
        st.markdown(prompt)

    # Отображаем ответ ассистента в контейнере чата
    with st.chat_message("assistant"):
        # Формируем список сообщений для API Mistral как обычные словари
        messages_for_mistral = [
            {"role": m["role"], "content": m["content"]}
            for m in st.session_state.messages
        ]

        # Вызываем API Mistral для получения потокового ответа
        stream = client.chat_stream(
            model=st.session_state["mistral_model"],
            messages=messages_for_mistral,
        )

        # Функция-генератор для извлечения текстового контента из потока Mistral
        def get_mistral_response_content(mistral_stream):
            for chunk in mistral_stream:
                if chunk.choices[0].delta.content is not None:
                    yield chunk.choices[0].delta.content

        # Отображаем ответ по мере его поступления и сохраняем полный ответ
        full_response_content = st.write_stream(get_mistral_response_content(stream))

    # Добавляем полный ответ ассистента в историю чата (ОДИН РАЗ)
    st.session_state.messages.append({"role": "assistant", "content": full_response_content})