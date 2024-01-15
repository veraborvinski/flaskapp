docker stop flaskapp
docker rm flaskapp
docker build -t flaskapp .
docker tag flaskapp acobley/flaskapp
docker run -p 80:5000 -d --name flaskapp acobley/flaskapp
