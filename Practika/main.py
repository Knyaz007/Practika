import uvicorn
from endpoints import *

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000, reload=True)