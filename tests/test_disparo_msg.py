import json
import requests
import os
from dotenv import load_dotenv


load_dotenv()

token = os.getenv("TELEGRAM_BOT_TOKEN")
chat_id = os.getenv("TELEGRAM_GROUP_ID")
url_base = f"https://api.telegram.org/bot{token}"

mockup_produto = {
    "titulo": "Coturno Militar Masculino Com Zíper Tático Couro Exército",
    "preco_original": 115.00,
    "preco_atual": 109.25,
    "desconto": 5,
    "imagem_url": "https://http2.mlstatic.com/D_NQ_NP_2X_816922-MLB43494922142_092020-F-coturno-militar-masculino-com-ziper-tatico-couro-exercito.webp",
    "link_produto": "https://produto.mercadolivre.com.br/MLB-892428990-coturno-militar-masculino-com-ziper-tatico-couro-exercito-_JM?searchVariation=174821581111&pdp_filters=item_id%3AMLB892428990#polycard_client=search-desktop&searchVariation=174821581111&be_origin=searchv2&overlay_label=not_apply&search_layout=grid&position=5&type=item&tracking_id=89fd83aa-47a7-4c14-af2c-eeb3a95d32d0&overlay_label_capability=not_apply&sid=search"
}

caption_html = (
    f"🔥 <b>{mockup_produto['titulo']}</b>\n\n"
    f"❌ De: <s>R$ {mockup_produto['preco_original']:,.2f}</s>\n"
    f"✅ <b>Por: R$ {mockup_produto['preco_atual']:,.2f}</b> "
    f"(-{mockup_produto['desconto']}% OFF)\n\n"
    f"⚡ <i>Preço promocional sujeito a alteração de estoque.</i>"
)#formatar valores para PT-BR.

inline_keyboard = {
    "inline_keyboard":[
        [
            {
                "text": "🛒 Ver Oferta no Mercado Livre",
                "url": mockup_produto["link_produto"]
            }
        ]
    ]
}

payload = {
    "chat_id": chat_id,
    "photo": mockup_produto["imagem_url"],
    "caption": caption_html,
    "parse_mode": "HTML",
    "reply_markup": json.dumps(inline_keyboard)
}

def disparar_msg():
    url = f"https://api.telegram.org/bot{token}/sendPhoto"
    resposta = requests.post(url, data=payload)

    if resposta.ok:
        print(f"[SUCESSO]: Mensagem enviada! {resposta.status_code}")
    else:
        dados = resposta.json()
        print(f"[ERRO]: Falha no envio: {dados.get('description')} (Erro: {resposta.status_code})")

if __name__ == "__main__":
    disparar_msg()
    
