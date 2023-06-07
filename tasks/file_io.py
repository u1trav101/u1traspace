from celery import shared_task
import cdn
import os


@shared_task
def save_css(corpus, usercontent_dir, user_id):
    with open(os.path.join(usercontent_dir, f"css/{user_id}.css"), "w") as f:
        f.write(corpus)
        

    cdn.upload_css(
        f"{usercontent_dir}css/{user_id}.css",
        f"usercontent/css/{user_id}.css"
    )
