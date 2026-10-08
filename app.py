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

        <meta name="viewport" content="width=device-width, initial-scale=1.0">

        <style>
            * {
                box-sizing: border-box;
            }

            body {
                margin: 0;
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI",
                             Roboto, Arial, sans-serif;
                background: #0b1120;
                color: #e5e7eb;
            }

            .container {
                max-width: 1200px;
                margin: auto;
                padding: 40px 28px;
            }

            /* Header */
            .header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 35px;
                gap: 20px;
            }

            .title-section h1 {
                margin: 0;
                font-size: 32px;
                letter-spacing: -0.5px;
            }

            .subtitle {
                margin-top: 8px;
                color: #94a3b8;
                font-size: 15px;
            }

            .status {
                display: flex;
                align-items: center;
                gap: 8px;
                padding: 10px 16px;
                border-radius: 999px;
                background: #052e1a;
                color: #4ade80;
                font-size: 14px;
                font-weight: 600;
                border: 1px solid #166534;
            }

            .status-dot {
                width: 9px;
                height: 9px;
                border-radius: 50%;
                background: #22c55e;
                box-shadow: 0 0 10px #22c55e;
            }

            /* Metrics */
            .dashboard {
                display: grid;
                grid-template-columns: repeat(2, 1fr);
                gap: 20px;
            }

            .card {
                background: #111827;
                border: 1px solid #1f2937;
                border-radius: 16px;
                padding: 24px;
                box-shadow: 0 8px 25px rgba(0,0,0,0.18);
                transition: transform 0.2s ease, border-color 0.2s ease;
            }

            .card:hover {
                transform: translateY(-2px);
                border-color: #334155;
            }

            .card-header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 14px;
            }

            .label {
                color: #94a3b8;
                font-size: 14px;
                font-weight: 500;
            }

            .icon {
                width: 34px;
                height: 34px;
                display: flex;
                align-items: center;
                justify-content: center;
                border-radius: 9px;
                background: #1e293b;
                font-size: 16px;
            }

            .value {
                font-size: 32px;
                font-weight: 700;
                color: #f8fafc;
            }

            .healthy-value {
                color: #4ade80;
            }

            /* Progress bars */
            .progress {
                height: 7px;
                background: #1e293b;
                border-radius: 10px;
                margin-top: 15px;
                overflow: hidden;
            }

            .progress-bar {
                height: 100%;
                width: 0%;
                background: #3b82f6;
                border-radius: 10px;
                transition: width 0.5s ease;
            }

            /* Service section */
            .section {
                margin-top: 28px;
            }

            .section-title {
                font-size: 18px;
                font-weight: 600;
                margin-bottom: 14px;
            }

            .service-card {
                background: #111827;
                border: 1px solid #1f2937;
                border-radius: 16px;
                padding: 22px;
                display: flex;
                justify-content: space-between;
                align-items: center;
            }

            .service-info {
                display: flex;
                align-items: center;
                gap: 14px;
            }

            .service-icon {
                width: 42px;
                height: 42px;
                border-radius: 10px;
                background: #052e1a;
                display: flex;
                align-items: center;
                justify-content: center;
                color: #4ade80;
                font-size: 20px;
            }

            .service-name {
                font-weight: 600;
            }

            .service-description {
                color: #64748b;
                font-size: 13px;
                margin-top: 4px;
            }

            .operational {
                color: #4ade80;
                font-size: 14px;
                font-weight: 600;
            }

            /* Links */
            .links {
                margin-top: 28px;
                display: flex;
                gap: 12px;
            }

            .api-link {
                text-decoration: none;
                color: #93c5fd;
                background: #172554;
                border: 1px solid #1e40af;
                padding: 10px 16px;
                border-radius: 9px;
                font-size: 14px;
                transition: background 0.2s ease;
            }

            .api-link:hover {
                background: #1e3a8a;
            }

            /* Footer */
            .footer {
                margin-top: 30px;
                display: flex;
                justify-content: space-between;
                color: #64748b;
                font-size: 13px;
            }

            /* Responsive */
            @media (max-width: 700px) {

                .container {
                    padding: 25px 18px;
                }

                .header {
                    flex-direction: column;
                    align-items: flex-start;
                }

                .dashboard {
                    grid-template-columns: 1fr;
                }

                .service-card {
                    align-items: flex-start;
                    gap: 15px;
                    flex-direction: column;
                }

                .footer {
                    flex-direction: column;
                    gap: 8px;
                }
            }
        </style>
    </head>

    <body>

        <div class="container">

            <!-- Header -->
            <div class="header">

                <div class="title-section">
                    <h1>Cloud Application Monitoring</h1>

                    <div class="subtitle">
                        Real-time application health and infrastructure metrics
                    </div>
                </div>

                <div class="status">
                    <span class="status-dot"></span>
                    System Operational
                </div>

            </div>


            <!-- Metrics -->
            <div class="dashboard">

                <!-- CPU -->
                <div class="card">

                    <div class="card-header">
                        <div class="label">CPU Usage</div>
                        <div class="icon">⚙</div>
                    </div>

                    <div class="value" id="cpu">
                        {{ cpu }}%
                    </div>

                    <div class="progress">
                        <div
                            class="progress-bar"
                            id="cpu-bar"
                            style="width: {{ cpu }}%">
                        </div>
                    </div>

                </div>


                <!-- Memory -->
                <div class="card">

                    <div class="card-header">
                        <div class="label">Memory Usage</div>
                        <div class="icon">▣</div>
                    </div>

                    <div class="value" id="memory">
                        {{ memory }}%
                    </div>

                    <div class="progress">
                        <div
                            class="progress-bar"
                            id="memory-bar"
                            style="width: {{ memory }}%">
                        </div>
                    </div>

                </div>


                <!-- Uptime -->
                <div class="card">

                    <div class="card-header">
                        <div class="label">Application Uptime</div>
                        <div class="icon">◷</div>
                    </div>

                    <div class="value" id="uptime">
                        {{ uptime }}s
                    </div>

                </div>


                <!-- Requests -->
                <div class="card">

                    <div class="card-header">
                        <div class="label">Requests Served</div>
                        <div class="icon">↗</div>
                    </div>

                    <div class="value" id="requests">
                        {{ requests }}
                    </div>

                </div>

            </div>


            <!-- Service Health -->
            <div class="section">

                <div class="section-title">
                    Service Health
                </div>

                <div class="service-card">

                    <div class="service-info">

                        <div class="service-icon">
                            ✓
                        </div>

                        <div>
                            <div class="service-name">
                                Cloud Monitoring Service
                            </div>

                            <div class="service-description">
                                Health checks and metrics collection active
                            </div>
                        </div>

                    </div>

                    <div class="operational">
                        ● Operational
                    </div>

                </div>

            </div>


            <!-- API Links -->
            <div class="links">

                <a class="api-link" href="/health">
                    Health API →
                </a>

                <a class="api-link" href="/metrics">
                    Metrics API →
                </a>

            </div>


            <!-- Footer -->
            <div class="footer">

                <div>
                    Monitoring refreshes automatically every 10 seconds
                </div>

                <div>
                    Last updated: <span id="last-updated">just now</span>
                </div>

            </div>

        </div>


        <script>

            function updateDashboard() {

                fetch("/metrics")

                    .then(response => response.json())

                    .then(data => {

                        /* Update metric values */

                        document.getElementById("cpu").textContent =
                            data.cpu_usage_percent.toFixed(1) + "%";

                        document.getElementById("memory").textContent =
                            data.memory_usage_percent.toFixed(1) + "%";

                        document.getElementById("uptime").textContent =
                            data.uptime_seconds.toFixed(1) + "s";

                        document.getElementById("requests").textContent =
                            data.request_count;


                        /* Update progress bars */

                        document.getElementById("cpu-bar").style.width =
                            data.cpu_usage_percent + "%";

                        document.getElementById("memory-bar").style.width =
                            data.memory_usage_percent + "%";


                        /* Update timestamp */

                        document.getElementById("last-updated").textContent =
                            new Date().toLocaleTimeString();

                    })

                    .catch(error => {

                        console.error(
                            "Failed to fetch metrics:",
                            error
                        );

                    });

            }


            /* Initial update */

            updateDashboard();


            /* Refresh every 10 seconds */

            setInterval(updateDashboard, 10000);

        </script>

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