"""Module for the Chunking Factory."""

from h_rag.config.config_wrapper import get_config
from h_rag.workflows.default_workflow import DefaultWorkflow
from h_rag.workflows.workflow import Workflow


class WorkflowFactory:
    """Factory class for creating Workflow instances based on the provider."""

    _workflows = {
        "Default": DefaultWorkflow,
    }

    @classmethod
    def get_workflow(cls, model: str, knowledge_base: str) -> Workflow:
        """Factory Method."""
        workflow = get_config("run", "workflow")
        try:
            return cls._workflows[workflow](model, knowledge_base)
        except KeyError:
            raise ValueError(
                f"Unknown workflow: {workflow}, available workflows: {list(cls._workflows.keys())}"
            )
