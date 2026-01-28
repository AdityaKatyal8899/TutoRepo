from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"Hi!": {'name': 'Aditya'}}

@app.get("/about")
def about():
    return {"Hi!": {'Page': "About"}}

