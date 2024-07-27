from typing import Annotated

from fastapi import APIRouter, Response, HTTPException, status, File

from media.model import services


router = APIRouter()


@router.get("/image/{filename}", tags=["images"])
async def get_image(filename: str) -> Response:
    image = await services.get_image.perform(filename)

    if image is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND)

    if image.extension == "jpg":
        type_ = "jpeg"
    elif image.extension == "svg":
        type_ = "svg+xml"
    else:
        type_ = image.extension

    media_type = f"image/{type_}"
    return Response(content=image.content, media_type=media_type)


@router.post("/image/{filename}", tags=["images"])
async def post_image(
    filename: str,
    file_content: Annotated[bytes, File()],
) -> None:
    try:
        await services.put_image.perform(file_content, filename)
    except services.put_image.NotImageError as error:
        raise HTTPException(status.HTTP_400_BAD_REQUEST) from error


@router.put("/image/{filename}", tags=["images"])
async def put_image(
    filename: str,
    file_content: Annotated[bytes, File()],
) -> None:
    try:
        await services.put_image.perform(file_content, filename)
    except services.put_image.NotImageError as error:
        raise HTTPException(status.HTTP_400_BAD_REQUEST) from error


@router.delete("/image/{filename}", tags=["images"])
async def delete_image(filename: str) -> None:
    await services.remove_image.perform(filename)
