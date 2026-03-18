from uuid import uuid4


class ObjectStorageService:
    """Stub service for encrypted object storage integration."""

    def create_object_key(self, subject_id: int, filename: str) -> str:
        suffix = filename.split(".")[-1] if "." in filename else "jpg"
        return f"subjects/{subject_id}/{uuid4()}.{suffix}"


object_storage_service = ObjectStorageService()
