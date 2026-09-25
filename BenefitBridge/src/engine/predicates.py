from typing import Any, Callable, Dict
from src.models.schemas import UserProfile

# Type alias for a predicate function
# Takes the user profile and the threshold value, returns a boolean
PredicateFunc = Callable[[UserProfile, Any], bool]

def age_ge(user: UserProfile, value: int) -> bool:
    """Age Greater than or Equal to"""
    return user.age >= value

def age_le(user: UserProfile, value: int) -> bool:
    """Age Less than or Equal to"""
    return user.age <= value

def income_le(user: UserProfile, value: float) -> bool:
    """Monthly Income Less than or Equal to"""
    return user.monthly_income <= value

def income_ge(user: UserProfile, value: float) -> bool:
    """Monthly Income Greater than or Equal to"""
    return user.monthly_income >= value

def citizen_status_eq(user: UserProfile, value: str) -> bool:
    """Citizen Status Equals"""
    return user.citizen_status.lower() == value.lower()

def flat_type_in(user: UserProfile, value: list) -> bool:
    """Flat Type is in a list of allowed types"""
    return user.flat_type in value

# Registry mapping predicate keys to functions
PREDICATE_REGISTRY: Dict[str, PredicateFunc] = {
    "age_ge": age_ge,
    "age_le": age_le,
    "income_le": income_le,
    "income_ge": income_ge,
    "citizen_status": citizen_status_eq,
    "flat_type": flat_type_in,
}

def get_predicate(key: str) -> PredicateFunc:
    """Retrieve a predicate function by its key."""
    if key not in PREDICATE_REGISTRY:
        raise ValueError(f"Predicate '{key}' is not defined in the registry.")
    return PREDICATE_REGISTRY[key]
