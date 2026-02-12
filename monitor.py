import asyncio
import requests
from playwright.async_api import async_playwright

# Condifugracion (Implementar el producto futuro con .env)
TOKEN_TELEGRAM = "8528876963:AAE4O5GnpjlLLGjSmunyjsCGW5qtPwOBWds"
CHAT_ID = "1004580298"
URL_INTERES = "https://tienda-ejemplo.com"


#https://api.telegram.org/bot8528876963:AAE4O5GnpjlLLGjSmunyjsCGW5qtPwOBWds/getUpdates

def enviar_alerta_telegram(mensaje):
    # def notifica al alciente por movil
    url = f"https://api.telegram.org/bot{TOKEN_TELEGRAM}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": mensaje}
    
    try:
        requests.post(url, json=payload)
    except Exception as e:
        print(f"Error enviado a Telegram: {e}")




async def monitor_profesional():
    async with async_playwright() as p:
        # Lanzamos el navegador (headless=True para que sea invisible y rápido)
        browser = await p.chromium.launch(headless=True)

        # User-Agent real para evitar bloques (Esto los destaca para poder vnederlo)
        context = await p.chromium.launch(headless=True)
        
        page = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
        )

        page = await context.new_page()

        
        try:
            await page.goto(URL_INTERES, timeout=60000)

            # Selector generico (Cambiar ajuste par ala web real)
            nombre = await page.inner_text("h1")
            precio_raw = await page.inner_text(".price_value")

            precio_actual = float(precio_raw.replace("$", "").replace(".", "").strip())
            limite_compra = 500000 # Ejemplo



            
            # --- AQUÍ ESTÁ LA MAGIA ---
            # Buscamos el nombre y el precio usando selectores CSS
            # Nota: Los selectores cambian según la web (.price, #valor, etc.)
            nombre_producto = await page.inner_text("h1")
            precio_texto = await page.inner_text(".price-tag") 
            
            # Limpiamos el precio para convertirlo a número
            precio_actual = float(precio_texto.replace("$", "").replace(",", "").strip())
            limite_compra = 500000 # Ejemplo
            
            print(f"Producto: {nombre_producto} | Precio actual: ${precio_actual}")

            if precio_actual <= limite_compra:
                mensaje = f"🚀!OPORTUNIDAD! {nombre} ha bajado a ${precio_actual}. Compra aqui: {URL_INTERES}"
                enviar_alerta_telegram(mensaje)
                print(f"Chequeo completado: {nombre} - ${precio_actual}")
                # Aquí conectarías con una API de WhatsApp, Telegram o Email

        except Exception as e:
            print(f"Error al scraping: {e}")
        finally:
            await browser.close()

# Ejecutar el monitor
if __name__ == "__main__":
    asyncio.run(monitor_profesional())