import logging
from jinja2 import Template
import json
import openai

from moonshot.src.common.env_variables import EnvironmentVars

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class ContextSummary:
    """
    This is a context strategy that summarizes the n (configureable) number of previous prompts. 
    Summary is performed by GPT-3.5 Turbo.
    """

    @staticmethod
    def add_in_context(
        prompt_without_context: str = None, list_of_previous_prompts: list = None
    ) -> str:
        """
        The method to process and insert the context. i.e. summarise the 5 previous prompts by calling another LLM.
        Insert the logic to create context in this method.
        Args:
            prompt_without_context (str, optional): The original prompt without context.
            list_of_previous_prompts (list, optional): The list of previous prompts in dict.
                The dict contains the following fields:
                - chat_id (int): ID of the chat
                - connection_id (str): ID of the connection
                - context_strategy (str): The context strategy that was used for that prompt (if any)
                - prompt_template (str): The name of the prompt template that was used (if any)
                - prompt (str): The original prompt that was entered (without context and prompt template)
                - prepared_prompt (str): The final prompt that was sent to the LLM
                  (with context and prompt template if any)
                - predicted_result (str): The response from the LLM

        Returns:
            str: The context to be sent with the prompt.
        """
        # Note from Sita: The variable prompt_template_name should be configurable. 
        file_info = None
        prompt_template_name = "cs-summarization"
        # Note from Sita: To refactor with model connectors. Current example uses OpenAI. Use personal OpenAI key here to test.
        openai_api_key = ""
        # Note from Sita: num_previous_prompts should be configurable. Currently. I cannot find a way to access the variable in the add_in_context method.
        num_previous_prompts = 2
        if num_previous_prompts != len(list_of_previous_prompts):
            return ""
        with open(f"{EnvironmentVars.PROMPT_TEMPLATES}/{prompt_template_name}.json" , "r" , encoding = "utf-8") as json_file:
            file_info = json.load(json_file)
        jinja_template = Template(file_info["template"])

        previous_run_str = ""
        for previous_prompt_dict in list_of_previous_prompts:
            previous_run_str += f'Prompt: {previous_prompt_dict.get("prompt")}\nResponse: {previous_prompt_dict.get("predicted_result")}\n'
        combined_contextualised_previous_prompt = jinja_template.render({"prompt": previous_run_str})
        
        payload = [
            {"role": "user" , "content": combined_contextualised_previous_prompt}
        ]
        openai.api_key = openai_api_key
        completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": combined_contextualised_previous_prompt}])
        output = f"Summary: {completion.choices[0].message.content}"
        return output + "\n"

    @staticmethod
    def get_number_of_prev_prompts() -> int:
        """
        A temporary method to store the number of previous prompts required for context strategy.

        Returns:
            int: The number of previous prompts required for context strategy.
        """
        num_previous_prompts = 2
        return num_previous_prompts
