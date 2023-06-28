import uvicorn
from end_points import *

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)