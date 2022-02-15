from app.models.core import CoreModel
from typing import List, Dict, Any
from pydantic import EmailStr

class EmailSchema(CoreModel):
    subject: str
    email: List[EmailStr]
    body: Dict[str, Any]
