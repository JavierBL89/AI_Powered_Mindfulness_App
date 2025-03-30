1. Prerequisites
API Key: You'll need an API key from OpenAI to access GPT-3. Sign up for OpenAI if you don’t already have an account.

# Install OpenAI's Python Library: Run:

   pip install openai


Run this curl command in a terminal to generate a haiku for free using the gpt-4o-mini model.


curl https://api.openai.com/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer OPENAI_API_KEY" \
  -d '{
    "model": "gpt-4o-mini",
    "store": true,
    "messages": [
      {"role": "user", "content": "write a haiku about ai"}
    ]
  }'

  curl https://api.openai.com/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <autho_barer_api>" \
  -d '{
    "model": "gpt-4o-mini",
    "store": true,
    "messages": [
      {"role": "user", "content": "write a haiku about ai"}
    ]
  }'

PYTHON
  from openai import OpenAI

client = OpenAI(
  api_key=OPENAI_API_KEY"
)

completion = client.chat.completions.create(
  model="gpt-4o-mini",
  store=True,
  messages=[
    {"role": "user", "content": "write a haiku about ai"}
  ]
)

print(completion.choices[0].message);