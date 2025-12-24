# Aesthetic Image Rater - Frontend

A beautiful Next.js web application that evaluates image aesthetic quality using the LAION Aesthetic Predictor.

## Features

- 🎨 **Aesthetic Scoring**: Upload images and get aesthetic quality scores from 1-10
- 📊 **Big Score Card**: Prominent display of scores with color-coded ratings
- 📜 **History**: View your last 10 rated images
- 💾 **Download**: Save images with score overlays
- 🔗 **Share**: Share your scores via native share or clipboard
- 🌙 **Dark Mode**: Automatic dark mode support
- 📱 **Responsive**: Works on all device sizes

## Getting Started

### Prerequisites

- Node.js 18+ installed
- FastAPI backend running on `http://127.0.0.1:8000`

### Installation

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. (Optional) Create a `.env.local` file if you need to change the API URL:
```env
NEXT_PUBLIC_API_URL=http://127.0.0.1:8000
```

4. Run the development server:
```bash
npm run dev
```

5. Open [http://localhost:3000](http://localhost:3000) in your browser

## Building for Production

```bash
npm run build
npm start
```

## Usage

1. Click on the upload area or drag and drop an image
2. Wait for the aesthetic score to be calculated
3. View your score on the big score card
4. Download the image with score overlay or share your results
5. Check your rating history at the bottom of the page

## Tech Stack

- **Next.js 15** - React framework
- **TypeScript** - Type safety
- **Tailwind CSS** - Styling
- **Lucide React** - Icons

## API Integration

The app connects to the FastAPI backend at `/rate` endpoint:

```typescript
POST /rate
Content-Type: multipart/form-data

Response: { score: number }
```

## License

MIT
