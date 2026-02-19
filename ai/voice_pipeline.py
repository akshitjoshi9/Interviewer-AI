from core.config import openai_client


SYSTEM_PROMPT = """
You are a friendly, natural voice assistant.
Talk like a human.
Keep answers short, conversational, and spoken-friendly.
"""

class VoiceChatSession:
    def __init__(self):
        self.messages = [
            {"role": "system", "content": SYSTEM_PROMPT}
        ]

    def start(self) -> str:
        greeting = "Hi! I'm your AI assistant. You can talk to me naturally. What's on your mind today?"
        self.messages.append({"role": "assistant", "content": greeting})
        return greeting

    def reply(self, user_text: str) -> str:
        self.messages.append({"role": "user", "content": user_text})

        response = openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=self.messages,
            temperature=0.7
        )

        ai_text = response.choices[0].message.content
        self.messages.append({"role": "assistant", "content": ai_text})
        return ai_text
