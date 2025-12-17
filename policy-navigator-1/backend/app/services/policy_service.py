from typing import List, Dict
from app.models.policy import Policy
from app.database.repositories.policy_repository import PolicyRepository

class PolicyService:
    def __init__(self, policy_repository: PolicyRepository):
        self.policy_repository = policy_repository

    def get_all_policies(self) -> List[Policy]:
        return self.policy_repository.get_all()

    def get_policy_by_id(self, policy_id: str) -> Policy:
        return self.policy_repository.get_by_id(policy_id)

    def create_policy(self, policy_data: Dict) -> Policy:
        new_policy = Policy(**policy_data)
        return self.policy_repository.create(new_policy)

    def update_policy(self, policy_id: str, policy_data: Dict) -> Policy:
        existing_policy = self.policy_repository.get_by_id(policy_id)
        for key, value in policy_data.items():
            setattr(existing_policy, key, value)
        return self.policy_repository.update(existing_policy)

    def delete_policy(self, policy_id: str) -> None:
        self.policy_repository.delete(policy_id)