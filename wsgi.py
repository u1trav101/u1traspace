from flask import Flask
from flask_misaka import Misaka
from tasks import celery_init_app
from web import declare_routes, regex_replace
from config import CONFIG


app = Flask("u1traspace")

# applying configs from config class
app.config.from_object(CONFIG)

# initialising flask extensions
Misaka(app, autolink=True)

celery_app = celery_init_app(app)

# declaring jinja filters
app.add_template_filter(regex_replace)

# declaring the app URL endpoints
declare_routes(app)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=CONFIG.PORT)
