# Seguimiento de pedidos

El seguimiento se guarda en los metadatos de WooCommerce:

- `_empresa_envio`
- `_codigo_seguimiento`
- `_numero_orden_envio` (requerido por Shalom)

`TrackingService.consultar_pedido(order_id)` recupera estos valores y responde
con un objeto estructurado. `SalesAgent.consultar_seguimiento_pedido(order_id)`
expone el mismo flujo para una capa de conversación o una futura API privada.

## Consulta para clientes

La API expone `POST /tracking`. Recibe `order_id` y `email`; antes de devolver
el tracking comprueba que el correo coincide con el correo de facturación del
pedido en WooCommerce. Un correo incorrecto y un pedido inexistente devuelven
el mismo mensaje para no revelar pedidos de otros clientes.

```json
{
  "order_id": 42916,
  "email": "cliente@ejemplo.com"
}
```

La interfaz de chat debe pedir ambos datos y llamar a esta ruta; no debe pedir
ni mostrar la clave de consumidor de WooCommerce.

## Comportamiento actual

El servicio no inventa el estado de un envío. Para Shalom y Olva devuelve el
transportista, los identificadores guardados y el enlace a su portal oficial;
`estado` permanece como `None` y `consulta_automatica` como `False`.

No se debe añadir una ruta pública que acepte solamente un número de pedido:
antes de consultar se debe autenticar al cliente y verificar que ese pedido le
pertenece.

## Habilitar una consulta automática

Solo se implementará al recibir del transportista una API oficial documentada,
credenciales de producción y permiso para consultar los envíos de la tienda.
Antes de activarla se debe definir y probar:

1. Autenticación y rotación segura de credenciales.
2. Campos de consulta autorizados y límites de uso.
3. Mapeo explícito de cada estado oficial a la respuesta de ShopAgent.
4. Manejo de errores, tiempos de espera y datos incompletos.
5. Pruebas con envíos reales de prueba, sin exponer datos de clientes.

Mientras tanto, ShopAgent puede informar los datos registrados y enviar al
cliente al portal oficial sin afirmar que el paquete está en tránsito, entregado
o retrasado.
