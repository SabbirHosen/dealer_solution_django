const apiURL =
	'https://gist.githubusercontent.com/shahriarshafin/8904d575acfb07eb00d12be63416f19f/raw/1e0a9d95b9726a7db49cc55c30315bb84e024e3a/gistfile1.txt';

const createTableRow = (item) => {
	const remainingStock = item.stock - item.returnProduct;

	return `
    <tr class="bg-white border-b">
        <input type="hidden" name="product_id" readonly value="${item.id}" style="border:none;">
        <td scope="row" class="px-2 py-4 font-medium text-gray-900">
            <input type="text" name="product_name" readonly value="${item.productName}" style="border:none;">
        </td>
        <td class="px-2 py-2">
            <input min="0" max="${item.stock}" type="number" value="${item.returnProduct}" readonly class="text-center return-input" name="return" style="max-width:50px;">
        </td>
        <td class="px-2 py-2">
            <input min="0" max="${remainingStock}" type="number" value="0" class="border text-center" name="receive" style="min-width:60px;">
        </td>
    </tr>
  `;
};

const updateReceiveMax = (returnInput, receiveInput) => {
	const remainingStock =
		parseInt(returnInput.getAttribute('max')) - parseInt(returnInput.value);
	receiveInput.setAttribute('max', remainingStock);
	if (parseInt(receiveInput.value) > remainingStock) {
		receiveInput.value = remainingStock;
	}
};

const populateTable = (data) => {
	const tableBody = document.getElementById('productTableBody');
	tableBody.innerHTML = data.map(createTableRow).join('');

	// Add event listener to the checkbox
	const returnCheck = document.getElementById('returnCheck');
	const returnInputs = document.querySelectorAll('.return-input');

	returnCheck.addEventListener('change', function () {
		returnInputs.forEach((input) => {
			const correspondingReceiveInput =
				input.parentElement.nextElementSibling.querySelector(
					'input[name="receive"]'
				);

			if (this.checked) {
				input.value = input.getAttribute('data-original-value');
			} else {
				input.value = 0;
				correspondingReceiveInput.value = 0; // Resetting to 0 when checkbox is unchecked
			}

			updateReceiveMax(input, correspondingReceiveInput);
		});
	});

	// Save the original values for later reference
	returnInputs.forEach((input) => {
		const correspondingReceiveInput =
			input.parentElement.nextElementSibling.querySelector(
				'input[name="receive"]'
			);
		input.setAttribute('data-original-value', input.value);
		updateReceiveMax(input, correspondingReceiveInput);
	});

	// Add event listener to the return input
	returnInputs.forEach((input) => {
		const correspondingReceiveInput =
			input.parentElement.nextElementSibling.querySelector(
				'input[name="receive"]'
			);
		input.addEventListener('input', function () {
			updateReceiveMax(this, correspondingReceiveInput);
		});
	});
};

fetch(apiURL)
	.then((response) => response.json())
	.then((data) => {
		populateTable(data);
		window.data = data;
	})
	.catch((error) => {
		console.error('Error fetching data:', error);
		// Add code to handle the error, e.g., display a message to the user
	});
