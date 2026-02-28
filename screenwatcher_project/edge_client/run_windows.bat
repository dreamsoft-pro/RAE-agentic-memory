@echo off
echo Starting ScreenWatcher Edge Client...

if not exist config.json (
    echo Creating default configuration for Tailscale connection...
    (
        echo {
        echo     "machine_code": "WIN_CLIENT_%RANDOM%",
        echo     "api_url": "http://100.66.252.117:9000/api/collector/ingest/",
        echo     "interval_sec": 5,
        echo     "rois": []
        echo }
    ) > config.json
)

python main.py
pause
