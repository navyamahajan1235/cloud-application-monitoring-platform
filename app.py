from flask import Flask, jsonify, render_template_string, request
import logging
import psutil
import time

app = Flask(__name__)

@app.get("/healthz")
def healthz():
    return {"status": "healthy"}, 200

# -----------------------------
# Logging configuration
# -----------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

# -----------------------------
# Application metrics
# -----------------------------
start_time = time.time()
request_count = 0


@app.before_request
def track_request():
    global request_count
    request_count += 1
    request.start_time = time.time()


@app.after_request
def log_response(response):
    response_time = time.time() - request.start_time

    logger.info(
        "%s %s - %s - %.4fs",
        request.method,
        request.path,
        response.status_code,
        response_time
    )

    return response


# -----------------------------
# Home page
# -----------------------------
@app.route("/")
def home():
    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Cloud Application Monitoring Platform</title>

        <style>
            body {
                font-family: Arial, sans-serif;
                background: #f4f6f8;
                margin: 0;
                padding: 40px;
            }

            h1 {
                margin-bottom: 10px;
            }

            .subtitle {
                color: #666;
                margin-bottom: 30px;
            }

            .dashboard {
                display: grid;
                grid-template-columns: repeat(2, 1fr);
                gap: 20px;
                max-width: 900px;
            }

            .card {
                background: white;
                padding: 25px;
                border-radius: 12px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.08);
            }

            .label {
                color: #777;
                font-size: 14px;
            }

            .value {
                font-size: 28px;
                font-weight: bold;
                margin-top: 8px;
            }

            .healthy {
                color: green;
            }

            .links {
                margin-top: 30px;
            }

            a {
                margin-right: 20px;
            }
        </style>
    </head>

    <body>

        <h1>Cloud Application Monitoring Platform</h1>

        <div class="subtitle">
            Containerized application monitoring dashboard
        </div>

        <div class="dashboard">

            <div class="card">
                <div class="label">Application Status</div>
                <div class="value healthy">HEALTHY</div>
            </div>

            <div class="card">
                <div class="label">CPU Usage</div>
                <div class="value">{{ cpu }}%</div>
            </div>

            <div class="card">
                <div class="label">Memory Usage</div>
                <div class="value">{{ memory }}%</div>
            </div>

            <div class="card">
                <div class="label">Uptime</div>
                <div class="value">{{ uptime }}s</div>
            </div>

            <div class="card">
                <div class="label">Requests Served</div>
                <div class="value">{{ requests }}</div>
            </div>

        </div>

        <div class="links">
            <a href="/health">Health API</a>
            <a href="/metrics">Metrics API</a>
        </div>

    </body>
    </html>
    """,
    cpu=round(psutil.cpu_percent(interval=0.1), 2),
    memory=round(psutil.virtual_memory().percent, 2),
    uptime=round(time.time() - start_time, 2),
    requests=request_count
    )


# -----------------------------
# Health check endpoint
# -----------------------------
@app.route("/health")
def health():
    logger.info("Health check requested")

    return jsonify({
        "status": "healthy",
        "service": "cloud-monitoring-platform"
    })


# -----------------------------
# Metrics endpoint
# -----------------------------
@app.route("/metrics")
def metrics():

    uptime = time.time() - start_time

    return jsonify({
        "status": "healthy",
        "cpu_usage_percent": round(psutil.cpu_percent(interval=0.1), 2),
        "memory_usage_percent": round(psutil.virtual_memory().percent, 2),
        "uptime_seconds": round(uptime, 2),
        "request_count": request_count
    })


# -----------------------------
# Application startup
# -----------------------------
if __name__ == "__main__":

    logger.info("Starting Cloud Application Monitoring Platform")

    app.run(
        host="0.0.0.0",
        port=8000
    )