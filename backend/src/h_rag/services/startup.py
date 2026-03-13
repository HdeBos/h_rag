"""Service layer for health checks."""

import asyncio

from h_rag.llm.llm_factory import LLMFactory
from h_rag.object_storage.object_storage_factory import ObjectStorageFactory
from h_rag.tools import initialize_logger, load_env


class StartupService:
    """Service to check the health of various components in the system."""

    async def initalize_environment(self):
        """Initialize environment variables and logger."""
        load_env()
        initialize_logger()

    async def check_object_storage(self):
        """Check if the object storage is healthy."""
        object_storage = ObjectStorageFactory.get_object_storage()
        healthy = await asyncio.to_thread(object_storage.health_check)
        if not healthy:
            raise RuntimeError("Object storage unavailable")

    async def check_llm(self):
        """Check if the LLM gateway is healthy."""
        llm = LLMFactory.get_llm()
        healthy = await asyncio.to_thread(llm.health_check)
        if not healthy:
            raise RuntimeError("LLM gateway unavailable")
