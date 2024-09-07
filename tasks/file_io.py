from celery import shared_task
import cdn
import os


@shared_task
def save_css(corpus: str, usercontent_dir: str, user_id: int) -> None:
    with open(os.path.join(usercontent_dir, f"css/{user_id}.css"), "w") as f:
        f.write(corpus)
        
    cdn.upload_css(
        f"{usercontent_dir}css/{user_id}.css",
        f"u1traspace/usercontent/css/{user_id}.css"
    )
