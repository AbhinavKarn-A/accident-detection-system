from flask import Flask, render_template, request, redirect, Response
from detector import generate_frames, generate_cctv_frames

app = Flask(__name__)

USERNAME = "admin"
PASSWORD = "12345"

vehicle_count = 0
accident_count = 0
warning_count = 0


@app.route("/", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        if username == USERNAME and password == PASSWORD:

            return redirect("/dashboard")

    return render_template("login.html")


@app.route("/dashboard")
def dashboard():

    return render_template(
        "dashboard.html",
        vehicles=vehicle_count,
        accidents=accident_count,
        warnings=warning_count
    )


@app.route("/video")
def video():

    return render_template("video.html")


@app.route("/cctv_feed")
def cctv_feed():

    return Response(
        generate_cctv_frames(),
        mimetype='multipart/x-mixed-replace; boundary=frame'
    )


@app.route("/analytics")
def analytics():

    return render_template("analytics.html")


@app.route("/logs")
def logs():

    return render_template("logs.html")


@app.route("/video_feed")
def video_feed():

    return Response(
        generate_frames(),
        mimetype="multipart/x-mixed-replace; boundary=frame"
    )


if __name__ == "__main__":

    app.run(debug=True)