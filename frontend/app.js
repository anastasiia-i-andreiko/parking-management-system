// Функція для отримання списку авто з сервера
async function fetchCars() {
    try {
        const res = await fetch('http://127.0.0.1:5000/api/cars');
        const cars = await res.json();

        // Знаходимо тіло таблиці
        const tableBody = document.querySelector("#carsTable tbody");

        if (!tableBody) {
            console.error("Помилка: Тег <tbody> не знайдено в index.html");
            return;
        }

        tableBody.innerHTML = ""; // Очищуємо таблицю перед оновленням

        cars.forEach(car => {
            // Визначаємо іконку залежно від типу
            const icon = car.type === 'truck' ? '🚛' : '🚗';

            const row = `
                <tr>
                    <td>${car.plate}</td>
                    <td>${icon}</td>
                    <td>${car.entry || '--:--'}</td>
                    <td><span class="status-parked">${car.status}</span></td>
                    <td>
                        <button class="btn-exit" onclick="removeCar(${car.id})">Виїзд</button>
                    </td>
                </tr>
            `;
            tableBody.innerHTML += row;
        });
    } catch (err) {
        console.error("Не вдалося завантажити список авто:", err);
    }
}

// Функція для додавання нового авто
async function sendData() {
    const plateInput = document.getElementById('plate');
    const typeInput = document.getElementById('type');

    const plate = plateInput.value.trim();
    const type = typeInput.value;

    if (!plate) {
        alert("Будь ласка, введіть номер автомобіля!");
        return;
    }

    try {
        const res = await fetch('http://127.0.0.1:5000/api/park', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                plate_number: plate,
                vehicle_type: type
            })
        });

        if (res.ok) {
            alert("Авто успішно додано на парковку!");
            plateInput.value = ""; // Очищуємо поле вводу
            fetchCars(); // Оновлюємо таблицю
        } else {
            const errorData = await res.json();
            alert("Помилка: " + errorData.error);
        }
    } catch (err) {
        alert("Сервер не відповідає. Переконайтеся, що Flask запущений!");
    }
}

// Функція для оформлення виїзду (видалення)
async function removeCar(id) {
    // Отримуємо поточний час для повідомлення
    const now = new Date();
    const exitTime = now.getHours().toString().padStart(2, '0') + ":" +
                     now.getMinutes().toString().padStart(2, '0');

    if (!confirm(`Підтвердити виїзд авто о ${exitTime}?`)) return;

    try {
        const res = await fetch(`http://127.0.0.1:5000/api/park/${id}`, {
            method: 'DELETE'
        });

        if (res.ok) {
            alert(`Авто покинуло парковку о ${exitTime}`);
            fetchCars(); // Оновлюємо список
        } else {
            alert("Не вдалося видалити автомобіль.");
        }
    } catch (err) {
        console.error("Помилка видалення:", err);
        alert("Помилка з'єднання з сервером.");
    }
}

// Завантажуємо дані відразу при відкритті сторінки
window.onload = fetchCars;