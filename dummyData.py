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
        "avatar_url": # avatar url, use https://source.unsplash.com/random/widthxheight (dimension: 80 X 80)
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
