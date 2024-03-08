from fastapi import APIRouter, Depends, HTTPException
from dependency_injector.wiring import inject, Provide

from web_api.schemas.cookbook_create_dto import CookbookCreateDTO
from web_api.schemas.cookbook_executor_create_dto import CookbookExecutorCreateDTO
from web_api.schemas.endpoint_create_dto import EndpointCreateDTO
from web_api.schemas.recipe_executor_create_dto import RecipeExecutorCreateDTO
from ..container import Container
from ..schemas.endpoint_response_model import EndpointDataModel
from ..schemas.recipe_create_dto import RecipeCreateDTO
from ..services.benchmarking_service import BenchmarkingService
from ..services.utils.exceptions_handler import SessionException
from typing import Any, Optional


router = APIRouter()

@router.get("/v1/llm_endpoints")
@inject
def get_all_endpoints(
    benchmarking_service: BenchmarkingService = Depends(Provide[Container.benchmarking_service])
) -> list[Optional[EndpointDataModel]]:
    """
    Get all the endpoints from the database
    """
    try: 
        return benchmarking_service.get_all_endpoints()
    except SessionException as e:
        if e.error_code == "FileNotFound":
            raise HTTPException(status_code=404, detail=f"Failed to get endpoint: {e.msg}")
        elif e.error_code == "ValidationError":
            raise HTTPException(status_code=400, detail=f"Failed to get endpoint: {e.msg}")
        else:
            raise HTTPException(status_code=500, detail=f"Failed to get endpoint: {e.msg}")    

@router.post("/v1/llm_endpoints")
@inject
def add_new_endpoint(
    endpoint_data: EndpointCreateDTO,
    benchmarking_service: BenchmarkingService = Depends(Provide[Container.benchmarking_service])
) -> dict[str, str] | tuple[dict[str, str], int]:
    """
    Add a new endpoint to the database
    """
    try:
        benchmarking_service.add_endpoint(endpoint_data)
        return {"message": "Endpoint added successfully"}
    except SessionException as e:
        if e.error_code == "FileNotFound":
            raise HTTPException(status_code=404, detail=f"Failed to add endpoint: {e.msg}")
        elif e.error_code == "ValidationError":
            raise HTTPException(status_code=400, detail=f"Failed to add endpoint: {e.msg}")
        else:
            raise HTTPException(status_code=500, detail=f"Failed to add endpoint: {e.msg}")    

@router.delete("/v1/llm_endpoints/{endpoint_id}")
@inject
async def delete_endpoint(
    endpoint_id: str,
    benchmarking_service: BenchmarkingService = Depends(Provide[Container.benchmarking_service])
    ) -> dict[str, str] | tuple[dict[str, str], int]:
    try:
        benchmarking_service.delete_endpoint(endpoint_id)
        return {"message": "Endpoint deleted successfully"}
    except SessionException as e:
        if e.error_code == "FileNotFound":
            raise HTTPException(status_code=404, detail=f"Failed to delete endpoint: {e.msg}")
        elif e.error_code == "ValidationError":
            raise HTTPException(status_code=400, detail=f"Failed to delete endpoint: {e.msg}")
        else:
            raise HTTPException(status_code=500, detail=f"Failed to delete endpoint: {e.msg}")   
    
@router.get("/v1/connectors")
@inject
def get_all_connectors(benchmarking_service: BenchmarkingService = Depends(Provide[Container.benchmarking_service])): 
    #TODO - type check and model validation
    return benchmarking_service.get_all_connectors()

@router.get("/v1/recipes")
@inject
def get_all_recipes(benchmarking_service: BenchmarkingService = Depends(Provide[Container.benchmarking_service])):
    try:
        return benchmarking_service.get_all_recipes()
    except SessionException as e:
        if e.error_code == "FileNotFound":
            raise HTTPException(status_code=404, detail=f"Failed to retrieve recipes: {e.msg}")
        elif e.error_code == "ValidationError":
            raise HTTPException(status_code=400, detail=f"Failed to retrieve recipes: {e.msg}")
        else:
            raise HTTPException(status_code=500, detail=f"Failed to retrieve recipes: {e.msg}")   

@router.post("/v1/recipes")
@inject
def create_recipe(
    recipe_data: RecipeCreateDTO,
    benchmarking_service: BenchmarkingService = Depends(Provide[Container.benchmarking_service])
    ):
    try:
        benchmarking_service.create_recipe(recipe_data)
        return {"message": "Recipe created successfully"}
    except SessionException as e:
        if e.error_code == "FileNotFound":
            raise HTTPException(status_code=404, detail=f"Failed to create recipe: {e.msg}")
        elif e.error_code == "ValidationError":
            raise HTTPException(status_code=400, detail=f"Failed to create recipe: {e.msg}")
        else:
            raise HTTPException(status_code=500, detail=f"Failed to create recipe: {e.msg}")    

@router.delete("/v1/recipes/{recipe_id}")
@inject
async def delete_recipe(
    recipe_id: str,
    benchmarking_service: BenchmarkingService = Depends(Provide[Container.benchmarking_service])
    ) -> dict[str, str] | tuple[dict[str, str], int]:

    try:
        benchmarking_service.delete_recipe(recipe_id)
        return {"message": "Recipe deleted successfully"}
    except SessionException as e:
        if e.error_code == "FileNotFound":
            raise HTTPException(status_code=404, detail=f"Failed to delete recipe: {e.msg}")
        elif e.error_code == "ValidationError":
            raise HTTPException(status_code=400, detail=f"Failed to delete recipe: {e.msg}")
        else:
            raise HTTPException(status_code=500, detail=f"Failed to delete recipe: {e.msg}")    
    

@router.post("/v1/cookbooks")
@inject
def create_cookbook(
    cookbook_data: CookbookCreateDTO,
    benchmarking_service: BenchmarkingService = Depends(Provide[Container.benchmarking_service])
    ):
    try:
        benchmarking_service.create_cookbook(cookbook_data)
        return {"message": "Cookbook created successfully"}
    except SessionException as e:
        if e.error_code == "FileNotFound":
            raise HTTPException(status_code=404, detail=f"Failed to create cookbook: {e.msg}")
        elif e.error_code == "ValidationError":
            raise HTTPException(status_code=400, detail=f"Failed to create cookbook: {e.msg}")
        else:
            raise HTTPException(status_code=500, detail=f"Failed to create cookbook: {e.msg}")    


@router.get("/v1/cookbooks")
@inject
def get_all_cookbooks(
    benchmarking_service: BenchmarkingService = Depends(Provide[Container.benchmarking_service])
    ):
    try:
        cookbooks = benchmarking_service.get_all_cookbooks()
        return cookbooks
    except SessionException as e:
        if e.error_code == "FileNotFound":
            raise HTTPException(status_code=404, detail=f"Failed to retrieve cookbook: {e.msg}")
        elif e.error_code == "ValidationError":
            raise HTTPException(status_code=400, detail=f"Failed to retrieve cookbook: {e.msg}")
        else:
            raise HTTPException(status_code=500, detail=f"Failed to retrieve cookbook: {e.msg}")    
    
@router.get("/v1/cookbooks/{cookbook_id}")
@inject
def get_cookbook_by_id(
    cookbook_id: str,
    benchmarking_service: BenchmarkingService = Depends(Provide[Container.benchmarking_service])):
    try:
        cookbook = benchmarking_service.get_cookbook_by_id(cookbook_id)
        return cookbook
    except SessionException as e:
        return {"message": f"Unable to get cookbook: {e}"}, 500
    
@router.put("/v1/cookbooks/{cookbook_id}")
@inject
def update_cookbook(
    cookbook_id: str,
    cookbook_data: CookbookCreateDTO,
    benchmarking_service: BenchmarkingService = Depends(Provide[Container.benchmarking_service])):
    try:
        benchmarking_service.update_cookbook(cookbook_data, cookbook_id)
        return {"message": "Cookbook updated successfully"}
    except SessionException as e:
        if e.error_code == "FileNotFound":
            raise HTTPException(status_code=404, detail=f"Failed to update cookbook: {e.msg}")
        elif e.error_code == "ValidationError":
            raise HTTPException(status_code=400, detail=f"Failed to update cookbook: {e.msg}")
        else:
            raise HTTPException(status_code=500, detail=f"Failed to update cookbook: {e.msg}")    

# TODO - create cookbook executor should not be a route - the route will probably be high level 'run benchmark' then the executor is created and run by calling a series of ms lib apis
@router.post("/v1/execute/cookbook")
@inject
def cookbook_executor(
    cookbook_executor_data: CookbookExecutorCreateDTO,
    benchmarking_service: BenchmarkingService = Depends(Provide[Container.benchmarking_service])):
    try:
        benchmarking_service.execute_cookbook(cookbook_executor_data)
        return {"message": "Cookbook executed successfully"}
    except SessionException as e:
        return {"message": f"Unable to execute cookbook: {e}"}, 500
    
@router.post("/v1/execute/recipe")
@inject
def recipe_executor(
    recipe_executor_data: RecipeExecutorCreateDTO,
    benchmarking_service: BenchmarkingService = Depends(Provide[Container.benchmarking_service])):
    try:
        benchmarking_service.execute_recipe(recipe_executor_data)
        return {"message": "Recipe executed successfully"}
    except SessionException as e:
        return {"message": f"Unable to execute recipe: {e}"}, 500
    
