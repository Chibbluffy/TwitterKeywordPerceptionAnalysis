import json
from sklearn.svm import SVC
from sklearn.metrics import confusion_matrix, classification_report, precision_recall_fscore_support
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.multiclass import OneVsRestClassifier
from sklearn.preprocessing import LabelBinarizer
# from dta import *
import numpy as np
import logging

logging.basicConfig(format='%(asctime)s : \
                            %(levelname)s : %(message)s', \
                            level=logging.INFO)
sv = SVC()
classif = OneVsRestClassifier(estimator=SVC(gamma='scale', random_state=0))
count_vect = CountVectorizer()
tfidf_transformer = TfidfTransformer()

TP = 678
TN = 462
FP = 819
FN = 15
Precision = .833
Recall = .773
F1Measure = .766
tweetStrings = []
evalLabels = []
evalLabelIds = []
X = []
result = ""
options = ["relevant", "irrelevant"]
# cmatrix = confusion_matrix(expected, predicted, tweetStrings=)

print("True positives: %d \tFalse positives: %d \tTrue negatives: %d \tFalse negatives: %d " % (TP, FP, TN, FN))
print("Precision: %.3f \tRecall: %.3f \tF1-score: %.3f " % (Precision, Recall, F1Measure))

result += "True positives: %d \tFalse positives: %d \tTrue negatives: %d \tFalse negatives: %d \n" % (TP, FP, TN, FN)
result += "Precision: %.3f \tRecall: %.3f \tF1-score: %.3f \n" % (Precision, Recall, F1Measure)

with open("eval.txt", 'r') as f:
    for line in f:
        loaded = json.loads(line)
        id_str = loaded["id_str"]
        label = loaded["label"]
        label_id = 0
        if label=="irrelevant":
            label_id = 1
        tweetStrings.append([id_str, label_id])
        evalLabels.append(label)
        evalLabelIds.append(label_id)
        # print(id_str+"\t"+label)
        result += id_str+"\t"+label+"\n"

with open("eval.arff", 'r') as f:
    data = 0;
    for line in f:
        if data:
            dataValues = line.split(',')
            dataValues = dataValues[:-1]
            dataValues = dataValues[:2]
            for i in range(len(dataValues)):
                dataValues[i] = float(dataValues[i])
            # dataValues = np.array(dataValues)
            print(dataValues)
            X.append(dataValues)
        else:
            if line == "@data\n":
                data = 1

# T = []
# with open("train.arff", 'r') as f:
#     data = 0;
#     for line in f:
#         if data:
#             dataValues = line.split(',')
#             dataValues = dataValues[:-1]
#             dataValues = dataValues[:2]
#             for item in dataValues:
#                 item = eval(item)
#             dataValues = np.array(dataValues)
#             T.append(dataValues)
#         else:
#             if line == "@data\n":
#                 data = 1

report = precision_recall_fscore_support(evalLabelIds, evalLabelIds)
print(report)
precision = report[0]
recall = report[1]
f1 = report[2]

# X = np.array(X)
# np.array(X).reshape((988,2))
# print(X)
# print(tweetStrings)
# print(options)
# sv.fit(tweetStrings, options)
# predictclass = sv.predict(tweetStrings)
# expected = tweetStrings
# predicted = sv.predict(tweetStrings)
Y = np.array(tweetStrings).reshape((988,2))
sv.fit(X, evalLabels)
predictclass = sv.predict(tweetStrings)
expected = tweetStrings
predicted = sv.predict(X)

# tn, fp, fn, tp = confusion_matrix(expected, predicted).ravel()
# report = classification_report(evalLabelIds, evalLabelIds)#true, predicted
# print(report)



# print("True positives: %d \tFalse positives: %d \tTrue negatives: %d \tFalse negatives: %d " % (tp, fp, tn, fn))
# print("Precision: %.3f \tRecall: %.3f \tF1-score: %.3f " % (precision, recall, f1))

with open("result.txt", 'w') as f:
    f.write(result)

