# FastAPI File Upload Test

This is a simple test project to demonstrate file upload functionality using
**FastAPI**. The project includes a backend API built with FastAPI and a
frontend HTML form for uploading files. The app only returns the file size but
the backend can obvoiusly perform any action on the file and return custom data.

## Features

- **FastAPI Backend**: Handles file uploads and saves them to a specified
  directory.
- **Jinja2 Frontend**: Allows uploading a file and usesd websockets to update
  the page.
- **Simple and Lightweight**: Minimal setup required to get started.
- **Max File Size**: The maximum file size is set to 100 MB. This is checked
  both on the frontend and again on the backend (browser file-size calcs are
  often not 100% accurate so files that are close to the limit will slip
  through and be caught be the backend).

## Repository

The project is hosted on GitHub:
[https://github.com/seapagan/fastapi-upload-test](https://github.com/seapagan/fastapi-upload-test)

---

## Prerequisites

Before running the project, ensure you have the following installed:

- **Python 3.9+**
- **uv** (For package and environment management). Get it from
  [here](https://astral.sh/blog/uv) if you don't already have it.

---

## Installation

1. Clone the repository:

   ```terminal
   git clone https://github.com/seapagan/fastapi-upload-test.git
   cd fastapi-upload-test
   ```

2. Create a virtual environment and install the dependencies:

   ```terminal
   uv sync
   source ./.venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

---

## Running the Project

1. Start the FastAPI server using Uvicorn:

   ```bash
   uvicorn main:app --reload
   ```

2. Open your browser and navigate to the frontend form:

   ```pre
   <http://127.0.0.1:8000>
   ```

3. Use the form to upload a file:
   - Click the **Choose File** button to select a file.
   - Click **Upload** to submit the file to the server.

---

## Project Structure

```pre
fastapi-upload-test/
├── main.py               # FastAPI application and routes
├── templates/            # HTML templates for the frontend
│   └── index.html        # Frontend with the file upload form
├── static/               # Static files (CSS, JS, etc.)
│   ├── script.js         # Custom JavaScript for the form
│   └── styles.css        # Custom styles for the form
├── pyproject.toml        # Project metadata and dependencies
├── uv.lock               # Lock file for uv package manager
├── README.md             # Project documentation
└── uploads/              # Directory where uploaded files are saved (created automatically)
```

---

## Backend Details

The backend is built using **FastAPI** and provides a single endpoint for file uploads:

- **Endpoint**: `/upload/`
- **Method**: `POST`
- **Description**: Accepts a file upload and saves it to the `uploads/` directory.

Internally, the backend will update the file size on the front end using
**websockets**, after saving the file locally on the server. In a real app you
would want to delete the file after processing it to avoid filling up the disk
or periodically clean up the directory.

We could just return the file size in the response, but this is a good example
of how to use websockets with FastAPI and how to update the frontend in real
time. In reality the actual process may be longer-running, so this way the user
can see that the upload was successful while the processing continues in the
background.

### Example Request

```bash
curl -X POST -F "file=@/path/to/your/file.txt" <http://127.0.0.1:8000/upload/>
```

---

## Frontend Details

The frontend consists of an HTML form to allow uploading a file to the backend.
The form uses **Jinja2** templating to render the HTML and **websockets** to
update the page with the file size after uploading.

---

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.

---

## License

This project is open-source and available under the [MIT License](LICENSE).

---

## Acknowledgments

- **FastAPI** for providing a modern and fast web framework.
- **Uvicorn** for serving the application.

---

Enjoy testing and experimenting with file uploads using FastAPI! 🚀
