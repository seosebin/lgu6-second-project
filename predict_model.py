from multiprocessing import Pipe
import numpy as np
import pandas as pd
import warnings
warnings.filterwarnings('ignore')

from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler, OneHotEncoder, LabelEncoder
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, classification_report, roc_auc_score, confusion_matrix

from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.svm import SVC

import joblib

with_patient = pd.read_csv("data/Disease.csv")

with_patient = with_patient.drop(columns=['Outcome Variable', 'Unnamed: 0'])

with_patient = with_patient.rename(columns={
    'Fever': '열',
    'Cough': '기침',
    'Fatigue': '피로',
    'Difficulty Breathing': '호흡곤란',
    'Blood Pressure': '혈압',
    'Cholesterol Level': '콜레스테롤'
})

with_patient = with_patient.rename(columns={
    'Asthma': '천식',
    'Stroke': '뇌졸중',
    'Osteoporosis': '골다공증',
    'Influenza': '독감',
    'Bronchitis': '기관지염',
    'Pneumonia': '폐렴',
    'Diabetes': '당뇨병',
    'Migraine': '편두통',
    'Hypertension': '고혈압',
    'Hyperthyroidism': '갑상선기능항진증'
})

numeric_features = []
categorical_features = []

for i in with_patient.columns:
    if with_patient[i].dtype == 'object':
        categorical_features.append(i)
    else:
        numeric_features.append(i)

categorical_features.remove("Disease")
features = numeric_features + categorical_features
print(features)

numeric_transformer = Pipeline(steps=[
    ('impute', SimpleImputer(strategy='median')),
    ('scaler', StandardScaler())
])

categorical_transformer = Pipeline(steps=[
    ('impute', SimpleImputer(strategy='constant', fill_value='missing')),
    ('onehot', OneHotEncoder(handle_unknown='ignore', sparse_output=False))
])

preprocessor = ColumnTransformer(
    transformers = [
        ('num', numeric_transformer, numeric_features),
        ('cat', categorical_transformer, categorical_features)
    ]
)

label_encoder = LabelEncoder()

disease_counts = with_patient['Disease'].value_counts()
except_diseases = disease_counts[disease_counts <= 2].index
train = with_patient[~with_patient['Disease'].isin(except_diseases)]

X = train[features]
y = label_encoder.fit_transform(train['Disease'])

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

models = {
    'Random Forest Classifier' : RandomForestClassifier(n_estimators=100, random_state=42),
    'Gradient Boosting Classifier' : GradientBoostingClassifier(n_estimators=100, random_state=42),
    'SVM' : SVC(kernel='rbf', probability=True, random_state=42)
}

best_score = 0
best_model_name = None
best_model = None

for name, model in models.items():
    pipeline = Pipeline([
        ('preprocessor', preprocessor),
        ('classifier', model)
    ])

    pipeline.fit(X_train, y_train)

    y_pred = pipeline.predict(X_test)
    accuracy_test = accuracy_score(y_test, y_pred)

    try:
        y_pred_proba = pipeline.predict_proba(X_test)
        auc = roc_auc_score(y_test, y_pred_proba)
        # accuracy = accuracy_score(y_test, y_pred_proba)
    except:
        # accuracy = None
        auc = None

    # print(f"Train 데이터 정확도: {accuracy_train:.4f}")
    print(f"test 데이터 정확도: {accuracy_test:.4f}")

    print(f"\nResults for {name}: ")
    print("\nClassification Report: ")
    print(classification_report(y_test, y_pred))
    if auc:
        print(f"ROC-AUC Score: {auc:.4f}")
    
    if accuracy_test > best_score:
        best_score = accuracy_test
        best_model_name = name
        best_model = model
    print('-----------------------------------------------------------------')


final_pipeline = Pipeline([
    ('preprocessor', preprocessor),
    ('classifier', best_model)
])

final_pipeline.fit(X, y)

# 저장
joblib.dump(final_pipeline, 'predict_model/best_disease_model.joblib')
joblib.dump(label_encoder, 'predict_model/label_encoder.joblib')

print(f"최종 모델 '{best_model_name}' 저장 완료 (파일: best_disease_model.joblib)")