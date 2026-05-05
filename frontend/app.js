const API_URL = "http://127.0.0.1:5000/api";

// 1. Функція для отримання списку авто з сервера
async function fetchCars() {
    try {
        const response = await fetch(`${API_URL}/cars`);
        const cars = await response.json();

        const tableBody = document.querySelector("#carsTable tbody");
        tableBody.innerHTML = ""; // Очищуємо таблицю перед оновленням

        cars.forEach(car => {
            // Визначаємо клас для кольорового підсвічування рядка (зелений або сірий)
            const statusClass = car.status === 'left' ? 'status-left' : 'status-parked';

            const row = `
                <tr class="${statusClass}">
                    <td><strong>${car.plate}</strong></td>
                    <td>${car.type === 'car' ? '🚗 Авто' : '🏍️ Мото'}</td>
                    <td>${car.status === 'parked' ? '✅ На парковці' : '⚪ Виїхав'}</td>
                    <td>
                        ${car.status === 'parked'
                            ? `<button onclick="exitCar(${car.id})">Виїзд</button>`
                            : `<small>${car.entry}</small>`}
                    </td>
                </tr>
            `;
            tableBody.insertAdjacentHTML('beforeend', row);
        });
    } catch (error) {
        console.error("Помилка отримання даних:", error);
    }
}

// 2. Функція для додавання нового авто на парковку
async function sendData() {
    const plateInput = document.getElementById('plate');
    const typeInput = document.getElementById('type');

    const plate = plateInput.value.trim();
    const type = typeInput.value;

    if (!plate) {
        alert("Будь ласка, введіть номер автомобіля! ✍️");
        return;
    }

    const data = {
        plate_number: plate,
        vehicle_type: type
    };

    try {
        const response = await fetch(`${API_URL}/park`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });

        if (response.ok) {
            plateInput.value = ""; // Очищуємо поле після успіху
            fetchCars(); // Оновлюємо таблицю, щоб побачити нове авто
        } else {
            const err = await response.json();
            alert("Помилка: " + (err.error || "Не вдалося додати авто"));
        }
    } catch (error) {
        alert("Сервер не відповідає. Перевір, чи запущено backend/main.py!");
    }
}

// 3. Функція для фіксації виїзду авто
async function exitCar(id) {
    try {
        const response = await fetch(`${API_URL}/exit/${id}`, {
            method: 'PATCH'
        });

        if (response.ok) {
            fetchCars(); // Оновлюємо список
        } else {
            alert("Не вдалося оформити виїзд.");
        }
    } catch (error) {
        console.error("Помилка при виїзді:", error);