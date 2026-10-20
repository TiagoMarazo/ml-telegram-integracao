import requests
import json
import os
import time
from dotenv import load_dotenv

load_dotenv()

URL_AUTH = "https://api.mercadolibre.com/oauth/token"
ARQUIVO_TOKEN = "tokens.json"
APP_ID = os.getenv("APP_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
MARGEM_DE_SEGURANCA_SEGUNDOS = 300

def carrega_tokens() -> dict:
    if not os.path.exists(ARQUIVO_TOKEN):
            raise FileNotFoundError(
                f"[ERRO]: Arquivo '{ARQUIVO_TOKEN}' não encontrado. Execute o 'hand_shake_ml.py' primeiro."
            )
    with open(ARQUIVO_TOKEN, "r", encoding="utf-8") as file:
        return json.load(file)
    
def access_token_esta_valido(dados:dict) -> bool:
    created_at = dados.get("created_at")
    expires_in = dados.get("expires_in", 21600)

    if not created_at:
         return False
    
    tempo_decorrido = int(time.time()) - created_at

    return tempo_decorrido < (expires_in - MARGEM_DE_SEGURANCA_SEGUNDOS)

def renova_access_token() -> bool:
    dados_atuais = carrega_tokens()
    refresh_token = dados_atuais.get("refresh_token")

    if not refresh_token:
         print("[ERRO]: 'refresh_token' não encontrado no arquivo.")
         return False
    
    header = {
       "accept":"application/json",
       "content-type":"application/x-www-form-urlencoded"  
    }

    payload = {
         "grant_type":"refresh_token",
         "client_id":APP_ID,
         "client_secret":CLIENT_SECRET,
         "refresh_token":refresh_token
    }

    print("[...]Enviando requisição para renovação do Acess Token...")
    try:
        response = requests.post(URL_AUTH, headers=header, data=payload, timeout=10)
    except requests.RequestException as e:
        print(f"[ERRO]: Falha na conexão como Mercado Livre: {e}")
        return False
    
    dados = response.json()

    if not response.ok:
            print(f"[ERRO]: Falha ao renovar Acess Token. {response.status_code}: {dados}")
            return False

    dados["created_at"] = int(time.time())

    with open(ARQUIVO_TOKEN, "w", encoding="utf-8") as file:
         json.dump(dados, file, indent = 4)

    print(f"[SUCESSO]: Acess Token renovado com sucesso! Arquivo '{ARQUIVO_TOKEN}' atualizado!")
    print(f"Novo Acess_Token: {dados.get("access_token")} Expires_In: {dados.get("expires_in")}s")
    print(f"Novo Refresh_Token: {dados.get('refresh_token')}")
    return True

if __name__ == "__main__":
    dados = carrega_tokens()

    if access_token_esta_valido(dados):
        print("[OK]: O token atual ainda é válido e seguro para uso.")
    else:
        print("[AVISO]: Token precisa ser renovado.")
        renova_access_token()
    