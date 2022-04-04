from typing import List, Dict, Any

from pydantic import EmailStr

from app.models.core import CoreModel


class EmailSchema(CoreModel):
    subject: str
    email: List[EmailStr]
    body: Dict[str, Any]
