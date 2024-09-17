from celery import shared_task
import cdn
import os


def cleanup(file_path: str) -> None:
    os.remove(file_path)


@shared_task()
def transcode_and_upload_image(
    file_path: str, usercontent_dir: str, user_id: int, size: int
) -> None:
    os.system(
        f"ffmpeg -loglevel error -hide_banner -loop 0 -i {file_path} -y -vf scale={size}:{size} {usercontent_dir}img/rsz/{size}px/{user_id}.webp"
    )

    cdn.upload(
        f"{usercontent_dir}img/rsz/{size}px/{user_id}.webp",
        f"u1traspace/usercontent/img/rsz/{size}px/{user_id}.webp",
    )

    os.remove(f"{usercontent_dir}img/rsz/{size}px/{user_id}.webp")


@shared_task(link=transcode_and_upload_image)
def transcode_and_upload_images(
    file_path: str, usercontent_dir: str, user_id: int
) -> str:
    transcode_and_upload_image.delay(file_path, usercontent_dir, user_id, 32)
    transcode_and_upload_image.delay(file_path, usercontent_dir, user_id, 100)
    transcode_and_upload_image.delay(file_path, usercontent_dir, user_id, 200)

    cdn.upload(
        file_path,
        f"u1traspace/usercontent/img/raw/{user_id}.{file_path.split(".")[-1]}",
    )

    return file_path


@shared_task()
def transcode_and_upload_audio(
    file_path: str, usercontent_dir: str, user_id: int
) -> str:
    os.system(
        f"ffmpeg -loglevel error -i {file_path} -y {usercontent_dir}audio/{user_id}.mp3"
    )

    cdn.upload(
        f"{usercontent_dir}audio/{user_id}.mp3",
        f"u1traspace/usercontent/audio/{user_id}.mp3",
    )

    return file_path
