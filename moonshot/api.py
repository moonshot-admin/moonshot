from moonshot.src.benchmarking.cookbooks.cookbook import Cookbook
from moonshot.src.benchmarking.cookbooks.cookbook_arguments import CookbookArguments
from moonshot.src.benchmarking.executors.benchmark_executor import BenchmarkExecutor
from moonshot.src.benchmarking.executors.benchmark_executor_arguments import (
    BenchmarkExecutorArguments,
)
from moonshot.src.benchmarking.executors.benchmark_executor_types import (
    BenchmarkExecutorTypes,
)
from moonshot.src.benchmarking.recipes.recipe import Recipe
from moonshot.src.benchmarking.recipes.recipe_arguments import RecipeArguments
from moonshot.src.connectors.connector import Connector
from moonshot.src.connectors.connector_endpoint_arguments import (
    ConnectorEndpointArguments,
)
from moonshot.src.connectors.connector_manager import ConnectorManager


# ------------------------------------------------------------------------------
# Environment Variables APIs
# ------------------------------------------------------------------------------
def api_set_environment_variables(env_vars: dict) -> None:
    """
    Sets the environment variables for the current session.

    Args:
        env_vars (dict): A dictionary containing the environment variables to set.

    Returns:
        None
    """
    pass


# ------------------------------------------------------------------------------
# Connector APIs
# ------------------------------------------------------------------------------
def api_create_endpoint(
    name: str,
    connector_type: str,
    uri: str,
    token: str,
    max_calls_per_second: int,
    max_concurrency: int,
    params: dict,
) -> None:
    """
    Creates a new endpoint to the connector manager.

    This function creates a new connector endpoint with the specified parameters. It constructs a
    ConnectorEndpointArguments object with the provided details and then calls the ConnectorManager's create_endpoint
    method to add the new endpoint.

    Args:
        name (str): The name of the new endpoint.
        connector_type (str): The type of the connector (e.g., 'GPT-3', 'Bert', etc.).
        uri (str): The URI for the connector's API.
        token (str): The access token for the API.
        max_calls_per_second (int): The maximum number of API calls allowed per second.
        max_concurrency (int): The maximum number of concurrent API calls.
        params (dict): Additional parameters for the connector.

    Returns:
        None
    """
    # Create a new connector endpoint arguments instance.
    # We do not need to provide id and created_date.
    # This is because during creation:
    #   1. the id is slugify from the name and stored as id.
    #   2. the created_date is based on the os file created date and time.
    connector_endpoint_args = ConnectorEndpointArguments(
        id="",
        name=name,
        connector_type=connector_type,
        uri=uri,
        token=token,
        max_calls_per_second=max_calls_per_second,
        max_concurrency=max_concurrency,
        params=params,
        created_date="",
    )
    ConnectorManager.create_endpoint(connector_endpoint_args)


def api_read_endpoint(ep_id: str) -> dict:
    """
    Reads an endpoint from the connector manager.

    This function reads an endpoint from the connector manager using the provided endpoint ID.

    Args:
        ep_id (str): The ID of the endpoint to read.

    Returns:
        dict: A dictionary containing the endpoint information.
    """
    return ConnectorManager.read_endpoint(ep_id).to_dict()


def api_update_endpoint(
    name: str,
    connector_type: str,
    uri: str,
    token: str,
    max_calls_per_second: int,
    max_concurrency: int,
    params: dict,
) -> None:
    """
    Updates an existing endpoint in the connector manager.

    This function updates an existing endpoint in the connector manager using the provided endpoint details.
    It first creates a ConnectorEndpointArguments instance with the provided details, then calls the
    ConnectorManager's update_endpoint method to update the endpoint.

    Args:
        name (str): The name of the endpoint.
        connector_type (str): The type of the connector.
        uri (str): The URI for the connector.
        token (str): The token for the connector.
        max_calls_per_second (int): The maximum number of API calls allowed per second.
        max_concurrency (int): The maximum number of concurrent API calls.
        params (dict): Additional parameters for the connector.

    Returns:
        None
    """
    connector_endpoint_args = ConnectorEndpointArguments(
        id="",
        name=name,
        connector_type=connector_type,
        uri=uri,
        token=token,
        max_calls_per_second=max_calls_per_second,
        max_concurrency=max_concurrency,
        params=params,
        created_date="",
    )
    ConnectorManager.update_endpoint(connector_endpoint_args)


def api_delete_endpoint(ep_id: str) -> None:
    """
    Deletes an existing endpoint in the connector manager.

    This function deletes an existing endpoint in the connector manager using the provided endpoint ID.
    It calls the ConnectorManager's delete_endpoint method to delete the endpoint.

    Args:
        ep_id (str): The ID of the endpoint to be deleted.

    Returns:
        None
    """
    ConnectorManager.delete_endpoint(ep_id)


def api_get_all_endpoints() -> list[dict]:
    """
    Retrieves a list of all available endpoints.

    This function calls the ConnectorManager's get_available_endpoints method to retrieve a list of all available
    endpoints and their details. It then converts each ConnectorEndpointArguments object into a dictionary for easier
    consumption by the caller.

    Returns:
        list[dict]: A list of dictionaries, each representing an endpoint's details.
    """
    _, endpoints = ConnectorManager.get_available_endpoints()
    return [endpoint.to_dict() for endpoint in endpoints]


def api_get_all_endpoints_names() -> list[str]:
    """
    Retrieves a list of all endpoint names.

    This function calls the ConnectorManager's get_available_endpoints method to retrieve a list of all available
    endpoint names. It extracts the names from the tuple returned by get_available_endpoints, which contains a list
    of endpoint names and a list of ConnectorEndpointArguments objects.

    Returns:
        list[str]: A list of endpoint names.
    """
    endpoints_names, _ = ConnectorManager.get_available_endpoints()
    return endpoints_names


def api_create_connector(ep_id: str) -> Connector:
    """
    Creates a connector based on the provided endpoint ID.

    This function retrieves the endpoint arguments using the provided endpoint ID and then creates a connector
    based on those arguments. It utilizes the ConnectorManager's read_endpoint method to fetch the endpoint
    arguments and then calls the create_connector method to initialize and return the connector.

    Args:
        ep_id (str): The ID of the endpoint for which to create a connector.

    Returns:
        Connector: An initialized Connector object.
    """
    return ConnectorManager.create_connector(ConnectorManager.read_endpoint(ep_id))


def api_create_connectors(ep_ids: list[str]) -> list[Connector]:
    """
    Creates connectors for multiple endpoints based on their IDs.

    This function takes a list of endpoint IDs, retrieves the corresponding endpoint arguments for each ID, and then
    creates and returns a list of connector objects based on those arguments. It utilizes the ConnectorManager's
    read_endpoint method to fetch the endpoint arguments and the create_connector method to initialize the connectors.

    Args:
        ep_ids (list[str]): A list of endpoint IDs for which connectors are to be created.

    Returns:
        list[Connector]: A list of initialized Connector objects.
    """
    return [
        ConnectorManager.create_connector(ConnectorManager.read_endpoint(ep_id))
        for ep_id in ep_ids
    ]


def api_get_all_connectors() -> list[str]:
    """
    Retrieves a list of all available connectors.

    This function calls the ConnectorManager's get_available_connectors method to retrieve a list of all available
    connectors. It returns a list of connector names, which are the names of Python files in the specified directory
    excluding any special or private files (denoted by "__" in their names).

    Returns:
        list[str]: A list of the names of available connectors.
    """
    return ConnectorManager.get_available_connectors()


# ------------------------------------------------------------------------------
# Cookbook APIs
# ------------------------------------------------------------------------------
def api_create_cookbook(name: str, description: str, recipes: list[str]) -> None:
    """
    Creates a new cookbook.

    This function takes the name, description, and recipes for a new cookbook as input. It then creates a new
    CookbookArguments object with these details and an empty id. The id is left empty because it will be generated
    from the name during the creation process. The function then calls the Cookbook's create_cookbook method to
    create the new cookbook.

    Args:
        name (str): The name of the new cookbook.
        description (str): A brief description of the new cookbook.
        recipes (list[str]): A list of recipes to be included in the new cookbook.
    """
    # Create a new cookbook
    # We do not need to provide the id.
    # This is because during creation:
    # 1. the id is slugify from the name and stored as id.
    cb_args = CookbookArguments(
        id="",
        name=name,
        description=description,
        recipes=recipes,
    )
    Cookbook.create_cookbook(cb_args)


def api_read_cookbook(cb_id: str) -> dict:
    """
    Retrieves a cookbook based on the provided cookbook ID.

    This function reads a cookbook using the `read_cookbook` method
    of the `Cookbook` class, and converts the returned `Cookbook` object to a dictionary using its `to_dict` method.

    Args:
        cb_id (str): A cookbook ID.

    Returns:
        dict: A dictionary representing a cookbook.
    """
    return Cookbook.read_cookbook(cb_id).to_dict()


def api_read_cookbooks(cb_ids: list[str]) -> list[dict]:
    """
    Retrieves a list of cookbooks based on the provided list of cookbook IDs.

    This function iterates over the list of cookbook IDs, reads each cookbook using the `read_cookbook` method
    of the `Cookbook` class, and converts the returned `Cookbook` object to a dictionary using its `to_dict` method.
    It returns a list of these dictionaries.

    Args:
        cb_ids (list[str]): A list of cookbook IDs.

    Returns:
        list[dict]: A list of dictionaries, each representing a cookbook.
    """
    return [Cookbook.read_cookbook(cb_id).to_dict() for cb_id in cb_ids]


def api_update_cookbook(
    name: str,
    description: str,
    recipes: list[str],
) -> None:
    """
    Updates an existing cookbook with new information.

    This function takes a cookbook ID and a CookbookArguments object as input, which contains the new information for
    the cookbook. It first deletes the existing cookbook with the same ID, then creates a new cookbook with the
    updated information. If the operation fails for any reason, an exception is raised and the error is printed.

    Args:
        cb_id (str): The ID of the cookbook to update.
        name (str): The new name of the cookbook.
        description (str): The new description of the cookbook.
        recipes (list[str]): The new list of recipes for the cookbook.

    Raises:
        Exception: If there is an error during the update operation.
    """
    cb_args = CookbookArguments(
        id="",
        name=name,
        description=description,
        recipes=recipes,
    )
    Cookbook.update_cookbook(cb_args)


def api_delete_cookbook(cb_id: str) -> None:
    """
    Deletes a cookbook.

    This function calls the `delete_cookbook` method of the `Cookbook` class, which deletes the cookbook
    corresponding to the provided ID.

    Args:
        cb_id (str): The ID of the cookbook to delete.
    """
    Cookbook.delete_cookbook(cb_id)


def api_get_all_cookbooks() -> list[dict]:
    """
    Retrieves all available cookbooks.

    This function calls the `get_available_cookbooks` method of the `Cookbook` class, which returns a tuple
    containing a list of cookbook IDs and a list of `CookbookArguments` objects. The function then returns a list
    of dictionaries, each representing a cookbook.

    Returns:
        list[dict]: A list of dictionaries, each representing a cookbook.
    """
    _, cookbooks = Cookbook.get_available_cookbooks()
    return [cookbook.to_dict() for cookbook in cookbooks]


def api_get_all_cookbooks_names() -> list[str]:
    """
    Retrieves the names of all available cookbooks.

    This function calls the `get_available_cookbooks` method of the `Cookbook` class, which returns a tuple
    containing a list of cookbook IDs and a list of `CookbookArguments` objects. The function then returns the
    list of cookbook IDs, which are the names of the cookbooks.

    Returns:
        list[str]: A list of cookbook names.
    """
    cookbooks_names, _ = Cookbook.get_available_cookbooks()
    return cookbooks_names


# ------------------------------------------------------------------------------
# Recipe APIs
# ------------------------------------------------------------------------------
def api_create_recipe(
    name: str,
    description: str,
    tags: list[str],
    datasets: list[str],
    prompt_templates: list[str],
    metrics: list[str],
) -> None:
    """
    Creates a new recipe.

    This function takes a name, description, tags, datasets, prompt templates, and metrics as input, and creates a
    new recipe. It constructs a RecipeArguments object with the provided details and then calls the Recipe's
    create_recipe method to add the new recipe.

    Args:
        name (str): The name of the new recipe.
        description (str): The description of the recipe.
        tags (list[str]): The tags associated with the recipe.
        datasets (list[str]): The datasets used in the recipe.
        prompt_templates (list[str]): The prompt templates used in the recipe.
        metrics (list[str]): The metrics used in the recipe.

    Returns:
        None
    """
    # Create a new recipe
    # We do not need to provide the id.
    # This is because during creation:
    # 1. the id is slugify from the name and stored as id.
    rec_args = RecipeArguments(
        id="",
        name=name,
        description=description,
        tags=tags,
        datasets=datasets,
        prompt_templates=prompt_templates,
        metrics=metrics,
    )
    Recipe.create_recipe(rec_args)


def api_read_recipe(rec_id: str) -> dict:
    """
    Reads a recipe and returns its information.

    This function takes a recipe ID as input, reads the corresponding recipe,
    and returns a dictionary containing the recipe's information.

    Args:
        rec_id (str): The ID of the recipe.

    Returns:
        dict: A dictionary containing the recipe's information.
    """
    return Recipe.read_recipe(rec_id).to_dict()


def api_read_recipes(rec_ids: list[str]) -> list[dict]:
    """
    Reads multiple recipes and returns their information.

    This function takes a list of recipe IDs as input, reads the corresponding recipes,
    and returns a list of dictionaries containing each recipe's information.

    Args:
        rec_ids (list[str]): The IDs of the recipes.

    Returns:
        list[dict]: A list of dictionaries, each containing a recipe's information.
    """
    # This function uses list comprehension to iterate over the list of recipe IDs,
    # calling the read_recipe method for each ID and converting the result to a dictionary.
    # The resulting list of dictionaries is then returned.
    return [Recipe.read_recipe(rec_id).to_dict() for rec_id in rec_ids]


def api_update_recipe(
    name: str,
    description: str,
    tags: list[str],
    datasets: list[str],
    prompt_templates: list[str],
    metrics: list[str],
) -> None:
    """
    Updates an existing recipe with new information.

    This function takes a set of arguments for a recipe, including its name, description, tags, datasets,
    prompt templates, and metrics. It first deletes the existing recipe with the same ID, then creates a new
    recipe with the updated information.

    Args:
        name (str): The name of the recipe.
        description (str): The description of the recipe.
        tags (list[str]): The tags associated with the recipe.
        datasets (list[str]): The datasets used in the recipe.
        prompt_templates (list[str]): The prompt templates used in the recipe.
        metrics (list[str]): The metrics used in the recipe.
    """
    rec_args = RecipeArguments(
        id="",
        name=name,
        description=description,
        tags=tags,
        datasets=datasets,
        prompt_templates=prompt_templates,
        metrics=metrics,
    )
    Recipe.update_recipe(rec_args)


def api_delete_recipe(rec_id: str) -> None:
    """
    Deletes a recipe.

    This method takes a recipe ID as input, deletes the corresponding JSON file from the directory specified by
    `EnvironmentVars.RECIPES`. If the operation fails for any reason, an exception is raised and the
    error is printed.

    Args:
        rec_id (str): The ID of the recipe to delete.

    Raises:
        Exception: If there is an error during file deletion or any other operation within the method.
    """
    Recipe.delete_recipe(rec_id)


def api_get_all_recipes() -> list[dict]:
    """
    Retrieves all available recipes.

    This function calls the get_available_recipes method to retrieve all available recipes. It then converts each
    recipe into a dictionary using the to_dict method and returns a list of these dictionaries.

    Returns:
        list[dict]: A list of dictionaries, each representing a recipe.
    """
    _, recipes = Recipe.get_available_recipes()
    return [recipe.to_dict() for recipe in recipes]


def api_get_all_recipes_names() -> list[str]:
    """
    Retrieves all available recipe names.

    This function calls the get_available_recipes method to retrieve all available recipes. It then extracts the names
    of each recipe and returns a list of these names.

    Returns:
        list[str]: A list of strings, each representing a recipe name.
    """
    recipes_names, _ = Recipe.get_available_recipes()
    return recipes_names


# ------------------------------------------------------------------------------
# Metrics APIs
# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
# Benchmark executor APIs
# ------------------------------------------------------------------------------
def api_create_recipe_executor(
    name: str, recipes: list[str], endpoints: list[str], num_of_prompts: int
) -> BenchmarkExecutor:
    """
    Creates a new recipe executor.

    This function takes a name, a list of recipes, a list of endpoints, and a number of prompts as input. It then
    creates a new BenchmarkExecutorArguments object with these inputs and an empty id. The id is left empty because
    it will be generated from the name during the creation process. The function then calls the create_executor method
    to create a new recipe executor and returns the result.

    Args:
        name (str): The name of the new recipe executor.
        recipes (list[str]): A list of recipes for the new recipe executor.
        endpoints (list[str]): A list of endpoints for the new recipe executor.
        num_of_prompts (int): The number of prompts for the new recipe executor.

    Returns:
        BenchmarkExecutor: The newly created recipe executor.
    """
    # Create a new recipe executor
    # We do not need to provide the id.
    # This is because during creating:
    # 1. the id is slugify from the name and stored as id.
    be_args = BenchmarkExecutorArguments(
        id="",
        name=name,
        type=BenchmarkExecutorTypes.RECIPE,
        recipes=recipes,
        endpoints=endpoints,
        num_of_prompts=num_of_prompts,
    )
    return BenchmarkExecutor.create_executor(be_args)


def api_create_cookbook_executor(
    name: str, cookbooks: list[str], endpoints: list[str], num_of_prompts: int
) -> BenchmarkExecutor:
    """
    Creates a new cookbook executor.

    This function takes a name, a list of cookbooks, a list of endpoints, and a number of prompts as input. It then
    creates a new BenchmarkExecutorArguments object with these inputs and an empty id. The id is left empty because it
    will be generated from the name during the creation process. The function then calls the create_executor method to
    create a new cookbook executor and returns the result.

    Args:
        name (str): The name of the new cookbook executor.
        cookbooks (list[str]): A list of cookbooks for the new cookbook executor.
        endpoints (list[str]): A list of endpoints for the new cookbook executor.
        num_of_prompts (int): The number of prompts for the new cookbook executor.

    Returns:
        BenchmarkExecutor: The newly created cookbook executor.
    """
    # Create a new cookbook executor
    # We do not need to provide the id.
    # This is because during creating:
    # 1. the id is slugify from the name and stored as id.
    be_args = BenchmarkExecutorArguments(
        id="",
        name=name,
        type=BenchmarkExecutorTypes.COOKBOOK,
        cookbooks=cookbooks,
        endpoints=endpoints,
        num_of_prompts=num_of_prompts,
    )
    return BenchmarkExecutor.create_executor(be_args)


def api_load_executor(be_id: str) -> BenchmarkExecutor:
    """
    Loads a benchmark executor from a database file.

    This method reads the benchmark executor information from a database file specified by the executor ID. It
    constructs the file path using the executor ID and the designated directory for executors. The method
    then reads the database file and returns the executor information as a BenchmarkExecutorArguments object.

    Args:
        be_id (str): The ID of the benchmark executor.

    Returns:
        BenchmarkExecutor: An instance of the BenchmarkExecutor class with the loaded executor information.
    """
    return BenchmarkExecutor.load_executor(be_id)


def api_read_executor(be_id: str) -> dict:
    """
    Reads an executor and returns its information.

    This function takes an executor ID as input, reads the corresponding database file from the storage manager,
    and returns a dictionary containing the executor's information.

    Args:
        be_id (str): The ID of the executor.

    Returns:
        dict: A dictionary containing the executor's information.
    """
    return BenchmarkExecutor.read_executor_arguments(be_id).to_dict()


def api_update_recipe_executor(
    name: str, recipes: list[str], endpoints: list[str], num_of_prompts: int
) -> None:
    """
    This function takes a name, a list of recipes, a list of endpoints, and a number of prompts as input. It then
    creates a new BenchmarkExecutorArguments object with these inputs and an empty id. The id is left empty because it
    will be generated from the name during the creation process. The function then calls the update_executor method to
    update an existing recipe executor with the new information.

    Args:
        name (str): The name of the recipe executor to be updated.
        recipes (list[str]): A list of recipes for the updated recipe executor.
        endpoints (list[str]): A list of endpoints for the updated recipe executor.
        num_of_prompts (int): The number of prompts for the updated recipe executor.
    """
    be_args = BenchmarkExecutorArguments(
        id="",
        name=name,
        type=BenchmarkExecutorTypes.RECIPE,
        recipes=recipes,
        endpoints=endpoints,
        num_of_prompts=num_of_prompts,
    )
    BenchmarkExecutor.update_executor(be_args)


def api_update_cookbook_executor(
    name: str, cookbooks: list[str], endpoints: list[str], num_of_prompts: int
) -> None:
    """
    This function takes a name, a list of cookbooks, a list of endpoints, and a number of prompts as input. It then
    creates a new BenchmarkExecutorArguments object with these inputs and an empty id. The id is left empty because it
    will be generated from the name during the creation process. The function then calls the update_executor method to
    update an existing cookbook executor with the new information.

    Args:
        name (str): The name of the cookbook executor to be updated.
        cookbooks (list[str]): A list of cookbooks for the updated cookbook executor.
        endpoints (list[str]): A list of endpoints for the updated cookbook executor.
        num_of_prompts (int): The number of prompts for the updated cookbook executor.
    """
    be_args = BenchmarkExecutorArguments(
        id="",
        name=name,
        type=BenchmarkExecutorTypes.COOKBOOK,
        cookbooks=cookbooks,
        endpoints=endpoints,
        num_of_prompts=num_of_prompts,
    )
    BenchmarkExecutor.update_executor(be_args)


def api_delete_executor(be_id: str) -> None:
    """
    This function takes an executor id as input and deletes the corresponding executor.

    Args:
        be_id (str): The id of the executor to be deleted.
    """
    BenchmarkExecutor.delete_executor(be_id)


def api_get_all_executors() -> list[dict]:
    """
    This function retrieves all available executors and returns them as a list of dictionaries. Each dictionary
    represents an executor and contains its information.

    Returns:
        list[dict]: A list of dictionaries, each representing an executor.
    """
    _, executors = BenchmarkExecutor.get_available_executors()
    return [executor.to_dict() for executor in executors]


def api_get_all_executors_names() -> list[str]:
    """
    This function retrieves all available executor names and returns them as a list.

    Returns:
        list[str]: A list of executor names.
    """
    executors_names, _ = BenchmarkExecutor.get_available_executors()
    return executors_names


# def api_run_cookbooks(cookbooks, endpoints, num_of_prompts) -> dict:
#     """
#     Creates a cookbook run instance.

#     Returns:
#         dict: A dictionary representing the newly created cookbook run instance.
#     """
#     cookbook_run = Run(
#         RunTypes.COOKBOOK,
#         {
#             "cookbooks": cookbooks,
#             "endpoints": endpoints,
#             "num_of_prompts": num_of_prompts,
#         },
#     )

#     return cookbook_run


# def api_get_all_results() -> list:
#     """
#     This function retrieves a list of available results.

#     Returns:
#         list: A list of available results. Each item in the list represents a result.
#     """
#     return get_all_results()


# def api_read_results(results_filename: str) -> dict:
#     """
#     This function retrieves the contents of a results file.

#     Args:
#         results_filename: The file name of the results.

#     Returns:
#         dict: A dictionary of results.
#     """
#     return read_results(results_filename)


# def api_load_run(run_id: str) -> None:
#     """
#     Loads a run using the provided run ID.

#     Args:
#         run_id (str): The ID of the run to resume.
#     """
#     return Run.load_run(run_id)


# def api_get_prompt_templates() -> list:
#     """
#     Gets a list of prompt templates.
#     This static method retrieves a list of prompt templates available.

#     Returns:
#         list: A list of prompt templates.
#     """
#     return get_prompt_templates()


# def api_get_prompt_template_names() -> list:
#     """
#     Gets a list of prompt template names.
#     This method retrieves a list of prompt template names available.

#     Returns:
#         list: A list of prompt template names.
#     """
#     return get_prompt_template_names()


# def api_get_all_sessions() -> list:
#     """
#     This method retrieves a list of available sessions.

#     Returns:
#         list: A list of available sessions. Each item in the list represents a session.
#     """
#     return get_all_sessions()
