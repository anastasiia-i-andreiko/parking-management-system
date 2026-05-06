async function fetchCars() {
    try {
        const res = await fetch('http://127.0.0.1:5000/api/cars');
        const cars = await res.json();

        // Знаходимо тіло таблиці саме за id "carsTable"
        const tableBody = document.querySelector("#carsTable tbody");

        if (!tableBody) {
            console.error("Помилка: Тег <tbody> не знайдено в index.html");
            return;
        }

        tableBody.innerHTML = ""; // Очищуємо стару таблицю

        cars.forEach(car => {
            const row = `<tr>
                <td>${car.plate}</td>
                <td>${car.type === 'car' ? '🚗' : '🚛'}</td>
                <td><span class="status-parked">${car.status}</span></td>
                <td><button onclick="removeCar(${car.id})">Виїзд</button></td>
            </tr>`;
            tableBody.innerHTML += row;
        });
    } catch (err) {
        console.error("Не вдалося завантажити список авто:", err);
    }
}

async function sendData() {
    const plate = document.getElementById('plate').value;
    const type = document.getElementById('type').value;

    if (!plate) {
        alert("Введіть номер!");
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
            alert("Авто додано!");
            document.getElementById('plate').value = "";
            fetchCars(); // Оновлюємо таблицю відразу
        } else {
            const errorData = await res.json();
            alert("Помилка: " + errorData.error);
        }
    } catch (err) {
        alert("Сервер не відповідає. Перевір PyCharm!");
    }
}
async function removeCar(id) {
    if (!confirm("Підтверджуєте виїзд авто?")) return;

    try {
        const res = await fetch(`http://127.0.0.1:5000/api/park/${id}`, {
            method: 'DELETE'
        });

        if (res.ok) {
            fetchCars(); // Оновлюємо таблицю після видалення
        } else {
            alert("Не вдалося видалити авто");
        }
    } catch (err) {
        console.error("Помилка при видаленні:", err);
    }
}
// Завантажуємо список при відкритті сторінки
window.onload = fetchCars;