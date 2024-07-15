docker build -t vjn-staging .
docker rm -f vjn-staging
docker run -p 8000:8000 -d --name vjn-staging vjn-staging
docker start vjn-staging
sudo nginx -s reload