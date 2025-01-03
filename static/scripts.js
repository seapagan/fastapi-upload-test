// Maximum file size (100 MB)
const MAX_FILE_SIZE = 100 * 1024 * 1024; // 100 MB in bytes

// Function to format file size with locale settings
function formatFileSize(bytes, locale = "en-GB") {
  const formatter = new Intl.NumberFormat(locale);
  return formatter.format(bytes);
}

// Connect to WebSocket
const clientId = Math.random().toString(36).substring(7); // Generate a random client ID
const ws = new WebSocket(`ws://localhost:8000/ws/${clientId}`);

ws.onmessage = function (event) {
  console.log("WebSocket message received:", event.data); // Debugging: Log the message
  try {
    const data = JSON.parse(event.data);
    if (data.file_size) {
      // Get the original filename from the file input
      const fileInput = document.querySelector('input[type="file"]');
      const originalFileName = fileInput.files[0].name;

      // Format the file size with locale settings
      const formattedFileSize = formatFileSize(data.file_size);

      // Update the HTML with the original file name and formatted size
      document.getElementById(
        "fileName"
      ).textContent = `File Name: ${originalFileName}`;
      document.getElementById(
        "fileSize"
      ).textContent = `File Size: ${formattedFileSize} bytes`;
    }
  } catch (error) {
    console.error("Error parsing WebSocket message:", error);
  }
};

// Handle form submission
document.getElementById("uploadForm").onsubmit = async function (event) {
  event.preventDefault();
  const formData = new FormData(event.target);

  // Clear any previous error messages
  document.getElementById("error").textContent = "";

  // Get the selected file
  const fileInput = document.querySelector('input[type="file"]');
  const file = fileInput.files[0];

  // Check file size on the frontend
  if (file.size > MAX_FILE_SIZE) {
    document.getElementById("error").textContent =
      "Error: File size exceeds the 100 MB limit.";
    return; // Stop the upload
  }

  // Upload file using fetch
  try {
    const response = await fetch("/upload/", {
      method: "POST",
      body: formData,
    });

    if (!response.ok) {
      // Handle HTTP errors (e.g., 413, 500)
      const error = await response.json();
      throw new Error(error.detail || "An unknown error occurred.");
    }

    const result = await response.json();
    console.log("Upload successful:", result.message);

    // Clear the file input field
    document.getElementById("uploadForm").reset();
  } catch (error) {
    // Display the error message in the frontend
    console.error("Upload failed:", error.message);
    document.getElementById("error").textContent = `Error: ${error.message}`;
  }
};
