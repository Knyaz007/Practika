import uvicorn
from api import *

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)