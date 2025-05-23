# models.py
from uagents import Model
from pydantic.v1 import Field  # ✅ Explicitly use Pydantic v1 to avoid JSON error

class Payment(Model):
    amount: int = Field(...)
    receiver: str = Field(...)
