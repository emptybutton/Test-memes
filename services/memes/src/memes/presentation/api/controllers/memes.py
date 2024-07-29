from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, HTTPException, status, UploadFile, Form

from memes.facade import services
from memes.presentation.api import views


router = APIRouter(tags=["memes"])


@router.get("/memes/{meme_id}")
async def read_meme(meme_id: UUID) -> views.success.MemeView:
    result = await services.read_meme.perform(meme_id)

    if result is None:
        raise views.failure.default_absence_view

    return views.success.MemeView(
        meme_id=result.meme_id,
        meme_text=result.meme_text,
    )


@router.get("/memes")
async def read_memes(page_number: int | None = None) -> views.success.MemeListView:
    try:
        result = await services.read_memes.perform(page_number)
    except services.read_memes.NegativePageNumberError as error:
        raise views.failure.negative_page_number_view from error

    page_memes = [
        views.success.MemeView(meme_id=dto.meme_id, meme_text=dto.meme_text)
        for dto in result.page_memes
    ]

    return views.success.MemeListView.of(page_memes, result.page_number)


@router.post("/memes")
async def create_meme(
    meme_text: Annotated[str, Form()],
    meme_image: UploadFile,
) -> views.success.MemeView:
    try:
        result = await services.add_meme.perform(
            meme_text,
            meme_image.filename,
            await meme_image.read(),
        )
    except services.add_meme.UnsupportedImageExtensionError as error:
        raise views.failure.bad_image_extension_view from error

    except services.add_meme.MediaIsNotWorkingError as error:
        raise views.failure.media_is_not_working_view from error

    return views.success.MemeView(
        meme_id=result.meme_id,
        meme_text=result.meme_text,
    )


@router.put("/memes/{meme_id}")
async def update_meme(
    meme_id: UUID,
    meme_text: Annotated[str, Form()],
    meme_image: UploadFile,
) -> views.success.MemeView:
    try:
        result = await services.update_meme.perform(
            meme_id,
            meme_text,
            meme_image.filename,
            await meme_image.read(),
        )
    except services.update_meme.NoMemeError as error:
        raise views.failure.default_absence_view from error

    except services.update_meme.MediaIsNotWorkingError as error:
        raise views.failure.media_is_not_working_view from error

    except services.update_meme.UnsupportedImageExtensionError as error:
        raise views.failure.bad_image_extension_view from error

    return views.success.MemeView(
        meme_id=result.meme_id,
        meme_text=result.meme_text,
    )


@router.delete("/memes/{meme_id}")
async def delete_meme(meme_id: UUID) -> None:
    try:
        await services.delete_meme.perform(meme_id)
    except services.delete_meme.NoMemeError as error:
        raise views.failure.default_absence_view from error
