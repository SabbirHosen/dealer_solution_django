let currentURL = window.location.href;
let endpoint = '/dsr/product-list/';
const apiURL = currentURL + endpoint;
console.log(apiURL);

const productsContainer = document.getElementById('productsContainer');
const sellingPriceElement = document.getElementById('sellingPrice');
const damagePriceElement = document.getElementById('damagePrice');
const totalSellingPriceElement = document.getElementById('totalSellingPrice');
const discountInput = document.getElementById('discount');
const finalAmountElement = document.getElementById('finalAmount');
const dueCash = document.getElementById('dueCash');
const deposit = document.getElementById('deposit');

// Toast config
const toastConfig = {
    text: '',
    duration: 3500,
    newWindow: true,
    gravity: 'top',
    position: 'center',
};

const updateFinalAmount = () => {
    const totalSellingPrice = parseFloat(totalSellingPriceElement.value) || 0;
    const discountValue = parseFloat(discountInput.value) || 0;
    const finalAmount = Math.max(0, totalSellingPrice - discountValue);
    finalAmountElement.value = finalAmount.toFixed(2);
    finalAmountElement.value = finalAmount.toFixed(2);
    updateDueCash();
};

const updateDueCash = () => {
    const finalAmount = parseFloat(finalAmountElement.value) || 0;
    const depositValue = parseFloat(deposit.value) || 0;
    const dueCashValue = finalAmount - depositValue;
    dueCash.value = dueCashValue.toFixed(2);
};

const updatePrices = (productDiv, item) => {
    const productReturn =
        parseFloat(productDiv.querySelector('[name="product_return"]').value) || 0;
    const productDamage =
        parseFloat(productDiv.querySelector('[name="product_damage"]').value) || 0;

    // Check if the sum of productReturn and productDamage exceeds the stock
    const sumOfReturnsAndDamages = productReturn + productDamage;
    if (sumOfReturnsAndDamages > item.stock) {
        Toastify({
            ...toastConfig,
            text: `পণ্যের পরিমাণ বর্তমান স্টক ${item.stock} হতে অতিক্রম করেছে`,
            style: {background: '#f43f5e'},
        }).showToast();

        // Reset the return and damage input values
        productDiv.querySelector('[name="product_return"]').value = 0;
        productDiv.querySelector('[name="product_damage"]').value = 0;

        // Also reset the selling price and damage price inputs
        const sellingPriceInput = productDiv.querySelector(
            '[name="product_selling_price"]'
        );
        const damagePriceInput = productDiv.querySelector(
            '[name="product_damage_price"]'
        );
        if (sellingPriceInput && damagePriceInput) {
            sellingPriceInput.value = 0;
            damagePriceInput.value = 0;
        } else {
            console.error('Input fields for selling and damage prices not found');
        }

        // Update the total prices and final amount
        calculateTotalPrices();
        updateFinalAmount();
        return;
    }

    const sellingPrice =
        productReturn === 0 ? 0 : (item.stock - productReturn) * item.productPrice;
    const damagePrice = item.productPrice * productDamage;

    const sellingPriceInput = productDiv.querySelector(
        '[name="product_selling_price"]'
    );
    const damagePriceInput = productDiv.querySelector(
        '[name="product_damage_price"]'
    );

    if (sellingPriceInput && damagePriceInput) {
        sellingPriceInput.value = sellingPrice.toFixed(2);
        damagePriceInput.value = damagePrice.toFixed(2);
    } else {
        console.error('Input fields not found');
    }

    calculateTotalPrices();
    updateFinalAmount();
};

const createProductDiv = (item) => {
    const productDiv = document.createElement('div');
    productDiv.className = 'p-2 bg-white rounded-md shadow';
    productDiv.innerHTML = `
    <div class="flex items-center justify-between mb-2">
      <div>
        <input type="hidden" name="product_id" readonly value="${item.id}" style="border:none;">
        <p class="text-base">
          <input type="text" name="product_name" readonly value="${item.productName}"
            class="bg-inherit" style="border:none; min-width:50px;">
        </p>
        <p class="text-xs text-slate-500">পণ্যের মূল্য:  <input type="text" name="product_price" readonly value="${item.productPrice}"> স্টকের পরিমান:  <input type="text" name="product_price" readonly value="${item.stock}"> </p>
      </div>
    </div>
    <div class="flex justify-between w-full">
      <div>
        <p class="text-xs text-slate-500">ফেরত(পিচ)</p>
        <input min="0" type="number" value="0" class="text-center border return-input w-20"
          name="product_return">
      </div>
      <div>
        <p class="text-xs text-slate-500">ড্যামেজ(পিচ)</p>
        <input min="0" type="number" value="0" class="text-center border receive-input w-20"
          name="product_damage">
      </div>
      <div>
        <p class="text-xs text-slate-500">বিক্রয় মূল্য</p>
        <input max="0" type="number" value="0"
          class="text-center bg-inherit receive-input product_selling_price w-20"
          name="product_selling_price" readonly>
      </div>
      <div>
        <p class="text-xs text-slate-500">ড্যামেজ মূল্য</p>
        <input max="0" type="number" value="0"
          class="text-center bg-inherit receive-input product_damage_price w-20"
          name="product_damage_price" readonly>
      </div>
    </div>
  `;

    // Add event listeners for input fields
    productDiv
        .querySelectorAll('.return-input, .receive-input')
        .forEach((input) => {
            input.addEventListener('input', () => updatePrices(productDiv, item));
        });

    return productDiv;
};

const calculateTotalPrices = () => {
    const productSellingPriceInputs = document.querySelectorAll(
        '.product_selling_price'
    );
    const productDamagePriceInputs = document.querySelectorAll(
        '.product_damage_price'
    );
    let totalSellingPrice = 0;
    let totalDamagePrice = 0;

    productSellingPriceInputs.forEach((input) => {
        totalSellingPrice += parseFloat(input.value) || 0;
    });

    productDamagePriceInputs.forEach((input) => {
        totalDamagePrice += parseFloat(input.value) || 0;
    });

    sellingPriceElement.value = totalSellingPrice.toFixed(2);
    damagePriceElement.value = totalDamagePrice.toFixed(2);

    totalSellingPriceElement.value = (
        totalSellingPrice - totalDamagePrice
    ).toFixed(2);

    updateFinalAmount();
};

fetch(apiURL)
    .then((response) => response.json())
    .then((data) => {
        data.forEach((item) => {
            const productDiv = createProductDiv(item);
            productsContainer.appendChild(productDiv);
        });
    })
    .catch((error) => console.error('Error fetching data:', error));

// Event listeners
discountInput.addEventListener('input', updateFinalAmount);
deposit.addEventListener('input', updateDueCash);
