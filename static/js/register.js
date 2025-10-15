document.getElementById("banquetForm").addEventListener("submit", function (event) {
    event.preventDefault(); // Prevent default form submission

    // Get form values
    const banquetName = document.getElementById("banquetName").value.trim();
    const ownerName = document.getElementById("ownerName").value.trim();
    const email = document.getElementById("email").value.trim();
    const phone = document.getElementById("phone").value.trim();
    const capacity = document.getElementById("capacity").value.trim();
    const location = document.getElementById("location").value.trim();
    const googleLink = document.getElementById("googleLink").value.trim();
    const services = document.getElementById("services").value;
    const images = document.getElementById("images").files;

    // Simple Google Maps link validation
    if (!googleLink.startsWith("https://maps.google.com") && !googleLink.startsWith("https://www.google.com/maps")) {
        showToast("⚠️ Please enter a valid Google Maps link!", "warning");
        return;
    }

    // Optional: log data
    console.log({
        banquetName, ownerName, email, phone, capacity, location, googleLink, services, images
    });

    // Show success toast
    showToast(`🎉 Banquet "${banquetName}" registered successfully!`, "success");

    // Reset form
    this.reset();
});

// Function to show a floating toast notification
function showToast(message, type) {
    const toast = document.createElement("div");
    toast.className = `toast ${type}`;
    toast.innerHTML = message;
    document.body.appendChild(toast);

    // Animate in
    setTimeout(() => {
        toast.classList.add("show");
    }, 100);

    // Animate out after 3 seconds
    setTimeout(() => {
        toast.classList.remove("show");
        setTimeout(() => toast.remove(), 500);
    }, 3000);
}
const fileInput = document.getElementById('id_image');
const isMobile = /iPhone|iPad|iPod|Android/i.test(navigator.userAgent);

if(isMobile) {
    fileInput.setAttribute('title', 'Tap to select images (multiple selection supported)');
} else {
    fileInput.setAttribute('title', 'Hold Ctrl / Shift to select multiple images');
}
