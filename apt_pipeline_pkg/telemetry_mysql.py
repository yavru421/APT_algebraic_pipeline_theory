"""
MySQL telemetry writer for APT snapshot events.

This module provides a function to insert APT pipeline snapshot events into a MySQL database.
It is intended to be called from the snapshot logger or as a post-processing step.

Usage:
    from apt_pipeline_pkg.telemetry_mysql import insert_event
    insert_event(
        host="localhost", user="user", password="pw", database="apt_db",
        event={...}
    )

Requirements:
    pip install mysql-connector-python

Security:
    Do not hardcode credentials. Use environment variables or a config file.
"""
import os
import mysql.connector
from mysql.connector import Error
from typing import Any, Dict

def insert_event(
    host: str,
    user: str,
    password: str,
    database: str,
    event: Dict[str, Any],
    port: int = 3306,
    table: str = "events",
) -> bool:
    """Insert a single event record into the MySQL events table.
    The event dict should contain keys matching the schema (id, provider, prompt, zipcode, lat, lng, geom, client_id, created_at).
    If id is not provided, a UUID will be generated.
    If geom is not provided, it will be computed from lat/lng if present.
    """
    import uuid
    from datetime import datetime

    # Prepare event fields
    ev = dict(event)
    if "id" not in ev:
        ev["id"] = str(uuid.uuid4())
    if "created_at" not in ev:
        ev["created_at"] = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    # Compute geom as WKT if not provided
    if ("lat" in ev and "lng" in ev) and (ev.get("lat") is not None and ev.get("lng") is not None):
        ev["geom"] = f"POINT({ev['lng']} {ev['lat']})"
    else:
        ev["geom"] = None

    # Build insert statement
    cols = [k for k in ev.keys() if k != "geom"] + ["geom"]
    placeholders = ["%s"] * len(cols)
    sql = f"INSERT INTO {table} ({', '.join(cols)}) VALUES ({', '.join(placeholders)})"
    values = [ev.get(k) for k in cols[:-1]] + [ev["geom"]]

    try:
        conn = mysql.connector.connect(
            host=host, user=user, password=password, database=database, port=port
        )
        cursor = conn.cursor()
        cursor.execute(sql, values)
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Error as e:
        print(f"[telemetry_mysql] Error inserting event: {e}")
        return False
