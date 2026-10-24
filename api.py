from fastapi import FastAPI

from main import minerar_api

motor = FastAPI()

@motor.get("/status")
def testarapi() -> dict[str, int]:
    teste: str = "contratação"
    return minerar_api(teste)
