import yaml
from typing import List, Tuple
from src.models.schemas import UserProfile, Grant, Rule
from src.engine.predicates import get_predicate

class EligibilityEvaluator:
    def __init__(self, grants_file: str):
        self.grants = self._load_grants(grants_file)

    def _load_grants(self, file_path: str) -> List[Grant]:
        with open(file_path, 'r') as f:
            data = yaml.safe_load(f)
            return [Grant(**g) for g in data.get('grants', [])]

    def evaluate(self, user: UserProfile) -> List[Tuple[Grant, bool, str]]:
        """
        Evaluates a user against all grants.
        Returns a list of (Grant, is_eligible, reasoning).
        """
        results = []
        for grant in self.grants:
            is_eligible, reason = self._check_grant(user, grant)
            results.append((grant, is_eligible, reason))
        return results

    def _check_grant(self, user: UserProfile, grant: Grant) -> Tuple[bool, str]:
        if not grant.rules:
            return True, "No specific eligibility rules defined."

        # We support basic AND/OR aggregation.
        # For MVP, we'll evaluate based on the first rule's logic or a simplified
        # approach: all rules must be true unless some are explicitly marked OR.

        # Simplified MVP logic:
        # 1. Evaluate all rules.
        # 2. If any rule is 'OR' and true, and all 'AND' rules are true -> Eligible.
        # Actually, a more robust way for MVP:
        # Treat as: (All AND rules must be true) AND (At least one OR rule must be true if any OR rules exist).

        and_rules = [r for r in grant.rules if r.logic == "AND"]
        or_rules = [r for r in grant.rules if r.logic == "OR"]

        # Check AND rules
        for rule in and_rules:
            predicate_fn = get_predicate(rule.predicate)
            if not predicate_fn(user, rule.value):
                return False, f"Failed mandatory requirement: {rule.predicate} (Expected {rule.value})"

        # Check OR rules
        if or_rules:
            any_or_true = False
            for rule in or_rules:
                predicate_fn = get_predicate(rule.predicate)
                if predicate_fn(user, rule.value):
                    any_or_true = True
                    break
            if not any_or_true:
                return False, f"Failed optional requirements: None of the following were met: {[r.predicate for r in or_rules]}"

        return True, "All eligibility criteria met."
