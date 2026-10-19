"""Small, dependency-free helpers for maintaining model conversation history."""


def build_messages(history, prompt):
    """Create a fresh request with prior turns and the new user message."""
    messages = list(history or [])
    messages.append({"role": "user", "content": prompt})
    return messages
