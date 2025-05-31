(Get-ECRLoginCommand).Password | docker login --username AWS --password-stdin 928383298076.dkr.ecr.eu-central-1.amazonaws.com
docker compose -f ./docker-compose.yaml build
docker compose -f ./docker-compose.yaml push