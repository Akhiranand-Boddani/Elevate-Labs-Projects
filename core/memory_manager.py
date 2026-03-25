class ConversationMemory:
    def __init__(self, max_turns: int = 5):
        self.history = []
        self.max_turns = max_turns

    def update(self, role: str, content: str):
        self.history.append({"role": role, "content": content})
        if len(self.history) > self.max_turns * 2:
            self.history = self.history[-(self.max_turns * 2):]

    def get_messages(self) -> list:
        return self.history

    def clear(self):
        self.history = []
