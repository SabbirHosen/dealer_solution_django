const apiURL =
    'product-info-api/';
const createTableRow = (item) => `
    <tr class="bg-white border-b">
		<input type="hidden" name="product_id" readonly value="${item.id}" style="border:none;">
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

    const productId = parseInt(
        row.querySelector('input[name="product_id"]').value,
        10
    );
    // console.log('Product ID:', productId);

    const item = data.find((item) => item.id === productId);

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
    // console.log('Total:', total.toFixed(2));
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
