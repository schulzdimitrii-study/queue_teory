document.addEventListener("DOMContentLoaded", () => {
    const modelSelect = document.getElementById("modelSelect");
    const commonFields = document.getElementById("commonFields");
    const serversField = document.getElementById("serversField");
    const capacityField = document.getElementById("capacityField");

    modelSelect.addEventListener("change", () => {
        const selected = modelSelect.value;

        if (selected) {
            commonFields.style.display = "block";
            capacityField.style.display = "block";
        } else {
            commonFields.style.display = "none";
            capacityField.style.display = "none";
        }

        if (selected === "MMSK") {
            serversField.style.display = "block";
        } else {
            serversField.style.display = "none";
        }
    });
});