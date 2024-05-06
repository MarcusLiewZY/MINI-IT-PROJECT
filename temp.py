# database seeding

class Campus(Enum):
    CYBERJAYA = "Cyberjaya"
    MALACCA = "Malacca"

# example
# user data
user_data = [
    {
        "email": # email address endwith .mmu.edu.my
        "username": # username
        "avatar_url": # avatar url, use https://source.unsplash.com/random/widthxheight
        "campus": # campus enum either CYBERJAYA or MALACCA
    },
    # add more user data
]

# post data
post_data = [
    {
        'title': # title of the post at most 120 characters
        'content': # content of the post
        'image_url': # image url, use https://source.unsplash.com/random/widthxheight, (maximum dimension = 800 x 800)
    },
    # add more post data
]

# tag data is prepared, dont need to change
# use this for the mapping of tags to post
tags = [
    {
        "name": "FCA",
        "color": "#FECACA",
        "description": "FCA description",
    },
    {
        "name": "FOL",
        "color": "#FED7AA",
        "description": "FOL description",
    },
    {
        "name": "FET",
        "color": "#FDE68A",
        "description": "FET description",
    },
    {
        "name": "FOE",
        "color": "#FEF08A",
        "description": "FOE description",
    },
    {
        "name": "FCI",
        "color": "#D9F99D",
        "description": "FCI description",
    },
    {
        "name": "ODL",
        "color": "#BBF7D0",
        "description": "ODL description",
    },
    {
        "name": "FIST",
        "color": "#A7F3D0",
        "description": "FIST description",
    },
    {
        "name": "FOM",
        "color": "#99F6E4",
        "description": "FOM description",
    },
    {
        "name": "FCM",
        "color": "#A5F3FC",
        "description": "FCM description",
    },
    {
        "name": "FAC",
        "color": "#BAE6FD",
        "description": "FAC description",
    },
    {
        "name": "FOB",
        "color": "#C7D2FE",
        "description": "FOB description",
    },
]


# comment data
comment_data = [
    {
        'content': # content of the comment (at least 2 paragraphs)
    },
    # add more comment data
]

# mappings

# user create post
# one to many relationship
# note that: since this is one to many relationship, the post_index is unique
user_create_post = [
    # 'user_index': ['post_index', 'post_index', 'post_index']
    1: [1, 2, 3],
    3: [4, 7]
]

# user create comment
# one to many relationship
# note that: since this is one to many relationship, the comment_index is unique
user_create_comment = [
    # 'user_index': ['comment_index', 'comment_index', 'comment_index']
    1: [1, 2, 3],
    3: [4, 7]
    # add more user create comment
]


# user like post  
# many to many relationship
# note that: since this is many to many relationship, the post_index can be repeated
user_like_post = [
    # 'user_index': ['post_index', 'post_index', 'post_index']
    1: [1, 2, 3],
    3: [1, 3, 5, 6],
    # add more user like post
]

# user bookmark post
# many to many relationship
# note that: since this is many to many relationship, the post_index can be repeated
user_bookmark_post = [
    # 'user_index': ['post_index', 'post_index', 'post_index']
    1: [1, 2, 3],
    3: [1, 5, 6],
    # add more user bookmark post
]

# user like comment
# many to many relationship
# note that: since this is many to many relationship, the comment_index can be repeated
user_like_comment = [
    # 'user_index': ['comment_index', 'comment_index', 'comment_index']
    1: [1, 2, 3],
    3: [1, 5, 6],
    # add more user like comment
]

# post tag
# many to many relationship
# note that: since this is many to many relationship, the post_index can be repeated
post_tag = [
    # 'post_index': ['tag_index', 'tag_index', 'tag_index']
    1: [1, 2, 3],
    3: [1, 5, 6],
    # add more post tag
]

# post comment

