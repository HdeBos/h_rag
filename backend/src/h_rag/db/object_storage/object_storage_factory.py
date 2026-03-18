"""Factory for creating vector database instances."""

from h_rag.config.config_wrapper import get_config
from h_rag.db.object_storage.garage_wrapper import GarageWrapper
from h_rag.db.object_storage.object_storage import ObjectStorage


class ObjectStorageFactory:
    """Factory for creating object storage instances."""

    _object_storages = {
        "Garage": GarageWrapper,
    }

    @classmethod
    def get_object_storage(cls) -> ObjectStorage:
        """Factory Method."""
        method = get_config("object_storage", "provider")
        try:
            return cls._object_storages[method]()
        except KeyError:
            raise ValueError(
                f"Unknown object storage: {method}, available methods: {list(cls._object_storages.keys())}"
            )
