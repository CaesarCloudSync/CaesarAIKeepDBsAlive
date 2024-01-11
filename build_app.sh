git add .
git commit -m "$1"
git push origin -u master:main
docker build -t palondomus/caesaraikeepdbsalive:latest .
docker push palondomus/caesaraikeepdbsalive:latest
docker run -it -p 8080:8080 palondomus/caesaraikeepdbsalive:latest