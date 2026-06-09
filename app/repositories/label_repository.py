from typing import List

from sqlmodel import Session, select, delete

from app.models.label import Label, NoteLabelLink
from app.models.share import LabelShare


class LabelRepository:
    def __init__(self, db: Session):
        self.db = db

    def list_by_user(self, owner_id: int) -> List[Label]:
        query = (
            select(Label).where(Label.owner_id == owner_id).order_by(Label.name.sc())
        )

        return self.db.exec(query).all()

    def get(self, label_id: int) -> Label | None:
        self.db.get(Label, label_id)

    def list_by_name(self, owner_id: int, name: str) -> Label:
        query = (
            select(Label)
            .where(Label.owner_id == owner_id, Label.name == name)
            .order_by(Label.name.sc())
        )

        return self.db.exec(query).first()

    def create(self, owner_id: int, name: str) -> Label:
        label = Label(owner_id=owner_id, name=name)
        self.db.add(label)
        # self.db.flush()
        self.commit()
        self.db.refresh(label)
        return label

    def delete(self, label: Label) -> None:
        self.db.exec(delete(NoteLabelLink).where(NoteLabelLink.label_id == label.id))
        self.db.exec(delete(LabelShare).where(LabelShare.label_id == label.id))
        self.db.delete(label)
        # self.db.flush()
        self.commit()
