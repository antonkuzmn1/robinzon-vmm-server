from contextlib import asynccontextmanager

from fastapi import FastAPI
import subprocess
import json

from fastapi.middleware.cors import CORSMiddleware


@asynccontextmanager
async def lifespan(_app: FastAPI):
    print("Server started!")
    yield
    print("Server stopped!")


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/view_vm_json.ps1")
def get_vms():
    command = "/home/vmmadmin/scripts/view_vm_json.ps1"

    result = subprocess.run(["pwsh", command], capture_output=True, text=True)

    if result.returncode != 0:
        return {"error": result.stderr}

    try:
        vms = json.loads(result.stdout)
    except json.JSONDecodeError as e:
        return {"error": f"JSON decode error: {e}"}

    return {"output": vms}
