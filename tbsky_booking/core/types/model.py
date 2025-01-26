import uuid

PrimaryKeyType = uuid.UUID
ForeignKeyType = uuid.UUID
OptionalForeignKeyType = uuid.UUID | None

__all__ = ["PrimaryKeyType", "ForeignKeyType", "OptionalForeignKeyType"]
