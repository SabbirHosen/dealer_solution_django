const BASE_URL =
	'api';

const dayBtn = document.getElementById('dayBtn');
const weekBtn = document.getElementById('weekBtn');
const monthBtn = document.getElementById('monthBtn');
const halfYearBtn = document.getElementById('halfYearBtn');
const yearBtn = document.getElementById('yearBtn');
const chooseStatusSelect = document.getElementById('chooseStatus');

dayBtn.addEventListener('click', function () {
	handleButtonClick('day');
});

weekBtn.addEventListener('click', function () {
	handleButtonClick('week');
});

monthBtn.addEventListener('click', function () {
	handleButtonClick('month');
});

halfYearBtn.addEventListener('click', function () {
	handleButtonClick('halfYear');
});

yearBtn.addEventListener('click', function () {
	handleButtonClick('year');
});

chooseStatusSelect.addEventListener('change', function () {
	handleButtonClick(getTimePeriod());
});

window.addEventListener('load', function () {
	dayBtn.click();
});

function handleButtonClick(timePeriod) {
	const selectedValue = chooseStatusSelect.value;

	let apiUrl;
	switch (selectedValue) {
		case 'buySell':
			apiUrl = `${BASE_URL}/buy-sell/${timePeriod}`;
			// apiUrl = `${BASE_URL}`;
			break;
		case 'collection':
			apiUrl = `${BASE_URL}/collection/${timePeriod}`;
			break;
		case 'expences':
			apiUrl = `${BASE_URL}/expences/${timePeriod}`;
			break;
		case 'dueSummary':
			apiUrl = `${BASE_URL}/due-summary/${timePeriod}`;
			break;
		default:
			return;
	}

	fetchData(apiUrl);
	removeActiveClass();
	setActiveButton(timePeriod);
}

function removeActiveClass() {
	dayBtn.classList.remove('active');
	weekBtn.classList.remove('active');
	monthBtn.classList.remove('active');
	halfYearBtn.classList.remove('active');
	yearBtn.classList.remove('active');
}

function setActiveButton(timePeriod) {
	switch (timePeriod) {
		case 'day':
			dayBtn.classList.add('active');
			break;
		case 'week':
			weekBtn.classList.add('active');
			break;
		case 'month':
			monthBtn.classList.add('active');
			break;
		case 'halfYear':
			halfYearBtn.classList.add('active');
			break;
		case 'year':
			yearBtn.classList.add('active');
			break;
		default:
			break;
	}
}

function fetchData(apiUrl) {
	fetch(apiUrl)
		.then((response) => response.json())
		.then((data) => {
			const wrapperDiv = document.getElementById('wrapper');
			wrapperDiv.innerHTML = '';

			let totalAmount = 0;

			data.forEach((item) => {
				const htmlString = `
                    <div class="bg-gray-200/80 shadow px-2 py-2 rounded-sm flex justify-between items-center">
                        <p class="text-sm text-gray-500">তারিখ: <span>${item.date}</span></p>
                        <div>
                            <p class="font-semibold">৳ <span>${item.amount}</span></p>
                        </div>
                    </div>
                `;
				wrapperDiv.insertAdjacentHTML('beforeend', htmlString);

				totalAmount += item.amount;
			});

			const totalAmountElement = document.getElementById('totalAmount');
			totalAmountElement.textContent = totalAmount;
		})
		.catch((error) => {
			console.log('Error:', error);
		});
}

function getTimePeriod() {
	const timePeriodButtons = [dayBtn, weekBtn, monthBtn, halfYearBtn, yearBtn];
	for (const button of timePeriodButtons) {
		if (button.classList.contains('active')) {
			return button.getAttribute('data-time-period');
		}
	}
	return null;
}