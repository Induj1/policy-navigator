from sqlalchemy.orm import Session
from app.models.credential import CitizenCredential
from app.database.connection import get_db

class CredentialRepository:
    def __init__(self, db: Session = next(get_db())):
        self.db = db

    def create_credential(self, credential_data: dict) -> CitizenCredential:
        credential = CitizenCredential(**credential_data)
        self.db.add(credential)
        self.db.commit()
        self.db.refresh(credential)
        return credential

    def get_credential(self, credential_id: int) -> CitizenCredential:
        return self.db.query(CitizenCredential).filter(CitizenCredential.id == credential_id).first()

    def update_credential(self, credential_id: int, credential_data: dict) -> CitizenCredential:
        credential = self.get_credential(credential_id)
        for key, value in credential_data.items():
            setattr(credential, key, value)
        self.db.commit()
        return credential

    def delete_credential(self, credential_id: int) -> None:
        credential = self.get_credential(credential_id)
        if credential:
            self.db.delete(credential)
            self.db.commit()