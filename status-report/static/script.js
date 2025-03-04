const dropArea = document.getElementById("drop-area");
const fileInput = document.getElementById("file-input");
const dialog = document.getElementById("dialog");
const dialogMessage = document.getElementById("dialog-message");
const closeButton = document.getElementById("close-btn");
const providerDiv = document.getElementById("provider");
const staffDiv = document.getElementById("staff");
const immDiv = document.getElementById("imm");
const bgDiv = document.getElementById("bg");
const balanceDiv = document.getElementById("balance");
const imageDropdown = document.getElementById("image-dropdown");
const selectedImage = document.getElementById("selected-image");
const imageUploadInput = document.getElementById("image-upload");
const imageUploadBtn = document.getElementById("image-upload-btn");

dropArea.addEventListener("click", () => fileInput.click());
fileInput.addEventListener("change", handleFile);

// "Close" button closes the dialog
closeButton.addEventListener("click", () => {
  dialog.close();
});

// Fetch and populate image dropdown
function populateImageDropdown() {
  imageDropdown.innerHTML = '<option value="">Choose an image</option>'; // Reset dropdown

  fetch("/list-images")
    .then((response) => response.json())
    .then((images) => {
      images.forEach((image) => {
        const option = document.createElement("option");
        option.value = image;
        option.textContent = image;
        imageDropdown.appendChild(option);
      });
    })
    .catch((error) => console.error("Error fetching images:", error));
}

populateImageDropdown();

// Handle image dropdown selection
imageDropdown.addEventListener("change", (event) => {
  const selectedImageName = event.target.value;
  if (selectedImageName) {
    selectedImage.src = `/static/img/${selectedImageName}`;
    selectedImage.style.display = "block";
  } else {
    selectedImage.style.display = "none";
  }
});

// Image Upload Button Click Handler
imageUploadBtn.addEventListener("click", () => {
  imageUploadInput.click();
});

// Image Upload Input Change Handler
imageUploadInput.addEventListener("change", (event) => {
  const file = event.target.files[0];
  if (file) {
    const formData = new FormData();
    formData.append("image", file);

    fetch("/upload-image", {
      method: "POST",
      body: formData,
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.error) {
          dialogMessage.innerText = data.error;
          dialog.showModal();
        } else {
          // Refresh dropdown and select the newly uploaded image
          populateImageDropdown();

          // Select the new image in dropdown
          const newImageOption = Array.from(imageDropdown.options).find(
            (option) => option.value === data.filename
          );
          if (newImageOption) {
            imageDropdown.value = data.filename;
            selectedImage.src = `/static/img/${data.filename}`;
            selectedImage.style.display = "block";
          }
        }
      })
      .catch((error) => {
        console.error("Error uploading image:", error);
        dialogMessage.innerText = "Error uploading image";
        dialog.showModal();
      });
  }
});

function handleFile() {
  const files = fileInput.files;
  if (!files) return;

  // Process each file
  Array.from(files).forEach((file, index) => {
    const formData = new FormData();
    formData.append("file", file);

    fetch("/upload", { method: "POST", body: formData })
      .then((response) => response.json())
      .then((data) => {
        // Check for unsupported file
        if (data.error) {
          dialogMessage.innerText = data.error;
          dialog.showModal();
        }
        if (data.providerData) {
          providerDiv.innerHTML = `<h3>Provider:</h3><div>${data.providerData}</div>`;
        } else if (data.staffData) {
          staffDiv.innerHTML = `<h3>Staff:</h3><div>${data.staffData}</div>`;
        } else if (data.immData) {
          immDiv.innerHTML = `<h3>Immunization Alerts:</h3><div>${data.immData}</div>`;
        } else if (data.bgdata) {
          bgDiv.innerHTML = `<h3>Background Checks:</h3><div>${data.bgdata}</div>`;
        } else if (data.balanceData) {
          balanceDiv.innerHTML = `<h3>Outstanding Balances:</h3><div>${data.balanceData}</div>`;
        }
      })
      .catch((error) => console.error("Error:", error));
  });
}
