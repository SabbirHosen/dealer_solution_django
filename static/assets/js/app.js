const toastContainer = document.getElementById("toastContainer");

window.addEventListener("online", function () {
	toastContainer.style.display = "none";
	document.body.style.pointerEvents = "auto";
});
window.addEventListener("offline", function () {
	toastContainer.style.display = "block";
	document.body.style.pointerEvents = "none";
});
