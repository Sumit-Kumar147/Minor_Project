document.addEventListener("DOMContentLoaded", function () {
    const uploadForm = document.getElementById("uploadForm");
    const imageUpload = document.getElementById("imageUpload");
    const previewImage = document.getElementById("previewImage");
    const loading = document.getElementById("loading");
    const resultText = document.getElementById("resultText");
    const locationForm = document.getElementById("locationForm");
    const latitudeInput = document.getElementById("latitude");
    const longitudeInput = document.getElementById("longitude");
    const getLocationBtn = document.getElementById("getLocationBtn");

    // Show image preview
    imageUpload.addEventListener("change", function () {
        const file = this.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = function (e) {
                previewImage.src = e.target.result;
                previewImage.style.display = "block";
            };
            reader.readAsDataURL(file);
        }
    });

    // Handle form submission
    uploadForm.addEventListener("submit", function (event) {
        event.preventDefault();

        if (!imageUpload.files[0]) {
            alert("⚠️ Please select an image first!");
            return;
        }

        if (!latitudeInput.value || !longitudeInput.value) {
            alert("⚠️ Please enter valid latitude and longitude!");
            return;
        }

        // Show loading animation
        loading.style.display = "block";
        resultText.innerText = "🔍 Analyzing...";
        resultText.style.color = "yellow";

        // Fake delay (Simulating backend request)
        setTimeout(() => {
            loading.style.display = "none";
            const randomResult = Math.random() > 0.5 ? "🛑 Garbage Detected" : "✅ Clean Road";
            resultText.innerHTML = `<strong>${randomResult}</strong>`;
            resultText.style.color = randomResult.includes("Garbage") ? "red" : "limegreen";
        }, 2000);
    });

    // Get the user's current location and fill in the latitude and longitude fields
    getLocationBtn.addEventListener("click", function () {
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(function (position) {
                latitudeInput.value = position.coords.latitude;
                longitudeInput.value = position.coords.longitude;
            }, function (error) {
                alert("Unable to retrieve your location. Please enter the coordinates manually.");
            });
        } else {
            alert("Geolocation is not supported by your browser.");
        }
    });
});
