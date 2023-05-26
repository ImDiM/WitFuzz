sudo docker build -t back_end .
sudo docker stop back_end
sudo docker run -d --rm -p 5000:5000 --name back_end --link mysql --link mongo --link redis back_end
sudo docker ps
