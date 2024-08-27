from messaging import poll_incoming_messages, send_message

class Messages():
    def __init__(self, sender_id: int, recipient_id: int) -> None:
        self.last_id: int = 0
        self.sender_id: int = sender_id
        self.recipient_id: int = recipient_id
        self.messages: list[dict] | None = poll_incoming_messages(sender_id, recipient_id, self.last_id)
    
    def get_last_id(self) -> int:
        return self.last_id

    def set_last_id(self, message_id: int) -> None:
        self.last_id = message_id
        if self.messages:
            new_msg = poll_incoming_messages(self.sender_id, self.recipient_id, self.last_id)
            if new_msg:
                self.messages.append(new_msg[0])
        else:
            self.messages = poll_incoming_messages(self.sender_id, self.recipient_id, self.last_id)

    def get_messages(self) -> list[dict] | None:
        return self.messages
    
    def add_message(self, corpus: str) -> None:
        send_message(self.sender_id, self.recipient_id, corpus)
        
        if self.messages:
            self.set_last_id(self.messages[-1]["message_id"])
        else:
            self.set_last_id(1)
        