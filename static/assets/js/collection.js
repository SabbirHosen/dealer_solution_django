const datePicker = document.getElementById('datePicker');
const customerNameField = document.getElementById('customerName');
const samePriceBtn = document.getElementById('samePriceBtn');

const BASE_URL = 'https://dealersolutions.com/api';
// const CUSTOMER = `${BASE_URL}/auth/register`;
const CUSTOMER =
	'http://127.0.0.1:8000/retailer/api/customer-info/';

// Today's date selected
datePicker.value = new Date().toISOString().substring(0, 10);

// Copy same amount
samePriceBtn.addEventListener('click', function (event) {
	event.preventDefault();
	cashField.value = dueAmountField.value;
});

// Name, Phone, DueAmount auto suggestion
let suggestions = [];
const fetchSuggestions = async () => {
	try {
		const response = await fetch(CUSTOMER);
		const data = await response.json();

		suggestions = data.map(({ phone, name, dueAmount }) => ({
			phone,
			name,
			dueAmount,
		}));

		showSuggestions();
	} catch (error) {
		console.error('Error fetching suggestions:', error);
	}
};

const showSuggestions = () => {
	const inputNumber = numberInput.value;
	suggestionsList.innerHTML = '';

	if (inputNumber) {
		const matchingSuggestions = suggestions.filter(({ phone }) =>
			phone.toLowerCase().includes(inputNumber.toLowerCase())
		);

		matchingSuggestions.forEach(({ phone, name, dueAmount }) => {
			const li = document.createElement('li');
			li.textContent = phone;
			li.classList.add(
				'py-1',
				'px-2',
				'cursor-pointer',
				'hover:bg-gray-100',
				'rounded-sm'
			);
			li.addEventListener('click', () => {
				numberInput.value = phone;
				suggestionsList.innerHTML = '';
				customerNameField.value = name;
				dueAmountField.value = dueAmount;
			});
			suggestionsList.appendChild(li);
		});
	}
};
numberInput.addEventListener('input', showSuggestions);
fetchSuggestions();
