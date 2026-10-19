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

url_auth = "https://api.mercadolibre.com/oauth/token"

arquivo_token = "tokens.json"

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
    response = requests.post(url_auth, header=header, data=payload)
    dados = response.json()

    if not response.ok:
        print(f"[ERRO]: Falha ao obter token. {response.status_code}: {dados}")
        print("Lembre-se o 'code' dura cerca de 15 minutos apenas! Você pode precisar autorizar novamente a aplicação.")
        return False

    dados["created_at"] = int(time.time())
    
    with open(arquivo_token, "w", encoding="utf-8") as file:
        json.dump(dados, file, indent = 4)

    print(f"[SUCESSO]: Chaves obtidas e salvas em '{arquivo_token}'!")
    print(f"Acess_Token: {dados.get("acess_token")} Expires_In: {dados.get("expires_in")}s")
    print(f"Refresh_Token: {dados.get('refresh_token')}")
    return True

if __name__ == "__main__":
    trocar_codigo_por_tokens()