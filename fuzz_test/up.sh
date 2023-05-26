sudo docker build -t fuzz_test .
sudo docker stop fuzz_test
sudo docker run -d --rm --name fuzz_test --link mysql --link mongo --link redis fuzz_test
sudo docker ps
