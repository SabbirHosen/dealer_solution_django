const factorInput = document.querySelector('#factor');
const cartoonInput = document.querySelector('#cartoon');
const piecesInput = document.querySelector('#pieces');
const productPriceInput = document.querySelector('#productPrice');
const pricePerpieceOutput = document.querySelector('#pricePerpiece');

const calculatePricePerPiece = () => {
	const factor = parseFloat(factorInput.value) || 0;
	const cartoon = parseFloat(cartoonInput.value) || 0;
	const pieces = parseFloat(piecesInput.value) || 0;
	const productPrice = parseFloat(productPriceInput.value) || 0;

	const pricePerPiece = productPrice / (factor * cartoon + pieces);
	pricePerpieceOutput.value = isNaN(pricePerPiece)
		? ''
		: pricePerPiece.toFixed(2);
};

factorInput.addEventListener('input', calculatePricePerPiece);
cartoonInput.addEventListener('input', calculatePricePerPiece);
piecesInput.addEventListener('input', calculatePricePerPiece);
productPriceInput.addEventListener('input', calculatePricePerPiece);

calculatePricePerPiece();
