import requests
import os
from dotenv import load_dotenv

load_dotenv()

token = os.getenv("TELEGRAM_BOT_TOKEN")
base_url = f"https://api.telegram.org/bot{token}"

def teste_conectividade():
    url = f"{base_url}/getMe"
    resposta = requests.get(url)

    if not resposta.ok:
        print(f"[Erro: {resposta.status_code}]: A conexão falhou! {resposta.text}")
        return False
    else:
        print(f"[Sucesso: {resposta.status_code}]")
        return True


def pega_chat_id():
    url = f"{base_url}/getUpdates"
    lista_dados = requests.get(url).json()
    
    if lista_dados.get("result"):

        primeira_atualizacao = lista_dados["result"][0]
        chat_id = primeira_atualizacao.get("message",{}).get("chat",{}).get("id")
        
        if chat_id:
            print(f"Chat Id: {chat_id}")
        else:
            print("[ERRO]: Chat_Id não encontrado, o bot não enxergou nenhuma atualização no padrão esperado para coletar o Chat Id. Envie uma mensagem no grupo mencionando o bot e tente novamente.")
    else:
        print("[ERRO]: Chat_Id não encontrado, o bot não enxergou nenhuma atualização no grupo. Envie uma mensagem no grupo mencionando o bot e tente novamente.")


if __name__ == "__main__":
    if teste_conectividade():
        print(f"Iniciando busca pelo Chat Id...")
        pega_chat_id()
    

