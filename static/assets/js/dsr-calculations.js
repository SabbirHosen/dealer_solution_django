let currentURL = window.location.href;
let endpoint = '/dsr/product-list/';
const apiURL = currentURL + endpoint;
console.log(apiURL);

const createTableRow = (item) => {
    return `
        <tr class="bg-white border-b">
            <input type="hidden" name="product_id" readonly value="${item.id}" style="border:none;">
            <td scope="row" class="px-2 py-4 font-medium text-gray-900">
                <input type="text" name="product_name" readonly value="${item.productName}" style="border:none;">
            </td>
            <td class="px-2 py-2">
                <input min="0" max="${item.stock}" type="number" value="0" class="border text-center return-input" name="return" style="min-width:60px;">
            </td>
            <td class="px-2 py-2">
                <input min="0" max="${item.stock}" type="number" value="0" class="border text-center receive-input" name="damage" style="min-width:60px;">
            </td>
        </tr>
    `;
};

const updateInputValues = (returnInput, receiveInput, maxStock) => {
    let returnVal = parseInt(returnInput.value) || 0;
    let receiveVal = parseInt(receiveInput.value) || 0;
    let sum = returnVal + receiveVal;

    if (sum > maxStock) {
        if (returnVal > maxStock) {
            returnInput.value = maxStock;
            receiveInput.value = 0;
        } else {
            receiveInput.value = maxStock - returnVal;
        }
    }
};

const addEventListeners = () => {
    document.querySelectorAll('.return-input').forEach((returnInput) => {
        const row = returnInput.closest('tr');
        const receiveInput = row.querySelector('.receive-input');
        const maxStock = parseInt(returnInput.getAttribute('max'));

        returnInput.addEventListener('input', () =>
            updateInputValues(returnInput, receiveInput, maxStock)
        );
    });

    document.querySelectorAll('.receive-input').forEach((receiveInput) => {
        const row = receiveInput.closest('tr');
        const returnInput = row.querySelector('.return-input');
        const maxStock = parseInt(returnInput.getAttribute('max'));

        receiveInput.addEventListener('input', () =>
            updateInputValues(returnInput, receiveInput, maxStock)
        );
    });
};

const populateTable = (data) => {
    const tableBody = document.getElementById('productTableBody');
    tableBody.innerHTML = data.map(createTableRow).join('');
};

fetch(apiURL)
    .then((response) => response.json())
    .then((data) => {
        populateTable(data);
        window.data = data;
        addEventListeners();
    })
    .catch((error) => {
        console.error('Error fetching data:', error);
        // Handle the error
    });
