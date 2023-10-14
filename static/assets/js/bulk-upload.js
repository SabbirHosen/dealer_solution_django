const apiURL =
	'https://gist.githubusercontent.com/shahriarshafin/3495d4ff4856b57dfc904811489e1709/raw/d1ea350e479cc9e6dabce4754497ad814ca4a087/gistfile1.txt';

const createTableRow = (item) => `
    <tr class="bg-white border-b">
      <td scope="row" class="px-2 py-4 font-medium text-gray-900">${item.name}</td>
      <td class="px-2 py-2">
        <input min="0" type="number" placeholder="0" class="border max-w-[50px]" data-id="${item.id}">
      </td>
      <td class="px-2 py-2">
        <input min="0" type="number" placeholder="0" class="border max-w-[50px]" data-id="${item.id}">
      </td>
      <td class="px-2 py-2">
        <span id="subtotal_${item.id}">$0.00</span>
      </td>
    </tr>
  `;

const populateTable = (data) => {
	const tableBody = document.getElementById('productTableBody');
	tableBody.innerHTML = data.map(createTableRow).join('');
};

const calculateSubtotal = (element) => {
	const row = element.closest('tr');
	if (!row) {
		console.error('Unable to find parent row.');
		return;
	}

	const [cartoonInput, pieceInput] = Array.from(
		row.querySelectorAll('input')
	).map((input) => parseFloat(input.value) || 0);
	const productName = row.querySelector('td:first-child').innerText.trim();
	const item = data.find((item) => item.name === productName);

	if (!item) {
		console.error('Unable to find product in API data.');
		return;
	}

	const subtotal = (cartoonInput * item.factor + pieceInput) * item.price;
	const subtotalCell = row.querySelector(`#subtotal_${item.id}`);

	if (subtotalCell) {
		subtotalCell.innerText = `$${subtotal.toFixed(2)}`;
		calculateTotal();
	}
};

const calculateTotal = () => {
	const subtotalCells = document.querySelectorAll(
		'tbody#productTableBody td:last-child'
	);
	const total = [...subtotalCells].reduce(
		(acc, cell) => acc + parseFloat(cell.innerText.replace('$', '')),
		0
	);
	const totalSum = document.getElementById('total');
	totalSum.innerHTML = total.toFixed(2);
	console.log('Total:', total.toFixed(2));
};

fetch(apiURL)
	.then((response) => response.json())
	.then((data) => {
		populateTable(data);
		window.data = data;
	})
	.catch((error) => console.error('Error fetching data:', error));

const productTableBody = document.getElementById('productTableBody');
productTableBody.addEventListener('input', (event) => {
	if (event.target.tagName === 'INPUT') {
		calculateSubtotal(event.target);
	}
});
