from flask import Flask
from flask import redirect
from flask import render_template
from flask import request
from flask import jsonify
from flask import session
from flask import url_for
import userManagement as dbHandler
import pandas as pd

# import pyotp
# import pyqrcode
# import os
# import base64
# from io import BytesIO
# import requests
from flask_wtf import CSRFProtect
from flask_csp.csp import csp_header
import logging
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

import userManagement as dbHandler

# Code snippet for logging a message
# app.logger.critical("message")

app_log = logging.getLogger(__name__)
logging.basicConfig(
    filename="security_log.log",
    encoding="utf-8",
    level=logging.DEBUG,
    format="%(asctime)s %(message)s",
)


# Generate a unique basic 16 key: https://acte.ltd/utils/randomkeygen
app = Flask(__name__)
app.secret_key = b"_53oi3uriq9pifpff;apl"

csrf = CSRFProtect(app)
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://",
)


# Redirect index.html to domain root for consistent UX
@app.route("/index", methods=["GET"])
@app.route("/index.htm", methods=["GET"])
@app.route("/index.asp", methods=["GET"])
@app.route("/index.php", methods=["GET"])
@app.route("/index.html", methods=["GET"])
def root():
    return redirect("/", 302)


@app.route("/", methods=["POST", "GET"])
@csp_header(
    {
        # Server Side CSP is consistent with meta CSP in layout.html
        "base-uri": "'self'",
        "default-src": "'self'",
        "style-src": "'self'",
        "script-src": "'self'",
        "img-src": "'self' data:",
        "media-src": "'self'",
        "font-src": "'self'",
        "object-src": "'self'",
        "child-src": "'self'",
        "connect-src": "'self'",
        "worker-src": "'self'",
        "report-uri": "/csp_report",
        "frame-ancestors": "'none'",
        "form-action": "'self'",
        "frame-src": "'none'",
    }
)
def index():
    return render_template("/index.html")


@app.route("/privacy.html", methods=["GET"])
def privacy():
    return render_template("/privacy.html")


@app.route("/form_login.html", methods=["POST", "GET"])
@limiter.limit("1/second", override_defaults=False)
def login():
    if request.method == "POST":
        global user
        user = request.form.get("user", "").strip()
        pwd = request.form.get("password", "")
        if dbHandler.loginput(user, pwd):
            session["login"] = True
            session["user"] = user
            return redirect("/index.html")
            # CODE FOR UNFINISHED 2FA
            # return redirect("/2_factor_auth.html")
        else:
            print("Username or password is incorrect.")
            return render_template("/form_login.html")
    else:
        return render_template("/form_login.html")


@app.route("/logout.html", methods=["GET"])
@limiter.limit("1/second", override_defaults=False)
def logout():
    session.clear()
    return redirect("/form_login.html")


@app.route("/form_signup.html", methods=["POST", "GET"])
@limiter.limit("1/second", override_defaults=False)
def signup():
    if request.method == "POST":
        user = request.form.get("user", "").strip()
        pwd = request.form.get("password", "")
        if dbHandler.signupinput(user, pwd):
            return redirect("/form_login.html")
        else:
            print(
                "Unable to sign up. Username may already be taken, or there was an error on our end."
            )
            return render_template(
                "/form_signup.html",
            )
    else:
        return render_template("/form_signup.html")


@app.route("/form_devlog.html", methods=["POST", "GET"])
@limiter.limit("1/second", override_defaults=False)
def cosup():
    if request.method == "POST":
        try:
            developer = request.form.get("developer").strip()
            project = request.form.get("project").strip()
            start = request.form.get("start").strip()
            end = request.form.get("end").strip()
            diarytime = request.form.get("diarytime").strip()
            worktime = request.form.get("worktime").strip()
            repo = request.form.get("repo").strip()
            notes = request.form.get("notes").strip()
            if not session.get("login") or not session.get("user"):
                print("not logged inn")
                return render_template("/form_devlog.html")
            if dbHandler.devlogadd(
                user, developer, project, start, end, diarytime, worktime, repo, notes
            ):
                return redirect("/devlogs.html")
            else:
                print(
                    "Unable to add devlog. Either you haven't submitted everything or this was an error on our end."
                )
                return render_template(
                    "/form_devlog.html",
                )
        except NameError:
            print("bleghhhh :P (not logged in)")
            return render_template("/form_devlog.html")
    else:
        return render_template("/form_devlog.html")


@app.route("/devlogs.html", methods=["POST", "GET"])
def tanup():
    devlogs = dbHandler.getdata()
    if request.method == "POST":
        searchdata = request.form.get("devlog_search", "").strip()
        # searchlog = request.form.get("search_option")
        # print(searchlog)
        logs = dbHandler.devlogsearch(searchdata)
        if logs:
            print(logs)
            print("search success")
            return render_template("/devlogs.html")
        else:
            return render_template("/devlogs.html")
    else:
        return render_template("/devlogs.html")


# @app.route("/2_factor_auth.html", methods=["POST", "GET"])
# def home():
#    user_secret = pyotp.random_base32()
#    totp = pyotp.TOTP(user_secret)
#    otp_uri = totp.provisioning_uri(name=user, issuer_name="YourAppName")
#    qr_code = pyqrcode.create(otp_uri)
#    stream = BytesIO()
#    qr_code.png(stream, scale=5)
#    qr_code_b64 = base64.b64encode(stream.getvalue()).decode("utf-8")
#    otp_input = request.form["otp"]
#    if request.method == "POST":
#        otp_input = request.form["otp"]
#    if totp.verify(otp_input):
#        session["login"] = True
#        session["user"] = user
#        return redirect("index.html")
#    else:
#        return render_
#    return render_template("/login.html")


# Endpoint for logging CSP violations
@app.route("/csp_report", methods=["POST"])
@csrf.exempt
def csp_report():
    app.logger.critical(request.data.decode())
    return "done"


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
