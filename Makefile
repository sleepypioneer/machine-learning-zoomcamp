IMG_NAME := machine-learning-zoomcamp
DOCKER_BUILD_CONTEXT="."

.PHONY: build
build:
	docker build \
	-f $(DOCKER_BUILD_CONTEXT)/Dockerfile \
	-t $(IMG_NAME) .

.PHONY: dev
dev: build
	docker run -it --rm --network host \
		-v "$(shell pwd)/data:/work/data" \
		-v "$(shell pwd)/notebooks:/work" -w /work \
		$(IMG_NAME) \
		jupyter notebook \
			--notebook-dir=/work \
			--ip='0.0.0.0' --port=8888 \
			--no-browser --allow-root \
			--NotebookApp.token='' --NotebookApp.password=''