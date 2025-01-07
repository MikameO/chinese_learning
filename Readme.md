# Chinese Learning Platform – Docker Installation & Usage

## Build the Docker Image
1. Clone or download this repository.
2. In the project root (where `Dockerfile` is located), build the Docker image:
   ```bash
   docker build -t chinese-learning-app .
    ```
## Run the container on port 5000:
```bash
docker run -d -p 5000:5000 --name chinese-learning-container chinese-learning-app
```

Visit http://localhost:5000 in your browser to access the app.
