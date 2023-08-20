const toastContainer = document.getElementById('toastContainer');
const pageForm = document.getElementById('pageForm');
const datePicker = document.getElementById('datePicker');
const samePriceBtn = document.getElementById('samePriceBtn');
const totalPriceField = document.getElementById('totalPriceField');
const cashField = document.getElementById('cashField');
const customerNameField = document.getElementById('customerName');
const dueField = document.getElementById('dueField');
const dueInfo = document.getElementById('dueInfo');
const numberInput = document.getElementById('numberInput');
const suggestionsList = document.getElementById('suggestionsList');

const BASE_URL = 'https://dealersolutions.com/api';
// const CUSTOMER = `${BASE_URL}/auth/register`;
const CUSTOMER =
	'/retailer/api/customer-info/';

// Toast hide and show on internet availability
window.addEventListener('online', () => {
	toastContainer.style.display = 'none';
	document.body.style.pointerEvents = 'auto';
});
window.addEventListener('offline', () => {
	toastContainer.style.display = 'block';
	document.body.style.pointerEvents = 'none';
});

// Hold link or inspect page restrict
document.addEventListener(
	'contextmenu',
	(event) => {
		event.preventDefault();
	},
	false
);

// Toast config
const toastConfig = {
	text: '',
	duration: 2500,
	newWindow: true,
	gravity: 'top',
	position: 'center',
	style: {
		background: '#26af61',
	},
};

// Today's date selected
if (datePicker) {
	const today = new Date();
	const year = today.getFullYear();
	const month = String(today.getMonth() + 1).padStart(2, '0');
	const day = String(today.getDate()).padStart(2, '0');
	datePicker.value = `${year}-${month}-${day}`;
}

// Hiding customer info
if (samePriceBtn) {
	samePriceBtn.addEventListener('click', function (event) {
		event.preventDefault();
		numberInput.removeAttribute('required');
		customerNameField.removeAttribute('required');
		cashField.value = totalPriceField.value;
		if (dueInfo) {
			dueInfo.style.display = 'none';
		}
	});
}

// Due calculation
const updateDueField = () => {
	if (dueField) {
		dueField.value =
			cashField.value === '' ? 0 : totalPriceField.value - cashField.value;
	}
	// Reset the value in the second input field if it exceeds the new maximum
	if (cashField.value > totalPriceField.value) {
		// cashField.value = '';
	}
};
if (cashField) {
	cashField.addEventListener('input', updateDueField);
}
if (cashField) {
	totalPriceField.addEventListener('input', updateDueField);
}

// Name, Phone, DueAmount auto suggestion
let suggestions = [];
const fetchSuggestions = async () => {
	try {
		const response = await fetch(CUSTOMER);
		const data = await response.json();

		suggestions = data.map(({ phone, name }) => ({
			phone,
			name,
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

		matchingSuggestions.forEach(({ phone, name }) => {
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
			});
			suggestionsList.appendChild(li);
		});
	}
};
numberInput.addEventListener('input', showSuggestions);
fetchSuggestions();
