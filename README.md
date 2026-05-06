# Hybrid IoT Intrusion Detection System (Hybrid IDS)

A real-time Hybrid Intrusion Detection System for IoT networks using:

- Rule-Based Detection
- Machine Learning Anomaly Detection
- Real-Time Dashboard Monitoring

This project monitors live network traffic in Mininet using Scapy and detects attacks such as:

- DDoS Attacks
- SYN Floods
- Port Scans
- UDP Floods
- MQTT Floods
- Behavioral Anomalies

---

# Features

## Phase 1 — Rule-Based IDS
Detects:
- Traffic Flooding
- SYN Floods
- Port Scans
- Distributed Bot Activity

## Phase 2 — Machine Learning IDS
Uses:
- Feature Extraction
- Random Forest Classifier
- Behavioral Analysis

Detects:
- Unknown anomalies
- Low-rate attacks
- Stealth attacks

## Phase 3 — Dashboard Monitoring
Provides:
- Live Packet Rate
- Live Alerts
- Blocked IP Monitoring
- Traffic Graphs
- Manual IP Blocking

---

# Technologies Used

- Python 3
- Scapy
- Flask
- Chart.js
- Scikit-learn
- Joblib
- Mininet
- Linux iptables

---

# Project Structure

iot-hybrid-ids/
│
├── phase1_rule_ids/
│   ├── packet_sniffer.py
│   ├── rule_engine.py
│   ├── alert_logger.py
│   ├── alert_formatter.py
│   ├── run_ids.py
│
├── phase2_ml_ids/
│   ├── feature_aggregator.py
│   ├── dataset_generator.py
│   ├── train_model.py
│   ├── ml_detector.py
│   ├── model.pkl
│
├── phase3_hybrid_ids/
│   ├── dashboard_api.py
│   ├── ip_blocker.py
│   ├── shared_state.py
│   ├── static/
│   │   └── index.html
│
├── logs/
│   └── alerts.log
│
└── README.md

---

# Installation

## Clone Repository

```bash
git clone https://github.com/karnikaagarwal/iot-hybrid-ids.git

cd iot-hybrid-ids
