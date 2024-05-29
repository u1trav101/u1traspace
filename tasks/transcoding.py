from celery import shared_task
from config import CONFIG
import cdn
import os


@shared_task()
def _transcode_and_upload_image(file_path, usercontent_dir, user_id, size):
    os.system(f"ffmpeg -loglevel error -hide_banner -i {file_path} -filter_complex '[0:v] scale={size}:-1:flags=lanczos,split [a][b]; [a] palettegen=reserve_transparent=on:transparency_color=ffffff [p]; [b][p] paletteuse' -y {usercontent_dir}img/rsz/{size}px/{user_id}.gif")
    cdn.upload_image(
        f"{usercontent_dir}img/rsz/{size}px/{user_id}.gif",
        f"u1traspace/usercontent/img/rsz/{size}px/{user_id}.gif"
    )


@shared_task()
def transcode_and_upload_images(file_path, usercontent_dir, user_id):
    _transcode_and_upload_image.delay(file_path, usercontent_dir, user_id, 32)
    _transcode_and_upload_image.delay(file_path, usercontent_dir, user_id, 100)
    _transcode_and_upload_image.delay(file_path, usercontent_dir, user_id, 200)

    os.system(f"ffmpeg -loglevel error -hide_banner -i {file_path} -filter_complex '[0:v] scale=-1:-1:flags=lanczos,split [a][b]; [a] palettegen=reserve_transparent=on:transparency_color=ffffff [p]; [b][p] paletteuse' -y {usercontent_dir}img/raw/{user_id}.gif")
    cdn.upload_image(
        f"{usercontent_dir}img/raw/{user_id}.gif",
        f"u1traspace/usercontent/img/raw/{user_id}.gif"
    )


@shared_task()
def transcode_and_upload_audio(file_path, usercontent_dir, user_id):
    os.system(f"ffmpeg -loglevel error -i {file_path} -y {usercontent_dir}audio/{user_id}.mp3")
    cdn.upload_audio(
        f"{usercontent_dir}audio/{user_id}.mp3",
        f"u1traspace/usercontent/audio/{user_id}.mp3"
    )
