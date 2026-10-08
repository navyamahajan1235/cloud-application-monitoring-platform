# Cloud Application Monitoring Platform

A containerized Flask application with built-in health checks, application metrics, logging, automated testing, CI/CD, and cloud deployment.

## 🚀 Live Demo

https://cloud-application-monitoring-platform.onrender.com

## 📌 Overview

This project demonstrates how a web application can be packaged, tested, deployed, and monitored using modern Cloud/DevOps practices.

The platform provides a monitoring dashboard that displays:

- Application health status
- CPU usage
- Memory usage
- Application uptime
- Number of requests served

It also exposes API endpoints for health and metrics monitoring.

## 🏗️ Architecture

```text
Developer
    │
    ▼
GitHub Repository
    │
    ▼
GitHub Actions
    │
    ├── Run automated tests
    │
    ▼
Docker Build
    │
    ▼
Render Cloud Deployment
    │
    ▼
Flask + Gunicorn Application
    │
    ├── /healthz
    ├── /metrics
    └── Monitoring Dashboard
