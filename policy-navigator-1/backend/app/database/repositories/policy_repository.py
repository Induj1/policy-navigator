from sqlalchemy.orm import Session
from app.models.policy import Policy
from app.database.connection import get_db

class PolicyRepository:
    def __init__(self, db: Session = next(get_db())):
        self.db = db

    def get_policy_by_id(self, policy_id: int) -> Policy:
        return self.db.query(Policy).filter(Policy.id == policy_id).first()

    def get_all_policies(self) -> list[Policy]:
        return self.db.query(Policy).all()

    def create_policy(self, policy: Policy) -> Policy:
        self.db.add(policy)
        self.db.commit()
        self.db.refresh(policy)
        return policy

    def update_policy(self, policy_id: int, updated_policy: Policy) -> Policy:
        policy = self.get_policy_by_id(policy_id)
        if policy:
            for key, value in updated_policy.dict().items():
                setattr(policy, key, value)
            self.db.commit()
            self.db.refresh(policy)
        return policy

    def delete_policy(self, policy_id: int) -> bool:
        policy = self.get_policy_by_id(policy_id)
        if policy:
            self.db.delete(policy)
            self.db.commit()
            return True
        return False