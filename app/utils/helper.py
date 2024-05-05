import requests
from cloudinary import uploader as cloudinary_uploader
from datetime import datetime
from werkzeug.datastructures import FileStorage


def format_datetime(value: datetime) -> str:
    return value.strftime("%Y-%m-%d %H:%M:%S")


def parse_datetime(value: str) -> datetime:
    return datetime.strptime(value, "%Y-%m-%d %H:%M:%S")


def upload_image(image, folder_name):
    try:
        if isinstance(image, FileStorage):
            upload_result = cloudinary_uploader.upload(
                image, resource_type="image", folder=folder_name
            )
        else:
            response = requests.get(image, stream=True)
            response.raw.decode_content = True
            upload_result = cloudinary_uploader.upload(
                response.raw, resource_type="image", folder=folder_name
            )
        return upload_result["secure_url"]
    except Exception as e:
        print(e)
        return None
