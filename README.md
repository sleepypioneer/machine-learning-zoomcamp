# Machine Learning Bookcamp

Notes and exercises from following [alexeygrigorev](https://github.com/alexeygrigorev) [Machine Learning Zoomcamp](https://github.com/alexeygrigorev/mlbookcamp-code/tree/master/course-zoomcamp)


## notes & project links
### Week one: Intro to Machine Learning

- [notes](notes/week_one.md)
- [homework](notebooks/homework_week_1.ipynb)

### Week two: Regression

- [notes](notebooks/week_two_predicting_car_price.ipynb)
- [homework](notebooks/homework_week_2.ipynb)

### Week three: Classification (churn prediction)

- [notes](notebooks/week_three_churn_prediction.ipynb)
- [homework](notebooks/homework_week_3.ipynb)

### Week four: model evaluation

- [notes](notebooks/week_four_evaluation_metrics.ipynb)
- [homework](notebooks/homework_week_4.ipynb)

### Week five: model deployment

- [notes](notes/week_five_deployment.md)
- [homework](homework_week_five/predict.py)

### Week six: decision trees

- [notes](notes/week_six_decision_trees.md)
- [homework](notebooks/homework_week_6.ipynb)

### Week seven: decision trees



### Week eight: deep learning

- [notes](notebooks/deep_learning.ipynb)
- [homework](notebooks/homework_week_8.ipynb)


### Week nine: serverless

- [notes](notes/week_nine_serverless.md)
- [homework](notebooks/homework_week_9.ipynb)
- [homework part 2](homework_week_nine/lambda_function.py)


### Week ten: kubernetes

- [notes](notes/week_ten_kubernetes.md)
- [homework](homework_week_ten/)


## Running the local dev environment

### Running scripts locally in a virtual environment

#### Create a virtual environment

```sh
python3.9 -m venv machine-learning-zoomcamp
```

#### Activate virtual environment

```sh
machine-learning-zoomcamp\Scripts\activate
# or on linux
source machine-learning-zoomcamp/bin/activate
```

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

To download all data you can run `make get-data` or for individual sets run the following commands.  

#### Car data (for week one homework and week two notebook)

```sh
cd data && mkdir car_data && cd car_data && wget https://raw.githubusercontent.com/alexeygrigorev/mlbookcamp-code/master/chapter-02-car-price/data.csv
```

#### New York City Airbnb Open Data (for weeks two and three homework)

```sh
cd data && mkdir airbnb_data && cd airbnb_data && wget https://raw.githubusercontent.com/alexeygrigorev/datasets/master/AB_NYC_2019.csv
```

#### UCI Student Performance Data (for weeks two homework)

```sh
cd data && mkdir student_performance_data && cd student_performance_data && wget https://archive.ics.uci.edu/ml/machine-learning-databases/00320/student.zip && unzip student.zip
```

#### Customer churn data

```sh
cd data && mkdir telco_customer_churn && cd telco_customer_churn && wget https://raw.githubusercontent.com/alexeygrigorev/mlbookcamp-code/master/chapter-03-churn-prediction/WA_Fn-UseC_-Telco-Customer-Churn.csv
```

#### Credit risk data

```sh
cd data && mkdir credit_risk && cd credit_risk && wget https://raw.githubusercontent.com/alexeygrigorev/datasets/master/AB_NYC_2019.csv
```

#### Clothing dataset (subset)

```sh
cd data && git clone git@github.com:alexeygrigorev/clothing-dataset-small.git
```

## Adding new libraries

Libraries which are currently not available in the Jupyter Notebook should be added to the Dockerfile.