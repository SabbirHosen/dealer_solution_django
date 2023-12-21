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
            <input min="0"  type="number" value="0" max="${item.stock}" class="border text-center return-input" name="return" style="max-width:50px;">
        </td>
        <td class="px-2 py-2">
            <input min="0"  type="number" value="0" class="border text-center" name="damage" style="max-width:50px;">
        </td>
    </tr>
  `;
};

const populateTable = (data) => {
    const tableBody = document.getElementById('productTableBody');
    tableBody.innerHTML = data.map(createTableRow).join('');
};

fetch(apiURL)
    .then((response) => response.json())
    .then((data) => {
        populateTable(data);
    })
    .catch((error) => {
        console.error('Error fetching data:', error);
    });
