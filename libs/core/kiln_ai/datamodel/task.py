from typing import TYPE_CHECKING, Dict, List, Union

from pydantic import BaseModel, Field

from kiln_ai.datamodel import Finetune
from kiln_ai.datamodel.basemodel import (
    ID_FIELD,
    ID_TYPE,
    NAME_FIELD,
    SHORT_NAME_FIELD,
    KilnParentedModel,
    KilnParentModel,
)
from kiln_ai.datamodel.datamodel_enums import Priority, TaskOutputRatingType
from kiln_ai.datamodel.dataset_split import DatasetSplit
from kiln_ai.datamodel.eval import Eval
from kiln_ai.datamodel.json_schema import JsonObjectSchema, schema_from_json_str
from kiln_ai.datamodel.prompt import Prompt
from kiln_ai.datamodel.prompt_id import PromptGenerators, PromptId
from kiln_ai.datamodel.task_run import TaskRun

if TYPE_CHECKING:
    from kiln_ai.datamodel.project import Project
    from kiln_ai.datamodel.task import RunConfig


class TaskRequirement(BaseModel):
    """
    Defines a specific requirement that should be met by task outputs.

    Includes an identifier, name, description, instruction for meeting the requirement,
    priority level, and rating type (five_star, pass_fail, pass_fail_critical, custom).
    """

    id: ID_TYPE = ID_FIELD
    name: str = SHORT_NAME_FIELD
    description: str | None = Field(default=None)
    instruction: str = Field(min_length=1)
    priority: Priority = Field(default=Priority.p2)
    type: TaskOutputRatingType = Field(default=TaskOutputRatingType.five_star)


class RunConfig(BaseModel):
    """
    A configuration for running a task.

    This includes everything needed to run a task, except the input. Running the same RunConfig with the same input should make identical calls to the model (output may vary as models are non-deterministic).

    For example: task, model, provider, prompt, etc.
    """

    task: "Task" = Field(description="The task to run.")
    model_name: str = Field(description="The model to use for this run config.")
    model_provider_name: str = Field(
        description="The provider to use for this run config."
    )
    prompt_id: PromptId = Field(
        description="The prompt to use for this run config. Defaults to building a simple prompt from the task if not provided.",
        default=PromptGenerators.SIMPLE,
    )


class Task(
    KilnParentedModel,
    KilnParentModel,
    parent_of={
        "runs": TaskRun,
        "dataset_splits": DatasetSplit,
        "finetunes": Finetune,
        "prompts": Prompt,
        "evals": Eval,
        # "run_configs": "RunConfig,
    },
):
    """
    Represents a specific task to be performed, with associated requirements and validation rules.

    Contains the task definition, requirements, input/output schemas, and maintains
    a collection of task runs.
    """

    name: str = NAME_FIELD
    description: str | None = Field(
        default=None,
        description="A description of the task for you and your team. Will not be used in prompts/training/validation.",
    )
    instruction: str = Field(
        min_length=1,
        description="The instructions for the task. Will be used in prompts/training/validation.",
    )
    requirements: List[TaskRequirement] = Field(default=[])
    output_json_schema: JsonObjectSchema | None = None
    input_json_schema: JsonObjectSchema | None = None
    thinking_instruction: str | None = Field(
        default=None,
        description="Instructions for the model 'thinking' about the requirement prior to answering. Used for chain of thought style prompting.",
    )

    def output_schema(self) -> Dict | None:
        if self.output_json_schema is None:
            return None
        return schema_from_json_str(self.output_json_schema)

    def input_schema(self) -> Dict | None:
        if self.input_json_schema is None:
            return None
        return schema_from_json_str(self.input_json_schema)

    # These wrappers help for typechecking. TODO P2: fix this in KilnParentModel
    def runs(self, readonly: bool = False) -> list[TaskRun]:
        return super().runs(readonly=readonly)  # type: ignore

    def dataset_splits(self, readonly: bool = False) -> list[DatasetSplit]:
        return super().dataset_splits(readonly=readonly)  # type: ignore

    def finetunes(self, readonly: bool = False) -> list[Finetune]:
        return super().finetunes(readonly=readonly)  # type: ignore

    def prompts(self, readonly: bool = False) -> list[Prompt]:
        return super().prompts(readonly=readonly)  # type: ignore

    def evals(self, readonly: bool = False) -> list[Eval]:
        return super().evals(readonly=readonly)  # type: ignore

    # Workaround to return typed parent without importing Task
    def parent_project(self) -> Union["Project", None]:
        if self.parent is None or self.parent.__class__.__name__ != "Project":
            return None
        return self.parent  # type: ignore
