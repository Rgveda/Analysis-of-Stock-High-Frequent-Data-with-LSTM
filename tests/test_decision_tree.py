from sklearn import tree
from model.config import *
import pandas as pd
from model.utils import *
import matplotlib.pyplot as plt
from model.evaluator import *

conf = LM_Config()

# step 1: Get dataset (csv)
data = pd.read_csv(conf['data_file_path'], encoding='gbk')

# step 2: Select Feature
data = extract_feature_and_label(data, conf['feature_name'], conf['label_name'])

# step 3: Preprocess
train, test = divide_train_and_test(data, conf['training_set_proportion'])
train_x, train_y = data_transform_for_xgboost(train)
test_x, test_y = data_transform_for_xgboost(test)

clf = tree.DecisionTreeRegressor(max_depth=3)

clf = clf.fit(train_x, train_y)
clf.fit(train_x, train_y)

train_pred = clf.predict(train_x)
test_pred = clf.predict(test_x)

show_feature_importance(clf, conf['feature_name'])

plot_scatter(y_true=test_y, y_pred=test_pred)

evaluator = Evaluator()
print('evaluate trend (with delay)')
train_acc = evaluator.evaluate_trend_with_delay(y_true=train_y, y_pred=train_pred)
print('train=', train_acc)
test_acc = evaluator.evaluate_trend_with_delay(y_true=test_y, y_pred=test_pred)
print('test=', test_acc)

print('simple evaluation')
train_acc = evaluator.evaluate_trend_simple(y_true=train_y, y_pred=train_pred)
print('train=', train_acc)
test_acc = evaluator.evaluate_trend_simple(y_true=test_y, y_pred=test_pred)
print('test=', test_acc)
