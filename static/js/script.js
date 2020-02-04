/*

 */

(function () {
    var MAX_PIZZA_COUNTER = 100;
    var MIN_PIZZA_COUNTER = 1;

    var products = document.querySelectorAll('.catalog__item');

    /**
     * Adds event listeners for product card buttons
     * @param {HTMLButtonElement} plusButton
     * @param {HTMLButtonElement} minusButton
     * @param {HTMLInputElement} quantityField
     */
    var addQuantityButtonsClickListener = function (plusButton, minusButton, quantityField) {
        plusButton.addEventListener('click', function (evt) {
            evt.preventDefault();
            var quantity = parseInt(quantityField.value, 10);
            if (quantity < MAX_PIZZA_COUNTER) {
                quantity++;
            }
            quantityField.value = quantity.toString();
        });

        minusButton.addEventListener('click', function (evt) {
            evt.preventDefault();
            var quantity = parseInt(quantityField.value, 10);
            if (quantity > MIN_PIZZA_COUNTER) {
                quantity--;
            }
            quantityField.value = quantity.toString();
        });
    };


    products.forEach(function (product) {
        var plusButton = product.querySelector('.catalog__item-plus');
        var minusButton = product.querySelector('.catalog__item-minus');
        var quantityField = product.querySelector('.catalog__item-quantity');

        addQuantityButtonsClickListener(plusButton, minusButton, quantityField);
    })
})();