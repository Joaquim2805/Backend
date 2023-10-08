from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import random
import uvicorn

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Vous pouvez spécifier les origines autorisées ici
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/items")
def get_items(minValue: float = Query(..., description="Valeur minimale"),
              maxValue: float = Query(..., description="Valeur maximale"),
              numBins: int = Query(..., description="Nombre de bacs")):
    data = data_sent(numBins, minValue, maxValue)
    labels = bin_label_py(numBins, minValue, maxValue)
    result = {"data": data, "labels": labels}
    return result
    


def data_sent(numBins, minValue, maxValue):
    
    data = []
    for i in range(numBins):
        random_value = random.uniform(0,1000)
        data.append(random_value)
    return data

def bin_label_py(numBins, minValue, maxValue):
    binWidth = (maxValue - minValue) / numBins
    labels = []
    for i in range(numBins):
        bin_start = minValue + i * binWidth
        bin_end = bin_start + binWidth
        formatted_string = f"{bin_start:.2f} - {bin_end:.2f}"
        labels.append(formatted_string)
    return labels


