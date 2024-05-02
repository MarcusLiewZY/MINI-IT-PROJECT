from datetime import datetime

posts = [
    {
        "title": "Post The First",
        "content": "Content for the first post",
        "image_url": "https://via.placeholder.com/200x300",
        "created_at": datetime.now(),
    },
    {
        "title": "Post The Second",
        "content": "Content for the second post",
        "image_url": "https://via.placeholder.com/150x500",
        "created_at": datetime.now(),
    },
    {
        "title": "Post The Third",
        "content": "Content for the third post",
        "image_url": "https://via.placeholder.com/400x700",
        "created_at": datetime.now(),
    },
]

tags = [
    {
        "name": "FOE",
        "color": "#7dd3fc",
        "description": "Tag for posts about animals",
        "created_at": datetime.now(),
    },
    {
        "name": "FIST",
        "color": "#86efac",
        "description": "Tag for posts about tech",
        "created_at": datetime.now(),
    },
    {
        "name": "FCI",
        "color": "#fef08a",
        "description": "Tag for posts about cooking",
        "created_at": datetime.now(),
    },
    {
        "name": "FCA",
        "color": "#fda4af",
        "description": "Tag for posts about writing",
        "created_at": datetime.now(),
    },
]


post = {
    "title": "Post The First",
    "content": "Content for the first post",
    # "image_url": "https://via.placeholder.com/200x300",
    # "tags": ["FOE", "FIST"],
}
