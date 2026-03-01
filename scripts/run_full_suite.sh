#!/bin/bash
export PYTHONPATH=rae-core
export PYTHONUNBUFFERED=1
PY=.venv/bin/python3

echo '--- ACADEMIC LITE ---'
$PY benchmarking/scripts/run_benchmark.py --set benchmarking/sets/academic_lite.yaml --queries 20
echo '--- ACADEMIC EXTENDED ---'
$PY benchmarking/scripts/run_benchmark.py --set benchmarking/sets/academic_extended.yaml --queries 20
echo '--- INDUSTRIAL SMALL ---'
$PY benchmarking/scripts/run_benchmark.py --set benchmarking/sets/industrial_small.yaml --queries 20
echo '--- INDUSTRIAL LARGE (10k) ---'
$PY benchmarking/scripts/run_benchmark.py --set benchmarking/sets/industrial_10k.yaml --queries 50
echo '--- 9/5 SPECIALIZED ---'
$PY benchmarking/nine_five_benchmarks/run_nine_five.py
