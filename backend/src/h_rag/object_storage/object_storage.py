"""Abstract base class for object storage."""

from abc import ABC, abstractmethod


class ObjectStorage(ABC):
    """Abstract base class for object storage."""

    @abstractmethod
    def health_check(self) -> bool:
        """Check if the object storage can be reached."""
        pass

    @abstractmethod
    def upload_file(self, file_data: bytes, file_name: str) -> None:
        """Upload a file to Garage object storage.

        Args:
            file_data (bytes): The file data to upload.
            file_name (str): The name of the file in the bucket.
        """
        pass

    @abstractmethod
    def delete_file(self, file_name: str) -> None:
        """Delete a file from Garage object storage.

        Args:
            file_name (str): The name of the file to delete.
        """
        pass

    @abstractmethod
    def list_files(self) -> list[str]:
        """List files in a Garage object storage bucket.

        Returns:
            list[str]: A list of file names in the bucket.
        """
        pass

    @abstractmethod
    def delete_all_files(self) -> None:
        """Delete all files from a Garage object storage bucket."""
        pass

    @abstractmethod
    def get_file(self, file_name: str) -> bytes:
        """Download a file from Garage object storage.

        Args:
            file_name (str): The name of the file to download.

        Returns:
            bytes: The content of the downloaded file.
        """
        pass
