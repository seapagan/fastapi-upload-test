// Connect to WebSocket
const clientId = Math.random().toString(36).substring(7); // Generate a random client ID
const ws = new WebSocket(`ws://localhost:8000/ws/${clientId}`);

ws.onmessage = function (event) {
  console.log("WebSocket message received:", event.data); // Debugging: Log the message
  try {
    const data = JSON.parse(event.data);
    if (data.file_name && data.file_size) {
      // Update the HTML with the file name and size
      document.getElementById(
        "fileName"
      ).textContent = `File Name: ${data.file_name}`;
      document.getElementById(
        "fileSize"
      ).textContent = `File Size: ${data.file_size} bytes`;
    }
  } catch (error) {
    console.error("Error parsing WebSocket message:", error);
  }
};

// Handle form submission
document.getElementById("uploadForm").onsubmit = async function (event) {
  event.preventDefault();
  const formData = new FormData(event.target);

  // Upload file using fetch
  const response = await fetch("/upload/", {
    method: "POST",
    body: formData,
  });

  if (response.ok) {
    const result = await response.json();
    console.log("Upload successful:", result.message);

    // Clear the file input field
    document.getElementById("uploadForm").reset();
  } else {
    const error = await response.json();
    console.error("Upload failed:", error);
  }
};
