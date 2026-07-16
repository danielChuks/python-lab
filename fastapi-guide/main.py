from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()


class Post(BaseModel):
    id: int
    title: str
    content: str
    
class UpdatePost(BaseModel):
    title: str | None = None
    content: str | None = None

posts = [
    {"id": 1, "title": "First Post", "content": "This is the content of the first post."},
    {"id": 2, "title": "Second Post", "content": "This is the content of the second post."},
]

def _get_post_by_id(post_id: int):
    for post in posts:
        if post["id"] == post_id:
            return post
    return None

@app.get("/posts")
def get_posts():
    return posts


@app.get("/posts/{post_id}")
def get_post(post_id: int):
    post = _get_post_by_id(post_id)
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    print(f"Retrieving post: {post}")
    return {"data": "Post retrieved successfully", "post": post}


@app.post("/posts")
def create_post(post: Post):
    if _get_post_by_id(post.id) is not None:
        raise HTTPException(status_code=400, detail="Post with this ID already exists")
    post_dict = post.model_dump()
    posts.append(post_dict)
    return {"data": "Post created successfully", "post": post}

@app.put("/posts/{post_id}")
def update_post(post_id: int, updated_post: Post):
    post  =_get_post_by_id(post_id)
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    post.update(updated_post.model_dump())
    return {"data": "Post updated successfully", "post": post}

@app.delete("/posts/{post_id}")
def delete_post(post_id: int):
    post = _get_post_by_id(post_id)
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    posts.remove(post)
    return {"message": "Post deleted successfully"}

def main():
    return {"app": "Hello from fastapi-guide!"}


if __name__ == "__main__":
    main()
