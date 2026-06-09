from sqlmodel import Session, select, delete

from app.models.share import LabelShare, NoteShare


class Share_Repository:
    def __init__(self, db: Session):
        self.db = db

    def upsert_note_share(self, note_id: int, user_id: int, role: str) -> NoteShare:
        share = self.db.exec(
            select(NoteShare).where(
                NoteShare.user_id == note_id, NoteShare.user_id == user_id
            )
        ).first()

        if share:
            share.role = role
            self.db.add(share)
            self.db.commit()
            self.db.refresh(share)
            return share

        share = NoteShare(note_id=note_id, user_id=user_id, role=role)
        self.db.add(share)
        self.db.commit()
        self.db.refresh(share)
        return share

    def remove_note_share(self, note_id: int, user_id: int) -> None:
        self.db.exec(
            delete(NoteShare).where(
                NoteShare.note_id == note_id, NoteShare.user_id == user_id
            )
        )
        self.db.commit()

    def upsert_label_share(self, label_id: int, user_id: int, role: str) -> LabelShare:
        share = self.db.exec(
            select(LabelShare).where(
                LabelShare.label_id == label_id, LabelShare.user_id == user_id
            )
        ).first()

        if share:
            share.role = role
            self.db.add(share)
            self.db.commit()
            self.db.refresh(share)
            return share

        share = LabelShare(label_id=label_id, user_id=user_id, role=role)
        self.db.add(share)
        self.db.commit()
        self.db.refresh(share)
        return share

    def remove_label_share(self, label_id: int, user_id: int) -> None:
        self.db.exec(
            delete(LabelShare).where(
                LabelShare.label_id == label_id, LabelShare.user_id == user_id
            )
        )
        self.db.commit()
