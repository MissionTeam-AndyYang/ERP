# coding=utf8
import os

class CConfig:

    HOST=os.getenv("FLASK_HOST","0.0.0.0")

    PORT=int(
        os.getenv("FLASK_PORT",5000)
    )

    DEBUG=(
        os.getenv(
            "FLASK_DEBUG",
            "False"
        ).lower()=="true"
    )