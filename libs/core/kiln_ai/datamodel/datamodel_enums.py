from enum import Enum, IntEnum


class Priority(IntEnum):
    """Defines priority levels for tasks and requirements, where P0 is highest priority."""

    p0 = 0
    p1 = 1
    p2 = 2
    p3 = 3


# Only one rating type for now, but this allows for extensibility if we want to add more in the future
class TaskOutputRatingType(str, Enum):
    """Defines the types of rating systems available for task outputs."""

    five_star = "five_star"
    pass_fail = "pass_fail"
    pass_fail_critical = "pass_fail_critical"
    custom = "custom"


class StructuredOutputMode(str, Enum):
    """
    Enumeration of supported structured output modes.

    - json_schema: request json using API capabilities for json_schema
    - function_calling: request json using API capabilities for function calling
    - json_mode: request json using API's JSON mode, which should return valid JSON, but isn't checking/passing the schema
    - json_instructions: append instructions to the prompt to request json matching the schema. No API capabilities are used. You should have a custom parser on these models as they will be returning strings.
    - json_instruction_and_object: append instructions to the prompt to request json matching the schema. Also request the response as json_mode via API capabilities (returning dictionaries).
    - json_custom_instructions: The model should output JSON, but custom instructions are already included in the system prompt. Don't append additional JSON instructions.
    - default: let the adapter decide (legacy, do not use for new use cases)
    - unknown: used for cases where the structured output mode is not known (on old models where it wasn't saved). Should lookup best option at runtime.
    """

    default = "default"
    json_schema = "json_schema"
    function_calling_weak = "function_calling_weak"
    function_calling = "function_calling"
    json_mode = "json_mode"
    json_instructions = "json_instructions"
    json_instruction_and_object = "json_instruction_and_object"
    json_custom_instructions = "json_custom_instructions"
    unknown = "unknown"


class FineTuneStatusType(str, Enum):
    """
    The status type of a fine-tune (running, completed, failed, etc).
    """

    unknown = "unknown"  # server error
    pending = "pending"
    running = "running"
    completed = "completed"
    failed = "failed"


class FinetuneDataStrategy(str, Enum):
    """Strategy for what data to include when fine-tuning a model."""

    # Only train on the final response, ignoring any intermediate steps or chain of thought
    final_only = "final_only"

    # Train on both the final response and any intermediate steps/chain of thought
    final_and_intermediate = "final_and_intermediate"

    # Train using R1-style thinking format, which includes the reasoning in <think> tags in the message
    final_and_intermediate_r1_compatible = "final_and_intermediate_r1_compatible"


THINKING_DATA_STRATEGIES: list[FinetuneDataStrategy] = [
    FinetuneDataStrategy.final_and_intermediate,
    FinetuneDataStrategy.final_and_intermediate_r1_compatible,
]


class ModelProviderName(str, Enum):
    """
    Enumeration of supported AI model providers.
    """

    openai = "openai"
    groq = "groq"
    amazon_bedrock = "amazon_bedrock"
    ollama = "ollama"
    openrouter = "openrouter"
    fireworks_ai = "fireworks_ai"
    kiln_fine_tune = "kiln_fine_tune"
    kiln_custom_registry = "kiln_custom_registry"
    openai_compatible = "openai_compatible"
    anthropic = "anthropic"
    gemini_api = "gemini_api"
    azure_openai = "azure_openai"
    huggingface = "huggingface"
    vertex = "vertex"
    together_ai = "together_ai"
