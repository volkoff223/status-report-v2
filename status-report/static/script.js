const dropArea = document.getElementById("drop-area");
const fileInput = document.getElementById("file-input");
const dialog = document.getElementById("dialog");
const dialogMessage = document.getElementById("dialog-message");
const closeButton = document.getElementById("close-btn");
const providerDiv = document.getElementById("provider");
const staffDiv = document.getElementById("staff");
const immDiv = document.getElementById("imm");

dropArea.addEventListener("click", () => fileInput.click());
fileInput.addEventListener("change", handleFile);

// "Close" button closes the dialog
closeButton.addEventListener("click", () => {
  dialog.close();
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
        }
      })
      .catch((error) => console.error("Error:", error));
  });
}
