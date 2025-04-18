import base64

from flask import Flask, redirect, render_template, request, send_from_directory
import json
from lib.util import cast_args


class FlaskApp:
    def __init__(
        self,
        screens=None,
        on_change_screen=None,
        on_default_screen=None,
        on_turn_off_screen=None,
        get_current_screen=None,
    ):
        self.screens = screens
        self.on_change_screen = on_change_screen
        self.on_turn_off_screen = on_turn_off_screen
        self.on_default_screen = on_default_screen
        self.get_current_screen = get_current_screen

        self.flask_app = Flask(__name__)
        self.flask_app.route("/change_screen", methods=["POST"])(self.change_screen)
        self.flask_app.route("/default_screen", methods=["POST"])(self.default_screen)
        self.flask_app.route("/turn_off_screen", methods=["POST"])(self.turn_off_screen)
        self.flask_app.route("/list_screens", methods=["GET"])(self.list_screens)
        self.flask_app.route("/current_screen", methods=["GET"])(self.current_screen)

    def start(self):
        self.flask_app.run(host="0.0.0.0", port="3000")

    def change_screen(self):
        kwargs = cast_args(request.form.copy())
        screen_id = kwargs.pop("screen_id")

        if kwargs.get("display_indefinitely"):
            display_indefinitely = kwargs.pop("display_indefinitely")
        else:
            display_indefinitely = False

        if kwargs.get("duration"):
            try:
                duration = kwargs.pop("duration")
            except:
                duration = None
        else:
            duration = None

        self.on_change_screen(screen_id, kwargs, display_indefinitely, duration)
        return redirect("/")

    def default_screen(self):
        self.on_default_screen()
        return redirect("/")

    def turn_off_screen(self):
        self.on_turn_off_screen()
        return redirect("/")

    def pwa_manfiest(self):
        return send_from_directory("templates", "manifest.json")

    def list_screens(self):
        return json.dumps([screen["id"] for screen in self.screens])

    def current_screen(self):
        return json.dumps({"screen_id": self.get_current_screen()})
