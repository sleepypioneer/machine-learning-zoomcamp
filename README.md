# Machine Learning Bookcamp

Notes and exercises from following [alexeygrigorev](https://github.com/alexeygrigorev) [Machine Learning Zoomcamp](https://github.com/alexeygrigorev/mlbookcamp-code/tree/master/course-zoomcamp)


## Start a Jupyter server for notebooks 📓

To spin up a Docker container with Jupyter Notebook libraries installed, run:

```sh
make dev
```

## Download data

The first time collecting data run the following to create the data directory:

```sh
mkdir data
```

### Week one

```sh
cd data && mkdir week_one && cd week_one && wget https://raw.githubusercontent.com/alexeygrigorev/mlbookcamp-code/master/chapter-02-car-price/data.csv
```

## Adding new libraries

Libraries which are currently not available in the Jupyter Notebook should be added to the Dockerfile.