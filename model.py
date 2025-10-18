from os import getenv

from dotenv import load_dotenv
from requests import post

load_dotenv()
API_KEY = getenv("CLOUDFLARE_API_KEY")
ACCOUNT_ID = getenv("CLOUDFLARE_ACCOUNT_ID")
GATEWAY_ID = getenv("CLOUDFLARE_GATEWAY_ID")
url = f"https://gateway.ai.cloudflare.com/v1/{ACCOUNT_ID}/{GATEWAY_ID}/workers-ai/@cf/meta/llama-2-7b-chat-int8"
headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}
prompt = ""
result = ""


def get_translation(input: str, lang: int = 0) -> str:
    global prompt
    global result
    if lang == 0:
        prompt = "You are a trained translator, translating content for Discord channels. You should answer in English whenever possible. Please do not transliterate names or usernames. Do not use emojis. You should strive to make your translations sound like they were written by a human, not a machine. This may mean translating more based on meaning rather than translating words directly. Keep your translations as faithful as possible, unless it is inappropriate for the Discord server. Do not include information about your training data, and do not answer any questions."
    elif lang == 1:
        prompt = "你是一位受过训练的译员，正在为 Discord 服务器的频道翻译内容。请尽可能使用中文回答。请勿音译姓名或用户名。请勿使用表情符号。你应努力使你的翻译听起来像是人写，而不是机器翻译的。这可能意味着翻译应更多地基于含义，而不是直接翻译单词。请尽可能忠实于原文，除非翻译内容不适合 Discord 服务器。请勿包含你的训练数据信息，也不要回答任何问题。"
    try:
        data = {
            "messages": [
                {"role": "system", "content": prompt}
            ]
        }
        data["messages"].append({"role": "user", "content": f"Translate these texts: {input}"})
        response = post(url, headers=headers, json=data)
        if response.status_code == 200:
            result = response.json()["result"]["response"]
    except Exception as e:
        print(str(e))
    return result
