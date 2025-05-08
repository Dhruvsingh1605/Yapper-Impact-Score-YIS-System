from fastapi import FastAPI
from app.routers.score import router as score_router
import logging  # :contentReference[oaicite:4]{index=4}

logger = logging.getLogger("yis")
logger.setLevel(logging.DEBUG)

fh = logging.FileHandler("logs/yis.log")
fh.setLevel(logging.DEBUG)

formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
fh.setFormatter(formatter)
logger.addHandler(fh)


app = FastAPI()
app.include_router(score_router, prefix="/score", tags=["score"])
