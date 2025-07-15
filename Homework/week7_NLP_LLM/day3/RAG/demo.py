# demo.py - полный код для запуска RAG с Ollama локально

import ollama
# from sentence_transformers import SentenceTransformer # Эта строка НЕ нужна, если используем ollama.embed()

# --- Настройка моделей ---
# Убедись, что эти модели загружены через 'ollama pull'
# Используй имена моделей, как они отображаются в Ollama после 'ollama list'
EMBEDDING_MODEL_NAME = 'hf.co/CompendiumLabs/bge-base-en-v1.5-gguf:latest' # <-- ИСПРАВЛЕНО
LANGUAGE_MODEL_NAME = 'hf.co/bartowski/Llama-3.2-1B-Instruct-GGUF:latest' # <-- ИСПРАВЛЕНО


# --- 1. Загрузка датасета ---
dataset = []
# Убедись, что cat-facts.txt находится в той же директории, что и demo.py
with open('cat-facts.txt', 'r') as file:
  dataset = file.readlines()
  print(f'Загружено {len(dataset)} записей.')


# --- 2. Реализация векторной базы данных ---
VECTOR_DB = []

def add_chunk_to_database(chunk):
  # Здесь мы используем ollama.embed напрямую, который обращается к локальному серверу Ollama
  # ollama.embed возвращает словарь, где вектор находится по ключу 'embedding'
  embedding = ollama.embed(model=EMBEDDING_MODEL_NAME, input=chunk)['embeddings'][0]
  VECTOR_DB.append((chunk, embedding))

print("\nНачинаем создание векторной базы данных...")
for i, chunk in enumerate(dataset):
  add_chunk_to_database(chunk)
  if (i + 1) % 10 == 0 or (i + 1) == len(dataset):
    print(f'Добавлено чанков: {i+1}/{len(dataset)}')

print(f'Векторная база данных создана. Всего {len(VECTOR_DB)} записей.')
if VECTOR_DB:
    print(f'Размерность эмбеддинга: {len(VECTOR_DB[0][1])}')


# --- 3. Реализация функции поиска ---
def cosine_similarity(a, b):
  # ollama.embed['embedding'] возвращает список чисел, поэтому np не нужен здесь
  dot_product = sum([x * y for x, y in zip(a, b)])
  norm_a = sum([x ** 2 for x in a]) ** 0.5
  norm_b = sum([x ** 2 for x in b]) ** 0.5
  if norm_a == 0 or norm_b == 0:
      return 0.0
  return dot_product / (norm_a * norm_b)

def retrieve(query, top_n=3):
  # Используем ollama.embed для запроса
  query_embedding = ollama.embed(model=EMBEDDING_MODEL_NAME, input=query)['embeddings'][0]
  similarities = []
  for chunk, embedding in VECTOR_DB:
    similarity = cosine_similarity(query_embedding, embedding)
    similarities.append((chunk, similarity))
  similarities.sort(key=lambda x: x[1], reverse=True)
  return similarities[:top_n]


# --- 4. Фаза генерации ---
input_query = input('Задайте мне вопрос о кошках: ') # Сделаем ввод интерактивным

retrieved_knowledge = retrieve(input_query)

print('\nНайденные знания:')
context_chunks = []
for chunk, similarity in retrieved_knowledge:
  chunk_text = chunk.strip()
  print(f' - (Сходство: {similarity:.4f}) {chunk_text}')
  context_chunks.append(chunk_text) # Просто текст чанка для промпта

# Конструируем инструкцию для LLM
instruction_prompt = f'''Ты полезный чатбот.
Используй ТОЛЬКО следующие фрагменты контекста для ответа на вопрос. Не придумывай новую информацию:
{'\n'.join([f' - {chunk}' for chunk in context_chunks])}
'''

print('\n--- Ответ чатбота ---')
# Используем ollama.chat для генерации ответа
stream = ollama.chat(
  model=LANGUAGE_MODEL_NAME,
  messages=[
    {'role': 'system', 'content': instruction_prompt},
    {'role': 'user', 'content': input_query},
  ],
  stream=True, # Включаем стриминг для вывода в реальном времени
)

for chunk in stream:
  print(chunk['message']['content'], end='', flush=True)

print("\n\nПрограмма завершена.")