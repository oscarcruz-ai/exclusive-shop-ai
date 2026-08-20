<?php
/**
 * Plugin Name: Exclusive Shop - Seguimiento de pedidos
 * Description: Añade campos de transportista, código de tracking y número de orden a los pedidos de WooCommerce.
 * Version: 1.0.0
 * Author: Exclusive Shop
 * Requires Plugins: woocommerce
 */

defined( 'ABSPATH' ) || exit;

add_action(
    'before_woocommerce_init',
    static function () {
        if ( class_exists( '\Automattic\WooCommerce\Utilities\FeaturesUtil' ) ) {
            \Automattic\WooCommerce\Utilities\FeaturesUtil::declare_compatibility(
                'custom_order_tables',
                __FILE__,
                true
            );
        }
    }
);

/**
 * Muestra los campos en la pantalla de edición de pedidos.
 *
 * @param WC_Order $order Pedido que se está editando.
 */
function exclusive_shop_tracking_admin_fields( $order ) {
    if ( ! $order instanceof WC_Order ) {
        return;
    }

    wp_nonce_field( 'exclusive_shop_save_tracking', 'exclusive_shop_tracking_nonce' );

    $empresa      = $order->get_meta( '_empresa_envio' );
    $codigo       = $order->get_meta( '_codigo_seguimiento' );
    $numero_orden = $order->get_meta( '_numero_orden_envio' );
    ?>
    <div class="order_data_column">
        <h3><?php esc_html_e( 'Seguimiento del envío', 'exclusive-shop-tracking' ); ?></h3>

        <p class="form-field form-field-wide">
            <label for="exclusive_shop_empresa_envio">
                <?php esc_html_e( 'Empresa de envío', 'exclusive-shop-tracking' ); ?>
            </label>
            <select id="exclusive_shop_empresa_envio" name="exclusive_shop_empresa_envio">
                <option value=""><?php esc_html_e( 'Seleccionar', 'exclusive-shop-tracking' ); ?></option>
                <option value="Shalom" <?php selected( $empresa, 'Shalom' ); ?>>Shalom</option>
                <option value="Olva Courier" <?php selected( $empresa, 'Olva Courier' ); ?>>Olva Courier</option>
            </select>
        </p>

        <p class="form-field form-field-wide">
            <label for="exclusive_shop_codigo_seguimiento">
                <?php esc_html_e( 'Código de tracking', 'exclusive-shop-tracking' ); ?>
            </label>
            <input type="text" id="exclusive_shop_codigo_seguimiento" name="exclusive_shop_codigo_seguimiento" value="<?php echo esc_attr( $codigo ); ?>" maxlength="100" />
        </p>

        <p class="form-field form-field-wide">
            <label for="exclusive_shop_numero_orden_envio">
                <?php esc_html_e( 'Número de orden del transportista', 'exclusive-shop-tracking' ); ?>
            </label>
            <input type="text" id="exclusive_shop_numero_orden_envio" name="exclusive_shop_numero_orden_envio" value="<?php echo esc_attr( $numero_orden ); ?>" maxlength="100" />
            <span class="description">
                <?php esc_html_e( 'Shalom puede requerir este dato para el rastreo.', 'exclusive-shop-tracking' ); ?>
            </span>
        </p>
    </div>
    <?php
}
add_action( 'woocommerce_admin_order_data_after_shipping_address', 'exclusive_shop_tracking_admin_fields' );

/**
 * Guarda los campos usando la API de pedidos de WooCommerce, compatible con HPOS.
 *
 * @param int $order_id ID del pedido.
 */
function exclusive_shop_save_tracking_fields( $order_id ) {
    if (
        ! isset( $_POST['exclusive_shop_tracking_nonce'] ) ||
        ! wp_verify_nonce(
            sanitize_text_field( wp_unslash( $_POST['exclusive_shop_tracking_nonce'] ) ),
            'exclusive_shop_save_tracking'
        )
    ) {
        return;
    }

    if ( ! current_user_can( 'edit_shop_order', $order_id ) ) {
        return;
    }

    $order = wc_get_order( $order_id );

    if ( ! $order ) {
        return;
    }

    $empresa_permitida = array( 'Shalom', 'Olva Courier' );
    $empresa = isset( $_POST['exclusive_shop_empresa_envio'] )
        ? sanitize_text_field( wp_unslash( $_POST['exclusive_shop_empresa_envio'] ) )
        : '';

    if ( ! in_array( $empresa, $empresa_permitida, true ) ) {
        $empresa = '';
    }

    $codigo = isset( $_POST['exclusive_shop_codigo_seguimiento'] )
        ? sanitize_text_field( wp_unslash( $_POST['exclusive_shop_codigo_seguimiento'] ) )
        : '';
    $numero_orden = isset( $_POST['exclusive_shop_numero_orden_envio'] )
        ? sanitize_text_field( wp_unslash( $_POST['exclusive_shop_numero_orden_envio'] ) )
        : '';

    $order->update_meta_data( '_empresa_envio', $empresa );
    $order->update_meta_data( '_codigo_seguimiento', $codigo );
    $order->update_meta_data( '_numero_orden_envio', $numero_orden );
    $order->save();
}
add_action( 'woocommerce_process_shop_order_meta', 'exclusive_shop_save_tracking_fields' );

/**
 * Muestra la información de seguimiento al cliente en el detalle de su pedido.
 * WooCommerce ya limita esta pantalla a los pedidos del cliente autenticado.
 *
 * @param WC_Order $order Pedido visualizado.
 */
function exclusive_shop_tracking_customer_details( $order ) {
    if ( ! $order instanceof WC_Order ) {
        return;
    }

    $empresa = $order->get_meta( '_empresa_envio' );
    $codigo  = $order->get_meta( '_codigo_seguimiento' );

    if ( empty( $empresa ) || empty( $codigo ) ) {
        return;
    }

    $urls = array(
        'Shalom'       => 'https://shalom.com.pe/rastrea/',
        'Olva Courier' => 'https://www.olvacourier.com/',
    );
    $url = isset( $urls[ $empresa ] ) ? $urls[ $empresa ] : '';
    ?>
    <section class="woocommerce-order-details exclusive-shop-tracking">
        <h2 class="woocommerce-order-details__title">
            <?php esc_html_e( 'Seguimiento del envío', 'exclusive-shop-tracking' ); ?>
        </h2>
        <p>
            <?php
            echo esc_html(
                sprintf( 'Empresa: %1$s · Código de tracking: %2$s', $empresa, $codigo )
            );
            ?>
        </p>
        <?php if ( $url ) : ?>
            <p>
                <a href="<?php echo esc_url( $url ); ?>" target="_blank" rel="noopener noreferrer">
                    <?php esc_html_e( 'Rastrear en el portal oficial', 'exclusive-shop-tracking' ); ?>
                </a>
            </p>
        <?php endif; ?>
    </section>
    <?php
}
add_action( 'woocommerce_order_details_after_order_table', 'exclusive_shop_tracking_customer_details' );
