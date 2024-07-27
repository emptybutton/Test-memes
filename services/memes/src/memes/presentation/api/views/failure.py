from fastapi import HTTPException, status


default_absence_view = HTTPException(status.HTTP_404_NOT_FOUND)

bad_image_extension_view = HTTPException(
    status.HTTP_400_BAD_REQUEST,
    [{
        "msg": "file extension is not supported",
        "type": "BadImageExtension",
    }],
)

media_is_not_working_view = HTTPException(
    status.HTTP_503_SERVICE_UNAVAILABLE,
    [{
        "msg": "try later",
        "type": "Unavailable",
    }],
)

negative_page_number_view = HTTPException(
    status.HTTP_400_BAD_REQUEST,
    [{
        "msg": "`page_number` must be greater than 0",
        "type": "NegativePageNumber",
    }],
)
