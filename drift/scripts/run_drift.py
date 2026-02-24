from __future__ import annotations

import json

from drift.config import DriftConfig
from drift.job import compute_drift


if __name__ == "__main__":
    print(json.dumps(compute_drift(DriftConfig()), indent=2))
