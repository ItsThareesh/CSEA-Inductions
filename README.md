# Aesthetics Image Rater

A full-stack web application that evaluates the aesthetic quality of images using the LAION Aesthetic Predictor built on top of CLIP.

Users can upload images, receive an aesthetic score, view suggestions, generate attention (saliency) map, and download annotated results.

## Features

### Image Rating

- Upload any image < 3MB
- Get an aesthetic score from 1 to 10
- View suggestions to improve image aesthetics

### Download Results

- Generate gradient-based saliency maps to visualize which regions influenced the score
- Download images with score overlay

### History

- View the last 10 rated images with scores
- Uses thumbnails to reduce storage usage
- Stored in browser localStorage

## Getting Started

1. Clone the repository:
```bash
git clone https://github.com/ItsThareesh/CSEA-Inductions.git
cd CSEA-Inductions
```

2. Run with Docker Compose:
```bash
docker-compose up --build
```

3. Open [http://localhost:3000](http://localhost:3000) in your browser

## Project Structure

```
.
├── backend
├── frontend
├── docker-compose.yml
└── README.md
```

## Architecture

The application consists of a FastAPI backend and a Next.js frontend. 

### Frontend

- User interface for uploading images, displaying scores, and managing history.
- Built with Next.js and shadcn/ui components.
- Client-side rendering only (current capability because of simple UI & lack of auth feature)


### Backend

- FastAPI server that handles image uploads, scoring, and saliency map generation.
- OpenAI's CLIP + Torch + LAION Aesthetic Predictor for image evaluation.
- Image heuristics via OpenCV
- Endpoints
    - `POST /rate`: Rate an image and return score & suggestion
    - `POST /download`: Generate image with score overlay
    - `POST /saliency-map`: Generate and return saliency map for a rated image

## Model Details

- CLIP ViT-B/16 backbone
- LAION Aesthetic Predictor head trained on LAION-Aesthetics v2 dataset

## License

This project is licensed under the MIT License.
