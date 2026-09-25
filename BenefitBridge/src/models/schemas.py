from pydantic import BaseModel, Field
from typing import List, Optional, Any, Union

class UserProfile(BaseModel):
    age: int = Field(..., description="Age of the senior")
    citizen_status: str = Field(..., description="Citizenship status (e.g., Singaporean, PR)")
    monthly_income: float = Field(..., description="Total monthly household income")
    flat_type: str = Field(..., description="HDB flat type (e.g., 1-room, 2-room, 3-room, etc.)")
    dependents_count: int = Field(0, description="Number of dependents")

class Rule(BaseModel):
    predicate: str = Field(..., description="The predicate key to use for evaluation")
    value: Any = Field(..., description="The threshold or value to compare against")
    logic: str = Field("AND", description="How to aggregate this rule (AND/OR)")

class Grant(BaseModel):
    id: str
    name: str
    description: str
    agency: str
    category: str
    application_url: str
    last_updated: str
    rules: List[Rule]
