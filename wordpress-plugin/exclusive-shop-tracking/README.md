# Plugin de seguimiento para WooCommerce

1. Comprime la carpeta `exclusive-shop-tracking` en un archivo ZIP.
2. En WordPress abre **Plugins → Añadir nuevo → Subir plugin**.
3. Sube el ZIP y actívalo.
4. Entra a **WooCommerce → Pedidos** y abre un pedido.
5. En la dirección de envío aparecerá **Seguimiento del envío**.

Guarda la empresa, el código de tracking y, para Shalom si corresponde, el
número de orden de la transportista. Los valores se almacenan con las mismas
claves de metadatos que usa ShopAgent:

- `_empresa_envio`
- `_codigo_seguimiento`
- `_numero_orden_envio`

El cliente autenticado verá el código y un enlace al portal oficial en el
detalle de su pedido.
