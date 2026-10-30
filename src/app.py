# THE WEBSITE - A SMALL FLASK SERVER THAT RUNS ON YOUR OWN COMPUTER
# 1. SERVE THE PAGE (static/index.html)
# 2. START A SUMMARY IN THE BACKGROUND WHEN A LINK IS SUBMITTED
# 3. THE PAGE ASKS FOR PROGRESS EVERY SECOND UNTIL IT IS DONE
# Run with: python src/app.py   (or double-click run.bat)

import sys
import threading
import uuid
import webbrowser

from flask import Flask, jsonify, request

from config import has_openai_key
from pipeline import summarize_video
from transcribe import load_model

HOST = "127.0.0.1"
PORT = 5000

app = Flask(__name__, static_folder="static", static_url_path="")

jobs = {}
#whisper uses all CPU cores, so summaries run one at a time
run_lock = threading.Lock()


def run_job(job, url):
    def report(event, **data):
        if event == "step":
            job["step"] = data["step"]
        elif event == "video":
            job["video"] = data["video"]
        elif event == "method":
            job.update(method=data["method"], device=data.get("device"), source=data.get("source"), percent=None)
        elif event == "progress":
            job["percent"] = data["percent"]

    with run_lock:
        job["status"] = "running"
        try:
            result = summarize_video(url, report)
            job.update(status="done", step=None, **result)
        except Exception as e:
            job.update(status="error", error=str(e))


@app.get("/")
def index():
    return app.send_static_file("index.html")


@app.get("/api/status")
def status():
    return jsonify(has_key=has_openai_key())


@app.post("/api/summarize")
def start_summary():
    url = (request.get_json(silent=True) or {}).get("url", "").strip()
    if not url:
        return jsonify(error="Paste a YouTube link first."), 400
    if not has_openai_key():
        return jsonify(error="No OpenAI API key found. Add it to the .env file, then try again."), 400

    job_id = uuid.uuid4().hex
    jobs[job_id] = {"id": job_id, "status": "queued", "step": None, "method": None, "percent": None, "video": None}
    threading.Thread(target=run_job, args=(jobs[job_id], url), daemon=True).start()
    return jsonify(id=job_id)


@app.get("/api/jobs/<job_id>")
def job_status(job_id):
    job = jobs.get(job_id)
    if job is None:
        return jsonify(error="Unknown job."), 404
    return jsonify(job)


if __name__ == "__main__":
    #load whisper in the background so the first summary starts faster
    threading.Thread(target=load_model, daemon=True).start()

    url = f"http://{HOST}:{PORT}"
    print(f"YT-Summary is running at {url}  (close this window to stop it)")
    if "--no-browser" not in sys.argv:
        threading.Timer(1.0, webbrowser.open, args=(url,)).start()
    app.run(host=HOST, port=PORT, threaded=True)
