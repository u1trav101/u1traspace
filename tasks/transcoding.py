from celery import shared_task
import cdn
import os


@shared_task()
def _transcode_and_upload_image(file_path: str, usercontent_dir: str, user_id: int, size: int) -> None:
    os.system(f"ffmpeg -loglevel error -hide_banner -loop 0 -i {file_path} -y -vf scale={size}:{size} {usercontent_dir}img/rsz/{size}px/{user_id}.webp")
    cdn.upload_image(
        f"{usercontent_dir}img/rsz/{size}px/{user_id}.webp",
        f"u1traspace/usercontent/img/rsz/{size}px/{user_id}.webp"
    )


@shared_task()
def transcode_and_upload_images(file_path: str, usercontent_dir: str, user_id: int) -> None:
    _transcode_and_upload_image.delay(file_path, usercontent_dir, user_id, 32)
    _transcode_and_upload_image.delay(file_path, usercontent_dir, user_id, 100)
    _transcode_and_upload_image.delay(file_path, usercontent_dir, user_id, 200)

    print(file_path)
    print(file_path.split(".")[-1])
    cdn.upload_image(
        file_path,
        f"u1traspace/usercontent/img/raw/{user_id}.{file_path.split(".")[-1]}"
    )


@shared_task()
def transcode_and_upload_audio(file_path: str, usercontent_dir: str, user_id: int) -> None:
    os.system(f"ffmpeg -loglevel error -loop 0 -i {file_path} -y {usercontent_dir}audio/{user_id}.mp3")
    cdn.upload_audio(
        f"{usercontent_dir}audio/{user_id}.mp3",
        f"u1traspace/usercontent/audio/{user_id}.mp3"
    )
