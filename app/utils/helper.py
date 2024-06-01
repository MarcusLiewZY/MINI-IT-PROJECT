import requests
from cloudinary import uploader as cloudinary_uploader
from datetime import datetime
from werkzeug.datastructures import FileStorage
import humanize


def format_datetime(value: datetime) -> str:
    return value.strftime("%Y-%m-%d %H:%M:%S")


def parse_datetime(value: str) -> datetime:
    return datetime.strptime(value, "%Y-%m-%d %H:%M:%S")


def getTimeAgo(time: datetime) -> str:
    return humanize.naturaltime(time)


def upload_image(image, folder_name):
    print(type(image))
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


def delete_image(image_url: str) -> bool:
    try:
        public_id = image_url.split("/")[-1].split(".")[0]
        cloudinary_uploader.destroy(public_id, invalidate=True)
        return True
    except Exception as e:
        print(e)
        return False
