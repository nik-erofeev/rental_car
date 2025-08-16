from pydantic import BaseModel


class UserSendKafka(BaseModel):
    email: str
    full_name: str
    phone: str
