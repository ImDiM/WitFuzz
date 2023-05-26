sudo docker build -t front_end .
sudo docker stop front_end
sudo docker run -d --rm -p 5173:5173 --name front_end front_end
sudo docker ps
