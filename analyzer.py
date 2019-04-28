import sys
import pandas as pd
import json

df_list = []
with open(sys.argv[1], 'r') as f:
    for line in f:
        loaded = json.loads(line)
        label = loaded["label"]
        text = loaded["text"]
        df_list.append({'text': text, 'label': label})
df = pd.DataFrame(df_list)

from sklearn.feature_extraction.text import CountVectorizer
vectorizer = CountVectorizer(min_df=0, lowercase=False)
vectorizer.fit([x['text'] for x in df_list])

from sklearn.model_selection import train_test_split
sentences = [x['text'] for x in df_list]
labels = [y['label'] for y in df_list]

sentences_train, sentences_test, \
label_train, label_test = train_test_split(sentences, labels, 
                                           test_size=.10, random_state=1000)
vectorizer = CountVectorizer()
vectorizer.fit(sentences_train)

X_train = vectorizer.transform(sentences_train)
X_test = vectorizer.transform(sentences_test)

from sklearn.linear_model import LogisticRegression
classifier = LogisticRegression(solver='lbfgs', multi_class='auto')
classifier.fit(X_train, label_train)
score = classifier.score(X_test, label_test)
# print("Accuracy: ", score)


from sklearn.metrics import precision_score, classification_report, confusion_matrix, recall_score, f1_score
from sklearn.svm import SVC
svclassifier = SVC(kernel='linear', C=1000, gamma='auto')
svclassifier.fit(X_train, label_train)
label_pred = svclassifier.predict(X_test)

# print("True positives: %s" % confusion_matrix(label_test, label_pred)[0,0])
# print("False positives: %s" % confusion_matrix(label_test, label_pred)[0,1])
# print("True negatives: %s" % confusion_matrix(label_test, label_pred)[1,0])
# print("False negatives: %s" % confusion_matrix(label_test, label_pred)[1,1])
print
print("Precision: %s" % precision_score(label_pred, label_test, average='macro'))
print("Recall: %s" % recall_score(label_pred, label_test, average='macro'))
print("F1_score: %s" % f1_score(label_pred, label_test, average='macro'))
print


