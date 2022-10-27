# TGBotReffBook
***

Configure for Docker build
=====================
1. Create secret token from **token.txt** file (create it and write your bot token) 
2. Instruction for secrets and swarm **https://cloud.croc.ru/blog/about-technologies/docker-secrets/**.
3. Build image by **Dockerfile**.
4. Run service **docker stack deploy --compose-file .\docker-compose.yaml poly-service**