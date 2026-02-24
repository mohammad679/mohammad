from __future__ import annotations

import os
from datetime import datetime, timezone

import pandas as pd
from sklearn.datasets import load_breast_cancer
from sqlalchemy import create_engine


def build_connection_uri() -> str:
    host = os.getenv("POSTGRES_HOST", "localhost")
    port = os.getenv("POSTGRES_PORT", "5432")
    db = os.getenv("POSTGRES_DB", "feature_store")
    user = os.getenv("POSTGRES_USER", "feast")
    password = os.getenv("POSTGRES_PASSWORD", "feast")
    return f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{db}"


def main() -> None:
    dataset = load_breast_cancer(as_frame=True)
    frame = dataset.frame[["mean radius", "mean texture", "mean perimeter", "mean area", "target"]].copy()
    frame.columns = [
        "mean_radius",
        "mean_texture",
        "mean_perimeter",
        "mean_area",
        "target",
    ]
    frame["entity_id"] = range(len(frame))
    now = datetime.now(tz=timezone.utc)
    frame["event_timestamp"] = now
    frame["created"] = now

    engine = create_engine(build_connection_uri())
    frame.to_sql("driver_stats", engine, if_exists="replace", index=False)
    print(f"Wrote {len(frame)} rows to driver_stats")


if __name__ == "__main__":
    main()
