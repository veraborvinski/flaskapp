docker stop flaskapp
docker rm flaskapp
docker build -t flaskapp .
docker tag flaskapp https://github.com/veraborvinski/flaskapp
docker run -p 80:5000 -d --name flaskapp https://github.com/veraborvinski/flaskapp
