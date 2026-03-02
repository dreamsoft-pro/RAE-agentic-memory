import mysql.connector
import os
import json
from datetime import datetime, timedelta

class ScreenWatcherBridge:
    def __init__(self):
        self.config = {
            'user': 'screenwatcher',
            'password': 'password',
            'host': 'screenwatcher_project-db-1',
            'database': 'screenwatcher'
        }

    def execute_query(self, sql):
        try:
            conn = mysql.connector.connect(**self.config)
            cursor = conn.cursor(dictionary=True)
            cursor.execute(sql)
            results = cursor.fetchall()
            cursor.close()
            conn.close()
            return results
        except Exception as e:
            return f"Error: {str(e)}"

    def get_smart_metrics(self, machine_code, date_str):
        """Pobiera zaawansowane metryki OEE (Wydajność netto, przestoje) zgodnie z logiką Grafany."""
        
        # Pobieramy UUID maszyny na podstawie kodu
        machine_info = self.execute_query(f"SELECT id FROM registry_machine WHERE code = '{machine_code}'")
        if not machine_info or isinstance(machine_info, str):
            return {"error": f"Machine {machine_code} not found"}
        mid = machine_info[0]['id']

        # SQL z Grafany (CTE) - Obliczanie statusu na podstawie zmiany hasha OCR
        sql = f"""
        WITH RealtimeStatus AS (
          SELECT
            timestamp,
            machine_id,
            CASE WHEN value = LAG(value, 1) OVER (PARTITION BY machine_id ORDER BY timestamp) THEN 'STOPPED' ELSE 'RUNNING' END as real_status
          FROM collector_metriccontext
          WHERE machine_id = '{mid}' AND `key` = 'ocr_blob_hash' AND DATE(timestamp) = '{date_str}'
        ),
        SpeedData AS (
          SELECT timestamp, value as speed_m2h
          FROM collector_metricreading
          WHERE machine_id = '{mid}' AND name = 'real_speed_m2h' AND value < 450 AND DATE(timestamp) = '{date_str}'
        ),
        Analytics AS (
            SELECT
              rs.timestamp,
              CASE WHEN rs.real_status = 'RUNNING' THEN sp.speed_m2h ELSE 0 END as net_speed,
              TIMESTAMPDIFF(SECOND, rs.timestamp, LEAD(rs.timestamp) OVER (ORDER BY rs.timestamp)) as gap_s,
              rs.real_status
            FROM RealtimeStatus rs
            LEFT JOIN SpeedData sp ON ROUND(UNIX_TIMESTAMP(rs.timestamp)) = ROUND(UNIX_TIMESTAMP(sp.timestamp))
        )
        SELECT 
            '{machine_code}' as code,
            '{date_str}' as date,
            AVG(NULLIF(net_speed, 0)) as avg_net_speed_m2h,
            MAX(net_speed) as max_speed_m2h,
            SUM(CASE WHEN real_status = 'STOPPED' AND gap_s BETWEEN 15 AND 300 THEN gap_s ELSE 0 END) / 60 as micro_stops_min,
            SUM(CASE WHEN real_status = 'STOPPED' AND gap_s > 300 THEN gap_s ELSE 0 END) / 60 as long_breaks_min,
            COUNT(*) as data_points
        FROM Analytics
        """
        return self.execute_query(sql)

if __name__ == "__main__":
    bridge = ScreenWatcherBridge()
    # Test for M01 on Feb 18
    print(f"--- Smart Metrics for M01 on 2026-02-18 ---")
    print(json.dumps(bridge.get_smart_metrics("M01", "2026-02-18"), indent=2))
