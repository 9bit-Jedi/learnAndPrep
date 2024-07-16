sudo docker build -t vjn-staging .
sudo docker rm -f vjn-staging
sudo docker run -p 8000:8000 -d --name vjn-staging vjn-staging
sudo docker start vjn-staging
sudo nginx -s reload