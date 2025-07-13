# OpenRedact Frontend

This is the React-based frontend for the OpenRedact project.

## Features
- Upload PDF files for redaction
- Download and preview redacted PDFs
- Simple, modern UI

## Development

### Install dependencies
```
npm install
```

### Run development server
```
npm run dev
```

The app will be available at [http://localhost:5173](http://localhost:5173).

### Connect to Backend
- The frontend is configured to proxy API requests to the backend at `http://localhost:5000` via Vite config.
- Make sure the FastAPI backend is running on port 5000.

### Build for production
```
npm run build
```

---

For more details, see the main project README.
