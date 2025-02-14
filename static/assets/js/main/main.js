document.addEventListener('DOMContentLoaded', () => {
    const weightOptions = document.getElementById('weightOptions');
    const finalPriceElement = document.getElementById('finalPrice');
    const originalPriceElement = document.getElementById('originalPrice');

    // Проверяем, существуют ли элементы
    if (!finalPriceElement || !originalPriceElement) {
        return;
    }

    // Получаем базовую цену из атрибутов
    const basePrice = parseFloat(originalPriceElement?.dataset.basePrice || 0);
    const discountedPrice = parseFloat(finalPriceElement?.dataset.discountedPrice || basePrice);

    if (weightOptions) {
        weightOptions.addEventListener('change', () => {
            const selectedOption = weightOptions.options[weightOptions.selectedIndex];
            const priceModifier = parseFloat(selectedOption.dataset.priceModifier || 0);

            // Рассчитываем финальную цену с учетом скидки и веса
            const finalPrice = discountedPrice + priceModifier;

            // Обновляем отображаемую цену
            finalPriceElement.textContent = `${finalPrice.toFixed(2)}₼`;
        });
    } else {
        console.log("Опции веса не найдены для данного товара.");
    }
});


document.addEventListener("DOMContentLoaded", function () {
    const menuItems = document.querySelectorAll(".menu-item.has-children");

    menuItems.forEach((item) => {
        item.addEventListener("click", function (event) {
            event.preventDefault(); // Предотвращаем переход по ссылке

            const submenu = item.nextElementSibling;
            const arrow = item.querySelector(".arrow");

            if (submenu) {
                submenu.classList.toggle("open");
                arrow.classList.toggle("open");
            }
        });
    });
});