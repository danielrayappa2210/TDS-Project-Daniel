import logging
from app.phase_a_tasks import *
from app.phase_b_tasks import *
from app.filter_csv import *
from app.llm_utils import *
from app.function_description import *
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import json
import re

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

DATA_DIR = "data"
def is_safe(path):
    if path.startswith('/'):
        path = path.strip('/')
    return path.startswith(DATA_DIR)

def agent(input_str,tools):
    logging.info(f"Initial task: {input_str}")
    response = query_gpt(input_str, tools)
    function_call_details = [tool_call["function"] for tool_call in response["tool_calls"]][0]
    logging.info(f"Function details loaded: {function_call_details}")

    # Checkinf task requires deletion of any file
    if function_call_details['name'] == "delete_file":
        return 1
    elif len(function_call_details)>0:
        try:
            arguments = json.loads(function_call_details['arguments'])
            for arg_name, arg_val in arguments.items():
                if ("dir" in arg_name) or ("path" in arg_name):
                    if not is_safe(arg_val):
                        return 2 # 400 bad request, access restricted, invalie input/output path
            func = globals()[function_call_details['name']]
            logging.info(f"Executing: {func}")
            _ = func(**arguments)
            return {func:arguments}
        except Exception as e:
            return 4 # 500 Internal server error, error in function call
    else:
        return 5 # 400 bad request unknow task request
    
app = FastAPI()

# Add CORS middleware to allow requests from anywhere
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

class InputData(BaseModel):
    input_str: str

@app.post("/run")
async def agent_post_endpoint(task: str):
    if not task:
        raise HTTPException(status_code=400, detail="No task description provided")
    
    result = agent(task, task_tools)
    if result == 1:
        logging.info("Bad request, Files cannot be deleted")
        raise HTTPException(status_code=400, detail="Bad request, Files cannot be deleted")
    elif result == 2:
        logging.info("Bad request, access restricted for the input/output path")
        raise HTTPException(status_code=400, detail="Bad request, access restricted for the input/output path")
    elif isinstance(result,dict):
        logging.info("Task executed successfully")
        return JSONResponse(content={"detail": "Task executed successfully"}, status_code=200)
    elif result == 4:
        logging.info("Internal server error, could not complete the task")
        raise HTTPException(status_code=500, detail="Internal server error, could not complete the task")
    else:
        logging.info("unknown task description/description not clear")
        raise HTTPException(status_code=400, detail="Bad request, unknown task description/description not clear")

@app.get("/read")
async def get_file_details(path: str):
    try:
        with open(path, 'r') as file:
            content = file.read()
        logging.info("File read succesfully")
        return JSONResponse(content={'file_content': content}, status_code=200)
    except FileNotFoundError:
        logging.info("File not found")
        raise HTTPException(status_code=404, detail="File not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/run")
async def run_agent_with_filter(task: str):
    if not task:
        raise HTTPException(status_code=400, detail="No task description provided")

    result = agent(task, filter_csv_tool)
    if result == 1:
        logging.info("Bad request, Files cannot be deleted")
        raise HTTPException(status_code=400, detail="Bad request, Files cannot be deleted")
    elif result == 2:
        logging.info("Bad request, access restricted for the input/output path")
        raise HTTPException(status_code=400, detail="Bad request, access restricted for the input/output path")
    elif isinstance(result,dict):
        logging.info("Task executed successfully")
        func, args = list(result.items())[0]
        return func(**args)
    elif result == 4:
        logging.info("Internal server error, could not complete the task")
        raise HTTPException(status_code=500, detail="Internal server error, could not complete the task")
    else:
        logging.info("unknown task description/description not clear")
        raise HTTPException(status_code=400, detail="Bad request, unknown task description/description not clear")