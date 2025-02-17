window.onload = function () {
    var _quantity, _price, _in_stock, orderitem_num, delta_quantity, orderitem_quantity, delta_cost, item_total_cost;

    var quantity_arr = [];
    var price_arr = [];
    var in_stock_arr = [];

    var TOTAL_FORMS = parseInt($('input[name=orderitems-TOTAL_FORMS]').val());

    var order_total_quantity = parseInt($('.order_total_quantity').text()) || 0;
    var order_total_cost = parseFloat($('.order_total_cost').text().replace(',', '.')) || 0;


    for (var i = 0; i < TOTAL_FORMS; i++) {
        _quantity = parseInt($('input[name=orderitems-' + i + '-quantity]').val());
        _price = parseFloat($('.orderitems-' + i + '-price').text().replace(',', '.'));
        _in_stock = parseInt($('.orderitems-' + i + '-in_stock').text());

        quantity_arr[i] = _quantity;
        if (_price) {
            price_arr[i] = _price;
        } else {
            price_arr[i] = 0;
        }
        if (_in_stock) {
            in_stock_arr[i] = _in_stock;
        } else {
            in_stock_arr[i] = 0;
        }
    }

    $('.order_form').on('click', 'input[type=number]', function () {
        var target = event.target;
        orderitem_num = parseInt(target.name.replace('orderitems-', '').replace('-quantity', ''));
        if (price_arr[orderitem_num]) {
            orderitem_quantity = parseInt(target.value);
            if (orderitem_quantity <= in_stock_arr[orderitem_num]) {
                delta_quantity = orderitem_quantity - quantity_arr[orderitem_num];
                quantity_arr[orderitem_num] = orderitem_quantity;
                orderSummaryUpdate(price_arr[orderitem_num], delta_quantity);
            } else {
                document.getElementById("id_orderitems-" + orderitem_num + "-quantity").value = in_stock_arr[orderitem_num];
            }
        }
    });

    $('.order_form').on('click', 'input[type=checkbox]', function () {
        var target = event.target;
        orderitem_num = parseInt(target.name.replace('orderitems-', '').replace('-quantity', ''));

        if (target.checked) {
            delta_quantity = -quantity_arr[orderitem_num];
        } else {
            delta_quantity = quantity_arr[orderitem_num];
        }
        orderSummaryUpdate(price_arr[orderitem_num], delta_quantity);
    });


    function orderSummaryUpdate(orderitem_price, delta_quantity) {
        delta_cost = orderitem_price * delta_quantity;

        order_total_cost = Number((order_total_cost + delta_cost).toFixed(2));
        order_total_quantity = order_total_quantity + delta_quantity;
        $('.order_total_quantity').html(order_total_quantity);
        $('.order_total_cost').html(order_total_cost);
    }


    $('.formset_row').formset({
        addText: "добавить товар",
        deleteText: "удалить",
        prefix: "orderitems",
        removed: deleteOrderItem
    });

    function deleteOrderItem(row) {
        var target_name = row[0].querySelector('input[type=number]').name;
        orderitem_num = target_name.replace('orderitems-', '').replace('-quantity', '');
        delta_quantity = -quantity_arr[orderitem_num];
        orderSummaryUpdate(price_arr[orderitem_num], delta_quantity);
    }

    $('.order_form').on('change', 'select', function () {
        var target = event.target;
        orderitem_num = parseInt(target.name.replace('orderitems-', '').replace('-product', ''));
        var orderitem_product_pk = target.options[target.selectedIndex].value;

        $.ajax({
            url: '/order/product/' + orderitem_product_pk + '/price/',
            success: function (data) {
                if (data.price) {
                    price_arr[orderitem_num] = parseFloat(data.price);
                    var price_html = "<span>" + data.price.toString().replace('.', ',') + "</span> руб";
                    var curr_tr = $('.order_form table').find('tr:eq(' + (orderitem_num + 1) + ')');
                    curr_tr.find('td:eq(2)').html(price_html);
                    OrderSummaryRecalc();
                }
            },
        });
    });

    function OrderSummaryRecalc() {
        for (var i = 0; i < TOTAL_FORMS; i++) {
            order_total_quantity += quantity_arr[i];
            order_total_cost += quantity_arr[i] * price_arr[i];
        }
        $('.order_total_quantity').html(order_total_quantity.toString());
        $('.order_total_cost').html(Number(order_total_cost.toFixed(2)).toString());
    }

}
