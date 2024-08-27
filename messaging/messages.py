from messaging import poll_incoming_messages, send_message


class Messages():
    def __init__(self, sender_id: int, recipient_id: int) -> None:
        self.sender_id: int = sender_id
        self.recipient_id: int = recipient_id
        self.messages: list[dict] | None = poll_incoming_messages(sender_id, recipient_id, 0)
        self.last_id: int = self.messages[-1]["message_id"] if self.messages else 0
        self.last_index: int = self.messages.index(self.messages[-1]) if self.messages else 0
        self.is_new_messages: bool = False
        
    def refresh(self) -> None:
        new_msgs = poll_incoming_messages(self.sender_id, self.recipient_id, self.last_id)

        if new_msgs:
            self.is_new_messages = True

            for msg in new_msgs:
                if self.messages:
                    self.messages.append(msg)
                else:
                    self.messages = new_msgs
        
        if self.messages:
            self.last_index = self.messages.index(self.messages[-1])
            self.last_id = self.messages[-1]["message_id"]
        
    def get_messages(self) -> list[dict] | None:
        return self.messages
    
    def get_last_index(self) -> int:
        return self.last_index
    
    def get_is_new_messages(self) -> bool:
        return self.is_new_messages
    
    def set_is_new_messages(self, is_new_messages) -> None:
        self.is_new_messages = is_new_messages

    def add_message(self, corpus: str) -> None:
        send_message(self.sender_id, self.recipient_id, corpus)
        
        self.last_id = self.messages[-1]["message_id"] if self.messages else 0
    


        