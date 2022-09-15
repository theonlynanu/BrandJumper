# Generates a base layer to bring dependencies into Lambda

# Remove our layer container and image if they already exist
docker rm layer-container
docker rmi base-layer

# Builds our base layer image
docker build -t base-layer .

# Runs image in container
docker run --name layer-container base-layer

#Extracts the .zip file that contains our dependencies for use by CDK
docker cp layer-container:layer.zip . && echo "layer.zip created with updated layer image and container."