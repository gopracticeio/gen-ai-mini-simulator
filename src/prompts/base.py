class Prompt(object):
    def __init__(self, system, user):
        self.system = system
        self.user = user

    def to_messages(self):
        messages = []
        if self.system is not None:
            messages.append({"role": "system", "content": self.system})
        messages.append({"role": "user", "content": self.user})
        return messages
