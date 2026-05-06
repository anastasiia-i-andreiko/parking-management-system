const API_URL = "http://127.0.0.1:5000/api";

async function fetchCars() {
    try {
        const res = await fetch(`${API_URL}/cars`);
        const cars = await res.json();
        const tableBody = document.querySelector("#carsTable tbody");

        tableBody.innerHTML = "";

        cars.forEach(car => {
            // Вибір іконки за типом
            let icon = '🚗';
            switch(car.type) {
                case 'truck': icon = '🚛'; break;
                case 'motorcycle': icon = '🏍️'; break;
                case 'bus': icon = '🚌'; break;
                case 'bicycle': icon = '🚲'; break;
                case 'electro': icon = '⚡'; break;
                default: icon = '🚗';
            }

            const row = `
                <tr>
                    <td>${car.plate}</td>
                    <td><span style="font-size: 1.5rem;">${icon}</span></td>
                    <td>${car.entry || '--:--'}</td>
                    <td><span class="status-parked">Паркується</span></td>
                    <td><button class="btn-exit" onclick="removeCar(${car.id})">Виїзд</button></td>
                </tr>
            `;
            tableBody.innerHTML += row;
        });
    } catch (err) {
        console.error("Помилка завантаження:", err);
    }
}

async function sendData() {
    const plate = document.getElementById('plate').value;
    const type = document.getElementById('type').value;

    if (!plate) return alert("Введіть номер!");

    try {
        const res = await fetch(`${API_URL}/park`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ plate_number: plate, vehicle_type: type })
        });

        if (res.ok) {
            document.getElementById('plate').value = "";
            fetchCars();
        }
    } catch (err) {
        alert("Сервер не відповідає!");
    }
}

async function removeCar(id) {
    if (!confirm("Підтвердити виїзд?")) return;
    try {
        const res = await fetch(`${API_URL}/park/${id}`, { method: 'DELETE' });
        if (res.ok) fetchCars();
    } catch (err) {
        alert("Помилка видалення.");
    }
}

window.onload = fetchCars;