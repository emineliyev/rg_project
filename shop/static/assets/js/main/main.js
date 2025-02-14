document.addEventListener('DOMContentLoaded', () => {
    /*** 🛒 Обновление цены при выборе веса ***/
    function setupWeightOptions() {
        const weightOptions = document.getElementById('weightOptions');
        const finalPriceElement = document.getElementById('finalPrice');
        const originalPriceElement = document.getElementById('originalPrice');

        if (!finalPriceElement || !originalPriceElement) return;

        const basePrice = parseFloat(originalPriceElement?.dataset.basePrice || 0);
        const discountedPrice = parseFloat(finalPriceElement?.dataset.discountedPrice || basePrice);

        if (weightOptions) {
            weightOptions.addEventListener('change', () => {
                const selectedOption = weightOptions.options[weightOptions.selectedIndex];
                const priceModifier = parseFloat(selectedOption.dataset.priceModifier || 0);
                finalPriceElement.textContent = `${(discountedPrice + priceModifier).toFixed(2)}₼`;
            });
        }
    }

    /*** 📂 Открытие подменю ***/
    function setupMenuToggle() {
        const menuItems = document.querySelectorAll('.menu-item.has-children');
        menuItems.forEach((item) => {
            item.addEventListener('click', (event) => {
                event.preventDefault();
                const submenu = item.nextElementSibling;
                const arrow = item.querySelector('.arrow');
                if (submenu) submenu.classList.toggle('open');
                if (arrow) arrow.classList.toggle('open');
            });
        });
    }

    /*** 💰 Фильтр цен ***/
    function setupPriceFilter() {
        const form = document.getElementById('price-filter-form');
        const priceMinInput = document.getElementById('price_min');
        const priceMaxInput = document.getElementById('price_max');
        const leftLabel = document.querySelector('.tm-rangeslider-leftlabel');
        const rightLabel = document.querySelector('.tm-rangeslider-rightlabel');
        const slider = document.querySelector('.tm-rangeslider');

        if (!slider) {
            console.warn('Элемент .tm-rangeslider не найден, функционал ползунка отключён.');
            return;
        }

        let minValue = parseFloat(slider.getAttribute('data-cur_min')) || 0;
        let maxValue = parseFloat(slider.getAttribute('data-cur_max')) || 100;

        function updateValues(min, max) {
            if (priceMinInput) priceMinInput.value = min;
            if (priceMaxInput) priceMaxInput.value = max;
            if (leftLabel) leftLabel.textContent = min;
            if (rightLabel) rightLabel.textContent = max;
        }

        slider.addEventListener('mousemove', (event) => {
            const rect = slider.getBoundingClientRect();
            const percent = (event.clientX - rect.left) / rect.width;

            if (event.target.classList.contains('tm-rangeslider-leftgrip')) {
                minValue = Math.max(0, Math.min(maxValue - 1, percent * (slider.dataset.range_max || 100)));
            } else if (event.target.classList.contains('tm-rangeslider-rightgrip')) {
                maxValue = Math.min((slider.dataset.range_max || 100), Math.max(minValue + 1, percent * (slider.dataset.range_max || 100)));
            }

            updateValues(minValue.toFixed(0), maxValue.toFixed(0));
        });

        form.addEventListener('submit', () => updateValues(minValue.toFixed(0), maxValue.toFixed(0)));
    }

    /*** 🎥 Перетаскиваемое видео ***/
    function setupDraggableVideo() {
        const videoContainer = document.getElementById('draggable-video');
        if (!videoContainer) return;

        let isDragging = false;
        let isExpanded = false;
        let offsetX, offsetY;

        const closeButton = document.createElement('button');
        closeButton.innerHTML = '&times;';
        closeButton.classList.add('close-button');
        videoContainer.appendChild(closeButton);

        videoContainer.addEventListener('mousedown', (e) => {
            if (e.target === closeButton || isExpanded) return;
            isDragging = true;
            offsetX = e.clientX - videoContainer.offsetLeft;
            offsetY = e.clientY - videoContainer.offsetTop;
            videoContainer.classList.add('dragging');
        });

        document.addEventListener('mousemove', (e) => {
            if (isDragging) {
                videoContainer.style.left = `${e.clientX - offsetX}px`;
                videoContainer.style.top = `${e.clientY - offsetY}px`;
            }
        });

        document.addEventListener('mouseup', () => {
            if (isDragging) {
                isDragging = false;
                videoContainer.classList.remove('dragging');
            }
        });

        videoContainer.addEventListener('click', (e) => {
            if (e.target.tagName === 'VIDEO' && !isDragging) {
                isExpanded = !isExpanded;
                videoContainer.classList.toggle('expanded', isExpanded);
            }
        });

        closeButton.addEventListener('click', () => {
            videoContainer.style.display = 'none';
        });
    }

    /*** 🔔 Удаление сообщений (Toast) ***/
    function setupToastMessages() {
        document.querySelectorAll('.toast-message').forEach((toast) => {
            setTimeout(() => {
                toast.style.transition = 'opacity 0.5s ease-out';
                toast.style.opacity = '0';
                setTimeout(() => toast.remove(), 500);
            }, 5000);
        });
    }

    /*** ✅ Переключение кнопки при выборе чекбокса ***/
    function setupCheckoutButton() {
        const checkbox = document.getElementById('checkout-read-terms');
        const submitButton = document.getElementById('submit-button');
        if (checkbox && submitButton) {
            checkbox.addEventListener('change', () => {
                submitButton.disabled = !checkbox.checked;
            });
        }
    }

    /*** 🚀 Вызов всех функций ***/
    setupWeightOptions();
    setupMenuToggle();
    setupPriceFilter();
    setupDraggableVideo();
    setupToastMessages();
    setupCheckoutButton();
});
