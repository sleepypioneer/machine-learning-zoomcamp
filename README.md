# Machine Learning Bookcamp

Notes and exercises from following [alexeygrigorev](https://github.com/alexeygrigorev) [Machine Learning Zoomcamp](https://github.com/alexeygrigorev/mlbookcamp-code/tree/master/course-zoomcamp)


## notes & project links
### Week one: Intro to Machine Learning

- [notes](notes/week_one.md)
- [homework](notebooks/homework_week_1.ipynb)

### Week two: Regression

- [notes](notebooks/week_two_predicting_car_price.ipynb)
- [homework]()

## Running the local dev environment
### Start a Jupyter server for notebooks 📓

To spin up a Docker container with Jupyter Notebook libraries installed, run:

```sh
make dev
```

### Download data

The first time collecting data run the following to create the data directory:

```sh
mkdir data
```

#### Car data (for week one homework and week two notebook)

```sh
cd data && mkdir car_data && cd car_data && wget https://raw.githubusercontent.com/alexeygrigorev/mlbookcamp-code/master/chapter-02-car-price/data.csv
```

#### New York City Airbnb Open Data (for weeks two homework)
```sh
cd data && mkdir airbnb_data && cd airbnb_data && wget https://raw.githubusercontent.com/alexeygrigorev/datasets/master/AB_NYC_2019.csv
```

#### UCI Student Performance Data (for weeks two homework)
```sh
cd data && mkdir student_performance_data && cd student_performance_data && wget https://archive.ics.uci.edu/ml/machine-learning-databases/00320/student.zip && unzip student.zip
```

## Adding new libraries

Libraries which are currently not available in the Jupyter Notebook should be added to the Dockerfile.