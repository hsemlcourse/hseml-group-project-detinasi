import joblib
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict, Any

# Создаем приложение FastAPI
app = FastAPI(
    title="Fraud Detection API", 
    description="API для детекции мошеннических транзакций",
    version="1.0"
)

# Загружаем нашу лучшую обученную модель (Random Forest)
# Убедись, что путь к модели правильный относительно корня проекта
MODEL_PATH = "models/best_rf_tuned.pkl"
try:
    model = joblib.load(MODEL_PATH)
    print("Модель успешно загружена!")
except Exception as e:
    print(f"Ошибка загрузки модели: {e}")

# Описываем формат входящих данных (JSON)
class PredictRequest(BaseModel):
    features: Dict[str, Any]

    model_config = {
        "json_schema_extra": {
            "example": {
                "features": {
                    "transaction_amount": 15000.0,
                    "account_age_days": 1.0,
                    "avg_monthly_spend": 1000.0,
                    "merchant_risk_score": 0.95,
                    "is_international": 1.0,
                    "ip_risk_score": 0.99,
                    "txn_count_1h": 2.0,
                    "txn_count_24h": 5.0,
                    "failed_txn_count_24h": 4.0,
                    "geo_distance_from_last_txn": 500.0,
                    "amount_deviation_from_user_mean": 14000.0,
                    "amount_to_avg_spend_ratio": 15.0,
                    "failed_to_total_24h_ratio": 0.8,
                    "is_new_account": 1.0,
                    
                    # Те самые колонки, которые требовала модель:
                    "credit_score_band": 3.0,
                    "kyc_level": 2.0,
                    "payment_channel_card": 1.0,
                    "payment_channel_upi": 0.0,
                    "payment_channel_wallet": 0.0,
                    
                    # Оставим девайсы на всякий случай
                    "device_type_mobile": 1.0,
                    "device_type_tablet": 0.0
                }
            }
        }
    }


# Создаем эндпоинт (ручку) для предсказаний
@app.post("/predict")
def predict(request: PredictRequest):
    if model is None:
         return {
             "status": "error", 
             "message": "Модель не загружена на сервере."
         }
         
    try:
        # 1. Преобразуем входящий словарь в DataFrame
        df = pd.DataFrame([request.features])
        
        # 2. Узнаем, какие колонки и в каком порядке ждет модель
        expected_columns = model.feature_names_in_
        
        # 3. Строго фильтруем и выстраиваем колонки. 
        # Если какой-то колонки в JSON нет, код упадет в KeyError (и мы его поймаем ниже)
        df = df[expected_columns]
        
        # 4. Делаем предсказание
        prediction = model.predict(df)
        probability = model.predict_proba(df)[:, 1]
        
        return {
            "status": "success",
            "is_fraud": int(prediction[0]),
            "fraud_probability": float(probability[0])
        }
    except KeyError as e:
        # Возвращаем понятную ошибку, если в JSON не хватает признаков
        return {"status": "error", "message": f"Не хватает обязательной колонки: {str(e)}"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

# Корневой эндпоинт для проверки, что сервер жив
@app.get("/")
def read_root():
    return {"message": "Fraud Detection API is running! Перейдите на /docs для интерфейса Swagger."}
