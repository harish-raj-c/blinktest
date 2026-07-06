# Eye Blink Test Application

A full-stack application for measuring eye blink patterns during reading to assess eye comfort and provide personalized recommendations.

## Architecture

- **Backend**: Python FastAPI server with NATS messaging for real-time eye tracking data
- **Frontend**: Svelte application with Vite for a modern, responsive UI

## Features

- **Instructions Page**: Clear guidance for test preparation
- **Reading Test Page**: Real-time blink monitoring while reading a paragraph
- **Results Page**: Comprehensive analysis with eye comfort score and recommendations
- **Real-time Updates**: WebSocket connection for live status updates
- **Calibration System**: Automatic face detection and distance calibration

## Setup Instructions

### Prerequisites

- Python 3.8+
- Node.js 16+
- NATS server running at `nats://192.168.0.187:4222`
- Eye tracking system publishing to NATS topics:
  - `vision.eye.cam0.face`
  - `vision.eye.cam0.depth`
  - `vision.eye.cam0.blink`

### Backend Setup

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Start the FastAPI server:
```bash
python server.py
```

The server will start on `http://localhost:8001`

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies (if not already installed):
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```

The frontend will be available at `http://localhost:5173` (or another port if 5173 is in use)

### Building for Production

To create a production build of the frontend:
```bash
cd frontend
npm run build
```

The built files will be in the `frontend/dist` directory.

## Usage

1. Start the backend server (`python server.py`)
2. Start the frontend development server (`cd frontend && npm run dev`)
3. Open the frontend URL in your browser
4. Follow the instructions on the screen
5. Position yourself in front of the camera
6. Wait for calibration to complete
7. Read the provided paragraph naturally
8. View your results and recommendations

## API Endpoints

- `GET /api/status` - Get current calibration and test status
- `POST /api/start` - Start the blink test
- `POST /api/stop` - Stop the test and get results
- `POST /api/reset` - Reset the test state
- `WS /ws` - WebSocket endpoint for real-time updates

## Configuration

Edit `config.py` to adjust:
- `TEST_DURATION`: Duration of the test in seconds
- `MIN_DEPTH`: Minimum distance for calibration (mm)
- `MAX_DEPTH`: Maximum distance for calibration (mm)

Edit `server.py` to change:
- `NATS_URL`: NATS server connection string
- Server host and port

## Project Structure

```
blinktest/
├── server.py              # FastAPI backend server
├── blink_test.py          # Blink test logic
├── config.py              # Configuration settings
├── main.py                # Original NATS listener (legacy)
├── nats_listener.py       # NATS utilities
├── requirements.txt       # Python dependencies
├── frontend/              # Svelte frontend
│   ├── src/
│   │   ├── App.svelte     # Main application component
│   │   ├── app.css        # Global styles
│   │   ├── main.js        # Entry point
│   │   └── pages/         # Page components
│   │       ├── Instructions.svelte
│   │       ├── ReadingTest.svelte
│   │       └── Results.svelte
│   ├── package.json       # Node dependencies
│   └── vite.config.js     # Vite configuration
└── README.md              # This file
```

## Troubleshooting

- **WebSocket connection fails**: Ensure the backend server is running on port 8001
- **Calibration stuck**: Check that NATS is receiving data from the eye tracking system
- **Frontend not updating**: Verify WebSocket connection is established in browser console
- **Port already in use**: The frontend will automatically try the next available port

## License

MIT
