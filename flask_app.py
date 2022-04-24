from flask import (Flask, redirect, render_template, request,
                   send_from_directory)


class FlaskApp:
  def __init__(self, screens=None, on_change_screen=None, on_turn_off_screen=None):
    self.screens = screens
    self.on_change_screen = on_change_screen
    self.on_turn_off_screen = on_turn_off_screen

    self.flask_app = Flask(__name__)
    self.flask_app.route("/")(self.index)
    self.flask_app.route("/change_screen", methods=["POST"])(
        self.change_screen
    )
    self.flask_app.route("/turn_off_screen", methods=["POST"])(
        self.turn_off_screen
    )
    self.flask_app.route("/manifest.json")(self.pwa_manfiest)

  def start(self):
    self.flask_app.run(host="0.0.0.0", port="3000")

  def index(self):
    return render_template("index.html", screens=self.screens)

  def change_screen(self):
    screen_id = request.form["screen_id"]
    self.on_change_screen(screen_id)
    return redirect("/")

  def turn_off_screen(self):
    self.on_turn_off_screen()
    return redirect("/")

  def pwa_manfiest(self):
    return send_from_directory("templates", "manifest.json")
