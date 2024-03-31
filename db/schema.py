from datetime import datetime
from pydantic import BaseModel, Field

class Purchase(BaseModel):
    id: str
    value: float
    date: datetime = Field(default_factory=datetime.now)