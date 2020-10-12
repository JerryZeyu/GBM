"""
GBM models
"""
import matplotlib.pyplot as plt
import lightgbm as lgb
import pandas as pd
import numpy as np
import time
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn import metrics
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import cross_val_score


# Load data sets
data_dir = "./data/"
model_dir = "./data/"

train_df = pd.read_csv(data_dir+"train.csv")
test_df = pd.read_csv(data_dir+"test.csv")
train_label_df = pd.read_csv(data_dir+"train_answers.csv")
print("Successfully load datasets.")


# Pre-process
train_data = train_df.values
train_features = train_data[:, 4:]
train_labels = train_label_df.values[:, 1]
train_labels = np.repeat(train_labels, 4)
feature_names = list(train_df.columns)[4:]
print("Num features: ", len(feature_names))
train_info = train_data[:, :4]

# Scaling
scaler = MinMaxScaler().fit(train_features)
train_features_trans = scaler.transform(train_features)

# Split train/val sets
train_x, test_x, train_y, test_y = train_test_split(train_features, train_labels, random_state=0)
print("Split train/val:\nNum train set: %s, Num val set: %s" % (len(train_y), len(test_y)))
train_dataset = lgb.Dataset(train_x, label=train_y, feature_name=feature_names)
test_dataset = lgb.Dataset(test_x, label=test_y, reference=train_dataset, feature_name=feature_names)

best_score=0
for a in [31, 64, 96, 127 ]:
    for b in [0.1, 0.05, 0.005]:
        model=lgb.LGBMClassifier(boosting_type='gbdt', num_leaves=a, max_depth=-1, learning_rate=b, n_estimators=1000,
                         subsample_for_bin=200000, objective=None, min_split_gain=0.0, min_child_weight=0.001,
                         min_child_samples=20, subsample=1.0, subsample_freq=1, colsample_bytree=1.0, reg_alpha=0.0,
                         reg_lambda=0.0, random_state=None, n_jobs=-1, silent=False)
        scores=cross_val_score(model,train_x,train_y,cv=5)
        score=np.mean(scores)
        if score > best_score:
            best_score = score
            best_parameter_num_leaves=a
            best_parameter_learning_rate=b


select_model=lgb.LGBMClassifier(boosting_type='gbdt', num_leaves=best_parameter_num_leaves, max_depth=-1, learning_rate=best_parameter_learning_rate,
                                n_estimators=1000,subsample_for_bin=200000, objective=None, min_split_gain=0.0,
                                min_child_weight=0.001,min_child_samples=20, subsample=1.0, subsample_freq=1, colsample_bytree=1.0,
                                reg_alpha=0.0, reg_lambda=0.0, random_state=None, n_jobs=-1, silent=False)
select_model_fitted=select_model.fit(train_x, train_y, sample_weight=None, init_score=None, eval_set=None, eval_names=None,
                        eval_sample_weight=None, eval_init_score=None, eval_metric='logloss',early_stopping_rounds=None,
                        verbose=True, feature_name='auto', categorical_feature='auto', callbacks=None)
result_score=select_model_fitted.score(test_x)

result_predicted=select_model_fitted.predict(test_x)

print('Test set score with best parameters is: ', result_score)
print('Prediction results are ', result_predicted)
















