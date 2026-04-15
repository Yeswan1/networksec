import sys
import os
import certifi

from dotenv import load_dotenv
load_dotenv()

# ✅ Mongo URL from ENV
mongo_db_url = os.getenv("MONGODB_URL_KEY")

ca = certifi.where()

import pymongo
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.pipeline.training_pipeline import TrainingPipeline

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, File, UploadFile
from uvicorn import run as app_run
from fastapi.responses import Response
from starlette.responses import RedirectResponse
import pandas as pd

from networksecurity.utils.main_utils.utils import load_object
from networksecurity.utils.ml_utils.model.estimator import NetworkModel


# ✅ SAFE MongoDB connection (TLS FIX)
client = None
try:
    if mongo_db_url:
        client = pymongo.MongoClient(
            mongo_db_url,
            tls=True,
            tlsCAFile=ca
        )
        client.server_info()
        print("MongoDB connected ✅")
except Exception as e:
    print("MongoDB FAILED ❌:", e)


from networksecurity.constant.training_pipeline import DATA_INGESTION_COLLECTION_NAME
from networksecurity.constant.training_pipeline import DATA_INGESTION_DATABASE_NAME

if client:
    database = client[DATA_INGESTION_DATABASE_NAME]
    collection = database[DATA_INGESTION_COLLECTION_NAME]


# ✅ FastAPI app
app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ✅ Root → Swagger
@app.get("/", tags=["authentication"])
async def index():
    return RedirectResponse(url="/docs")


# ✅ TRAIN API
@app.get("/train")
async def train_route():
    try:
        train_pipeline = TrainingPipeline()
        train_pipeline.run_pipeline()
        return {"message": "Training is successful"}
    except Exception as e:
        return {"error": str(e)}


# ✅ PREDICT API
@app.post("/predict")
async def predict_route(file: UploadFile = File(...)):
    try:
        df = pd.read_csv(file.file)

        # remove unwanted columns
        drop_cols = ["Unnamed: 0", "predicted_column"]
        df = df.drop(columns=[c for c in drop_cols if c in df.columns])

        # load model
        preprocessor = load_object("final_model/preprocessor.pkl")
        final_model = load_object("final_model/model.pkl")

        network_model = NetworkModel(
            preprocessor=preprocessor,
            model=final_model
        )

        y_pred = network_model.predict(df)

        return {"predictions": y_pred.tolist()}

    except Exception as e:
        return {"error": str(e)}


# ✅ Run server
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app_run(app, host="0.0.0.0", port=port)
