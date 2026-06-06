#!/bin/bash
echo "Starting FlutterFix Autonomous Society..."
pip install psutil --quiet
python flutter_fix_v22.py &
echo $! > flutterfix.pid
echo "Society started with PID: $(cat flutterfix.pid)"
