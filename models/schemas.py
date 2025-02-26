from datetime import datetime, date
from typing import List, Optional
from pydantic import BaseModel, EmailStr, Field
from enum import Enum

class CadenceFrequency(str, Enum):
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    QUARTERLY = "quarterly"
    CUSTOM = "custom"

class Category(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    rule_text: str
    precedence_order: int = 0

class Contact(BaseModel):
    id: str
    name: str
    email: str
    phone: Optional[str] = None
    special_dates: dict[str, date] = Field(default_factory=dict)  # e.g., {"birthday": date(1990, 1, 1)}
    categories: List[str] = Field(default_factory=list)  # List of category IDs
    personal_instructions: Optional[str] = None
    cadence_frequency: CadenceFrequency = CadenceFrequency.MONTHLY
    next_outreach_date: datetime
    relevant_websites: List[str] = Field(default_factory=list)
    keywords: List[str] = Field(default_factory=list)
    last_contact: Optional[datetime] = None

class SystemSettings(BaseModel):
    system_prompt: str = "Maintain a friendly yet professional tone; keep the email concise."
    user_email: Optional[str] = None
    bcc_email: Optional[str] = None 