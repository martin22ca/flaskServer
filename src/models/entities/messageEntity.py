
class Message():

    def __init__(self,messageTxt,info) -> None:
        self.messageTxt = messageTxt
        self.info = info

    def toJSON(self):
        return {
            "messageTxt": self.messageTxt,
            "info": self.info
        }