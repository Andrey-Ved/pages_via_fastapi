from pathlib import Path
from typing import IO, Generator
from fastapi import Request


def ranged(
        file: IO[bytes],
        start: int = 0,
        end: int = None,
        block_size: int = 8192,
) -> Generator[bytes, None, None]:

    consumed = 0
    file.seek(start)

    while True:
        if end:
            data_length = min(
                block_size,
                end - start - consumed
            )
        else:
            data_length = block_size

        if data_length <= 0:
            break

        data = file.read(data_length)

        if not data:
            break

        consumed += data_length

        yield data

    if hasattr(file, 'close'):
        file.close()


async def open_video_file(
        request: Request,
        file_name: str
) -> tuple:

    path = Path("static/video/" + file_name)

    file = path.open('rb')
    file_size = path.stat().st_size

    content_length = file_size

    headers = {}
    status_code = 200
    content_range = request.headers.get('range')

    if content_range is not None:
        content_range = content_range.strip().lower()
        content_ranges = content_range.split('=')[-1]

        range_start, range_end, *_ = map(
            str.strip,
            (content_ranges + '-').split('-')
        )

        if range_start:
            range_start = max(
                0,
                int(range_start)
            )
        else:
            range_start = 0

        if range_end:
            range_end = min(
                file_size - 1,
                int(range_end)
            )
        else:
            range_end = file_size - 1

        content_length = (range_end - range_start) + 1

        file = ranged(
            file,
            start=range_start,
            end=range_end + 1
        )

        status_code = 206
        headers['Content-Range'] = f'bytes {range_start}-{range_end}/{file_size}'

    return (
        file,
        status_code,
        content_length,
        headers
    )

print('init video services')
