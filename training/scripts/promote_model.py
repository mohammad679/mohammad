from __future__ import annotations

import json

from training.config import TrainingConfig
from training.promote import promote_latest_version_if_valid


if __name__ == "__main__":
    result = promote_latest_version_if_valid(TrainingConfig())
    print(json.dumps(result, indent=2))
