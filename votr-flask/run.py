# -*- coding: utf-8 -*-
"""Create an application instance."""
from votr_flask.app import create_app
from flask import Flask

app = create_app()


if __name__ == "__main__":
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True)
