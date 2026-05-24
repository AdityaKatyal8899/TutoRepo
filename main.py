from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
app = FastAPI()


class Blog(BaseModel):
    title: str
    text: str
    published: Optional[bool]

print("Example Text")

@app.get("/")
def root():
    return {"Hi!": {'data': 'Home Page'}}


@app.get("/about")
def about():
    return {"Hi!": {'Page': "About"}}


@app.post("/blog")
def blog_post(blog: Blog):
    return {"Message": {"data": {"title": blog.title, "text": blog.text, "Is availabel": "Yes" if blog.published else "No"}}} 


@app.get("/blog/{blog_id}")
def give_blog(blog_id: int, username: str, published: bool):

    if published:
        return {"Blogs": {"id": blog_id, "Username": username, "IS availabel": "Yes! This blog is published"}}
    
    else: 
        return {"Blogs": {"id": blog_id, "Username": username, "IS availabel": "No! This blog isn't published"}}



@app.get("/blog/{blog_id}/comments")
def give_blog_data(blog_id: int):
    return {"Blogs": {"id": blog_id, "data": f"comments on blog {blog_id}"},}

