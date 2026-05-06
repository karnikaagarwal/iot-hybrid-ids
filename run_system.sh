#!/bin/bash

echo "======================================="
echo " Starting Hybrid IoT IDS System"
echo "======================================="

BASE_DIR=~/iot-hybrid-ids

cd $BASE_DIR

echo ""
echo "[1] Activating Virtual Environment..."
source iotsec-ml-env/bin/activate

echo ""
echo "[2] Starting Dashboard API..."
gnome-terminal -- bash -c "cd $BASE_DIR && sudo ~/iotsec-ml-env/bin/python -m phase3_hybrid_ids.dashboard_api; exec bash"

sleep 3

echo ""
echo "[3] Starting IDS Engine..."
gnome-terminal -- bash -c "cd $BASE_DIR && sudo ~/iotsec-ml-env/bin/python -m phase1_rule_ids.run_ids; exec bash"

sleep 3

echo ""
echo "[4] Opening Dashboard..."

xdg-open http://localhost:5000

echo ""
echo "======================================="
echo " Hybrid IDS Running Successfully"
echo "======================================="
