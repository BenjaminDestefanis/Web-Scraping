import asyncio
from playwright.async_api import async_playwright

async def monitor_precios():
    async with async_playwright() as p:
        # Lanzamos el navegador (headless=True para que sea invisible y rápido)
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        # Ejemplo con una URL de producto (puedes cambiarla por Amazon, Mercado Libre, etc.)
        url = "https://www.ejemplo-tienda.com/laptop-pro-123"
        
        try:
            await page.goto(url, wait_until="domcontentloaded")
            
            # --- AQUÍ ESTÁ LA MAGIA ---
            # Buscamos el nombre y el precio usando selectores CSS
            # Nota: Los selectores cambian según la web (.price, #valor, etc.)
            nombre_producto = await page.inner_text("h1")
            precio_texto = await page.inner_text(".price-tag") 
            
            # Limpiamos el precio para convertirlo a número
            precio_actual = float(precio_texto.replace("$", "").replace(",", "").strip())
            
            precio_objetivo = 1200.00
            
            print(f"Producto: {nombre_producto} | Precio actual: ${precio_actual}")

            if precio_actual <= precio_objetivo:
                print("¡ALERTA! El precio ha bajado. Enviando notificación...")
                # Aquí conectarías con una API de WhatsApp, Telegram o Email
            else:
                print("El precio sigue alto. Seguiremos monitoreando.")

        except Exception as e:
            print(f"Error al scrapear: {e}")
        
        await browser.close()

# Ejecutar el monitor
if __name__ == "__main__":
    asyncio.run(monitor_precios())