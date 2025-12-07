# Deployment Guide

This guide covers different options for deploying the LA Crime Data Visualization Dashboard.

## Option 1: Local Development

The simplest way to run the dashboard is locally:

```bash
python src/app.py
```

Then access at `http://localhost:8050`

## Option 2: Streamlit Cloud (Alternative)

If you prefer Streamlit over Dash, you can convert the app to Streamlit and deploy to Streamlit Cloud:

1. Convert `app.py` to use Streamlit instead of Dash
2. Push to GitHub
3. Connect repository to [Streamlit Cloud](https://streamlit.io/cloud)
4. Deploy automatically

## Option 3: Heroku

1. Create a `Procfile`:
```
web: gunicorn src.app:server
```

2. Create `runtime.txt`:
```
python-3.11.0
```

3. Install gunicorn:
```bash
pip install gunicorn
```

4. Deploy to Heroku:
```bash
heroku create your-app-name
git push heroku main
```

## Option 4: Railway

1. Create `railway.json`:
```json
{
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "gunicorn src.app:server --bind 0.0.0.0:$PORT"
  }
}
```

2. Connect GitHub repository to Railway
3. Deploy automatically

## Option 5: GitHub Pages (Static Export)

For GitHub Pages, you need to export the dashboard as static HTML. However, this will lose interactivity. A better approach is to:

1. Use Plotly's static export feature
2. Export individual visualizations as HTML
3. Create a static HTML page that links to these

**Note**: Full interactivity requires a running server, so GitHub Pages is not ideal for Dash apps.

## Option 6: Docker

Create a `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8050

CMD ["python", "src/app.py"]
```

Build and run:
```bash
docker build -t crime-dashboard .
docker run -p 8050:8050 crime-dashboard
```

## Recommended: Railway or Heroku

For a fully interactive dashboard with cross-filtering, Railway or Heroku are recommended as they support Python web applications.

## Environment Variables

If needed, you can set environment variables for:
- `DASH_DEBUG`: Set to `False` for production
- `PORT`: Server port (usually set by hosting platform)

## Data Files

Make sure processed data files are included in deployment or generated on first run. You may want to:
- Include `data/processed/` in repository (if files are small)
- Or run preprocessing script as part of deployment
- Or use a data storage service (S3, etc.)

