import matplotlib.pyplot as plt
import mlflow
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    ConfusionMatrixDisplay,
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline

from src.preprocessing import clean_text

INPUT_FILE = "data/annotated_emails.csv"
mlflow.set_tracking_uri("http://127.0.0.1:5000")
mlflow.set_experiment("gmail-email-classifier")


def main():
    # Load labelled dataset
    df = pd.read_csv(INPUT_FILE)

    # Combine subject and body
    df["text"] = df["subject"].fillna("") + " " + df["body"].fillna("")

    # Clean the text
    df["text"] = df["text"].apply(clean_text)

    X = df["text"]
    y = df["label"]

    # Stratified split keeps the class proportions approximately
    # the same in training and test sets.
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.20,
        random_state=42,
        stratify=y,
    )

    print(f"Training samples: {len(X_train)}")
    print(f"Test samples: {len(X_test)}")

    experiments = [
        {
            "name": "logistic_regression_baseline",
            "class_weight": None,
        },
        {
            "name": "logistic_regression_balanced",
            "class_weight": "balanced",
        },
    ]

    for experiment in experiments:
        # Fit ONLY on training data
        with mlflow.start_run(run_name=experiment["name"]):
            # TF-IDF + Logistic Regression
            model = Pipeline(
                [
                    (
                        "tfidf",
                        TfidfVectorizer(
                            ngram_range=(1, 2),
                            min_df=2,
                            max_df=0.95,
                        ),
                    ),
                    (
                        "classifier",
                        LogisticRegression(
                            max_iter=1000,
                            class_weight=experiment["class_weight"],
                        ),
                    ),
                ]
            )

            model.fit(X_train, y_train)

            y_pred = model.predict(X_test)

            accuracy = accuracy_score(y_test, y_pred)

            macro_f1 = f1_score(
                y_test,
                y_pred,
                average="macro",
            )

            weighted_f1 = f1_score(
                y_test,
                y_pred,
                average="weighted",
            )

            mlflow.log_param(
                "model",
                "LogisticRegression",
            )

            mlflow.log_param(
                "class_weight",
                experiment["class_weight"],
            )

            mlflow.log_param("ngram_range", "(1, 2)")
            mlflow.log_param("min_df", 2)
            mlflow.log_param("max_df", 0.95)
            mlflow.log_param("test_size", 0.20)
            mlflow.log_param("random_state", 42)

            mlflow.log_metric("accuracy", accuracy)
            mlflow.log_metric("macro_f1", macro_f1)
            mlflow.log_metric("weighted_f1", weighted_f1)
            mlflow.sklearn.log_model(model, name="model")

            print("\n" + "=" * 60)
            print(experiment["name"])
            print("=" * 60)

            print(f"Accuracy: {accuracy:.2f}")
            print(f"Macro F1: {macro_f1:.2f}")
            print(f"Weighted F1: {weighted_f1:.2f}")

            print("\nClassification report:")
            print(
                classification_report(
                    y_test,
                    y_pred,
                    zero_division=0,
                )
            )


if __name__ == "__main__":
    main()
