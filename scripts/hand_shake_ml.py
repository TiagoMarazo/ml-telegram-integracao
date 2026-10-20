import requests
import json
import os
import time
from dotenv import load_dotenv

load_dotenv()

APP_ID = os.getenv("APP_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
AUTHORIZATION_CODE = os.getenv("AUTHORIZATION_CODE")
REDIRECT_URI = os.getenv("REDIRECT_ URI")

URL_AUTH = "https://api.mercadolibre.com/oauth/token"

ARQUIVO_TOKEN = "tokens.json"

def trocar_codigo_por_tokens():
    header = {
        "accept":"application/json",
        "content-type":"x-www-form-urlencoded"
    }

    payload = {
        "grant-type":"authorization_code",
        "client_id":APP_ID,
        "client_secret":CLIENT_SECRET,
        "code":AUTHORIZATION_CODE,
        "redirect_uri":REDIRECT_URI
    }

    print("[...] Enviando requisição para obter Tokens iniciais...")
    response = requests.post(URL_AUTH, header=header, data=payload)
    dados = response.json()

    if not response.ok:
        print(f"[ERRO]: Falha ao obter token. {response.status_code}: {dados}")
        print("Lembre-se o 'code' dura cerca de 15 minutos apenas! Você pode precisar autorizar novamente a aplicação.")
        return False

    dados["created_at"] = int(time.time())
    
    with open(ARQUIVO_TOKEN, "w", encoding="utf-8") as file:
        json.dump(dados, file, indent = 4)

    print(f"[SUCESSO]: Chaves obtidas e salvas em '{ARQUIVO_TOKEN}'!")
    print(f"Access_Token: {dados.get("access_token")} Expires_In: {dados.get("expires_in")}s")
    print(f"Refresh_Token: {dados.get('refresh_token')}")
    return True

if __name__ == "__main__":
    trocar_codigo_por_tokens()