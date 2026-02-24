from __future__ import annotations

import json

from training.config import TrainingConfig
from training.pipeline import train_and_log


if __name__ == "__main__":
    result = train_and_log(TrainingConfig())
    print(json.dumps(result, indent=2))
