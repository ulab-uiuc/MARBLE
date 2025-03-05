from colorama import Fore, Style
class EventBus:
    def __init__(self):
        # 使用字典存储订阅者，键为索引，值为处理方法
        self.subscribers = {}

    def subscribe(self, index, handler):
        """
        订阅事件。
        
        Args:
            index: 订阅者的索引（可以是整数、字符串等）。
            handler: 订阅者的事件处理方法。
        """
        self.subscribers[index] = handler

    def publish(self, event: dict):
        """
        广播事件，调用事件接收者的处理方法。
        
        Args:
            event (dict): 包含事件数据的字典。必须包含 "recipients" 字段。
        """
        recipients = event.get("recipients", [])
        if not recipients:
            raise ValueError("No recipients specified for the event.")
        
        for recipient_index in recipients:
            if recipient_index not in self.subscribers:
                continue
            handler = self.subscribers[recipient_index]
            handler(event)