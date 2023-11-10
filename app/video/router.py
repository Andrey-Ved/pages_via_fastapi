from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse

from app.video.services import open_video_file


router = APIRouter()


@router.get("/{video_name}")
async def get_streaming_video(
        request: Request,
        video_name: str
) -> StreamingResponse:

    (
        file,
        status_code,
        content_length,
        headers
    ) = await open_video_file(request, video_name)

    response = StreamingResponse(
        file,
        media_type='video/mp4',
        status_code=status_code,
    )

    response.headers.update({
        'Accept-Ranges': 'bytes',
        'Content-Length': str(content_length),
        **headers,
    })

    return response


print('init video routers')
