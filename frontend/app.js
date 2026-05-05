const API_URL = "http://127.0.0.1:5000/api";

async function fetchCars() {
    const response = await fetch(`${API_URL}/cars`);
    const cars = await response.json();
    const tableBody = document.querySelector("#carsTable tbody");
    tableBody.innerHTML = "";
    cars.forEach(car => {
        const row = `<tr>
            <td>${car.plate}</td>
            <td>${car.type}</td>
            <td>${car.status}</td>
            <td>${car.status === 'parked' ? `<button onclick="exitCar(${car.id})">Виїзд</button>` : car.entry}</td>
        </tr>`;
        tableBody.insertAdjacentHTML('beforeend', row);
    });
}

async function sendData() {
    const plate = document.getElementById('plate').value;
    const type = document.getElementById('type').value;
    await fetch(`${API_URL}/park`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ plate_number: plate, vehicle_type: type })
    });
    fetchCars();
}

async function exitCar(id) {
    await fetch(`${API_URL}/exit/${id}`, { method: 'PATCH' });
    fetchCars();
}

document.getElementById('addBtn').addEventListener('click', sendData);
window.onload = fetchCars;