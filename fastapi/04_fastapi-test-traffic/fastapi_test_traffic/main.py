from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get('/home')
async def hello():
    return {'message':' Hello World'}


def main(): 
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

if __name__ == "__main__":
    main()