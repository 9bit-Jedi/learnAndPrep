sudo docker build -t vjn-prod .
sudo docker rm -f vjn-prod
sudo docker run -p 8000:8000 -d --name vjn-prod vjn-prod
sudo docker start vjn-prod
sudo nginx -s reload