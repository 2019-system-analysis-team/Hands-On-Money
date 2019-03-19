docker rm -f flask-container
docker build -t flask-image:latest .
docker run -d -p 5000:5000 --name flask-container flask-image
