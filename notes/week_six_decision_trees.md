# Week six Decision Trees and Ensemble Learning

We will build a credit risk model to determine if a bank should lend a customer money and what risk there is that the customer will default on their loan.

## Data cleaning and Preparation

- handling missing values
- handling categorical data

## Decision Trees

Go through binary conditions (if else rules) to make a prediction.

```python
 if client['records'] == 'yes':
    if client['job'] == 'parttime':
        return 'default'
    else:
        return 'ok'
else:
    if client['assets'] > 6000:
        return 'ok'
    else:
        return 'default'
```

### Algorithm basics

- find best split
- stop if max_depth is reached
- if Left is sufficiently large and not pure -> repeat for Left
- if Right is sufficiently large and not pure -> repeat for Right

### Finding best split Algorithm

#### For each feature

- Sort dataset
- Find all possible thresholds
- Select all unique thresholds (except last one as we always want to have at least one record when we split)
- Split on each threshold
- Calculate impurity right and left for each split
- See which has the lowest average (from all thresholds and features)

Calculate miscalssification Rate (impurity)

SPLIT: Assets > T


##### ASSETS feature
|   T      | Decision left | Impurity Left | Decision Right | Impurity Right | Avg     |
|----------|---------------|---------------|----------------|----------------|---------|
|   0      | DEFAULT       |  0%           |  OK            |  93%           | 21%     |
| 2000     | DEFAULT       |  0%           |  OK            |  33%           | 16%     |
| **3000** | **DEFAULT**   |  **0%**       |  **OK**        |  **20%**       | **10%** |
| 4000     | DEFAULT       |  25%          |  OK            |  25%           | 25%     |
| 5000     | DEFAULT       |  50%          |  OK            |  50%           | 50%     |
| 8000     | DEFAULT       |  43%          |  OK            |  0%            | 21%     |

The threshold 3000 is the best as it has the lowest average impurity.

##### DEBT feature
|   T      | Decision left | Impurity Left | Decision Right | Impurity Right | Avg     |
|----------|---------------|---------------|----------------|----------------|---------|
|  500     | OK            |  0%           | DEFAULT        |  43%           | 21%     |
| 1000     | OK            |  33%          | DEFAULT        |  0%            | 16%     |
| 2000     | OK            |  43%          | DEFAULT        |  0%            | 21%     |

The assets 3000 threshold is still the best one for the split.


### Implementing Decision Trees in Python with SciKit Learn

```python
from sklearn.tree import DecisionTreeClassifier
from sklearn.feature_extraction import DictVectorizer
from sklearn.metrics import roc_auc_score
from sklearn.tree import export_text

train_dicts = df_train.fillna(0).to_dict(orient='records')
dv = DictVectorizer(sparse=False)
X_train = dv.fit_transform(train_dicts)


dt = DecisionTreeClassifier()
dt.fit(X_train, y_train)

val_dicts = df_val.fillna(0).to_dict(orient='records')
X_val = dv.transform(val_dicts)

y_pred = dt.predict_proba(X_val)[:, 1]
roc_auc_score(y_val, y_pred)
# output 0.65


y_pred = dt.predict_proba(X_train)[:, 1]
roc_auc_score(y_train, y_pred)
# output 1.0

```

Control depth to avoid overfitting

```python
dt = DecisionTreeClassifier(max_depth=2)
dt.fit(X_train, y_train)

y_pred = dt.predict_proba(X_train)[:, 1]
auc = roc_auc_score(y_train, y_pred)
print('train:', auc)
# output train: 0.7054989859726213

y_pred = dt.predict_proba(X_val)[:, 1]
auc = roc_auc_score(y_val, y_pred)
print('val:', auc)
# output val: 0.6685264343319367
```

```python
print(export_text(dt, feature_names=dv.get_feature_names()))
# output:
# |--- records=no <= 0.50
# |   |--- seniority <= 6.50
# |   |   |--- class: 1
# |   |--- seniority >  6.50
# |   |   |--- class: 0
# |--- records=no >  0.50
# |   |--- job=partime <= 0.50
# |   |   |--- class: 0
# |   |--- job=partime >  0.50
# |   |   |--- class: 1
```

### Tuning Parameters

Most important for us is selecting values for `max_depth` and `min_samples_leaf`.

- use different values to train the model
- comput auc for each
- remember if we don't limit the max depth our model will over fit
- pick the one with the best auc score. If we only have this parameter pick the smallest one with best depth
- if we have another parameter to tune we should take a small range of best values to see it in combination with the values for the other parameter.

```python
depths = [1, 2, 3, 4, 5, 6, 10, 15, 20, None]

for depth in depths: 
    dt = DecisionTreeClassifier(max_depth=depth)
    dt.fit(X_train, y_train)
    
    y_pred = dt.predict_proba(X_val)[:, 1]
    auc = roc_auc_score(y_val, y_pred)
    
    print('%4s -> %.3f' % (depth, auc))
```

```python
scores = []

for depth in [4, 5, 6]:
    for s in [1, 5, 10, 15, 20, 500, 100, 200]:
        dt = DecisionTreeClassifier(max_depth=depth, min_samples_leaf=s)
        dt.fit(X_train, y_train)

        y_pred = dt.predict_proba(X_val)[:, 1]
        auc = roc_auc_score(y_val, y_pred)
        
        scores.append((depth, s, auc))
```

We put these scores into a dataframe so the data can be read easier.

```python
columns = ['max_depth', 'min_samples_leaf', 'auc']
df_scores = pd.DataFrame(scores, columns=columns)

df_scores_pivot = df_scores.pivot(index='min_samples_leaf', columns=['max_depth'], values=['auc'])
df_scores_pivot.round(3)
```

Visualising with a heat map can make this even easier to understand

```python
sns.heatmap(df_scores_pivot, annot=True, fmt=".3f")
```

## Ensembles and Random Forest

### Random forest

Train 5 models and take average of returned predictions. Each decision tree model gets a different set of features.

`n_estimators` : number of models
`max_features` : max number of features given to a model
`bootstrap` : offers another way of randomisation
`n_jobs` : allows us to train in parallel (default is none) `-1` will use all available processors


*Each model gets a random set of features, we can use `random_state` to fix this, so our results are reproduceable.*

## Gradient Boosting

Combine multiple ensembles into one.


Data -> train model 1 -> predictions 1 ->
Errors ->  train model 2 -> predictions 2 ->
Errors ->  train model 3 -> predictions 3 ->
Errors ->  train model 4 -> predictions 4

Combine all predictions to give final productions.
Each new model tries to correct the previous models errors. (so it happens sequencially not in parallel like trees)


### Parameter tuning

`eta`, `max_depth` and `min_child_weight` are important features to configure but also useful are `subsample`, `colsample_bytree`


## Conclusion

XgBoost often gives better performance, however it has more variables which require tuning in comparision with decision tree models which only have two variables (`max_depth` and`min_samples_leaf`) that require tuning. However decision trees easily overfit (performs well on training model and less well on test data)