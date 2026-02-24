from __future__ import annotations

import uvicorn

from serving.app import app
from serving.config import ServingConfig


if __name__ == "__main__":
    cfg = ServingConfig()
    uvicorn.run(app, host=cfg.host, port=cfg.port)
