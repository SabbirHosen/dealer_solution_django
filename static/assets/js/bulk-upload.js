const apiURL =
	'https://gist.githubusercontent.com/shahriarshafin/ef53dd78d4d7660040a393c405ed77b1/raw/5290160a09bee2029868551b70b68c5a407012f1/gistfile1.txt';
const createTableRow = (item) => `
    <tr class="bg-white border-b">
      <td scope="row" class="px-2 py-4 font-medium text-gray-900">
	  	<input type="text" name="product_name" readonly value="${item.name}" style="border:none;">
	  </td>
      <td class="px-2 py-2">
        <input min="0" type="number" value="0" class="border text-center" name="carton" data-id="${item.id}" style="max-width:50px;">
      </td>
      <td class="px-2 py-2">
        <input min="0" type="number" value="0" class="border text-center" name="piece" data-id="${item.id}" style="max-width:50px;">
      </td>
      <td class="px-2 py-2" style="max-width:50px;">
        <span id="subtotal_${item.id}">0.00</span>
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

	const productNameInput = row.querySelector('input[name="product_name"]');
	if (!productNameInput) {
		console.error('Unable to find product name input.');
		return;
	}

	const productName = productNameInput.value.trim();
	console.log(productName);
	const item = data.find((item) => item.name === productName);

	if (!item) {
		console.error('Unable to find product in API data.');
		return;
	}

	const [cartonInput, pieceInput] = Array.from(
		row.querySelectorAll('input[name="carton"], input[name="piece"]')
	).map((input) => parseFloat(input.value) || 0);

	const subtotal = (cartonInput * item.factor + pieceInput) * item.price;
	const subtotalCell = row.querySelector(`#subtotal_${item.id}`);

	if (subtotalCell) {
		subtotalCell.innerText = `${subtotal.toFixed(2)}`;
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
	totalSum.value = total.toFixed(2);
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
