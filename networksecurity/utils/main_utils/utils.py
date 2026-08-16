import yaml
from networksecurity.logging.logger import logging
from networksecurity.exception.exception import CustomException
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import f1_score
import os, sys
import numpy as np
import pickle


def read_yaml_file(file_path: str) -> dict:
    try:
        with open(file_path, "rb") as yaml_file:
            return yaml.safe_load(yaml_file)
    except Exception as e:
        raise CustomException(e)


def write_yaml_file(file_path: str, content: object, replace: bool = False) -> None:
    try:
        if replace and os.path.exists(file_path):
            os.remove(file_path)

        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        with open(file_path, "w") as file:
            yaml.dump(content, file)

    except Exception as e:
        raise CustomException(e)


def save_numpy_array_data(file_path: str, array: np.ndarray):
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path, "wb") as file:
            np.save(file, array)
    except Exception as e:
        raise CustomException(e)


def load_numpy_array_data(file_path: str) -> np.ndarray:
    try:
        with open(file_path, "rb") as file:
            return np.load(file)
    except Exception as e:
        raise CustomException(e)


def save_object(file_path: str, obj: object):
    try:
        logging.info("Enterd the save object method of main_utils class")
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "wb") as file:
            pickle.dump(obj, file)
        logging.info("Exited the save object method of main_utils class")
    except Exception as e:
        raise CustomException(e)


def load_object(
    file_path: str,
) -> object:
    try:
        if not os.path.exists(file_path):
            raise Exception(f"The file: {file_path} is not exists")
        with open(file_path, "rb") as file_obj:
            print(file_obj)
            return pickle.load(file_obj)
    except Exception as e:
        raise CustomException(e) from e


def evaluate_models(
    X_train, y_train, X_test, y_test, models, param
) -> dict[str, float]:
    try:
        report: dict[str, float] = {}

        for model_name, model in models.items():

            para = param[model_name]

            gs = GridSearchCV(
                estimator=model, param_grid=para, cv=3, scoring="f1", n_jobs=-1
            )

            gs.fit(X_train, y_train)

            # Get the best fitted model
            best_model = gs.best_estimator_

            # Update the dictionary
            models[model_name] = best_model

            # Predictions
            y_train_pred = best_model.predict(X_train)
            y_test_pred = best_model.predict(X_test)

            # F1 scores
            train_model_score = float(f1_score(y_train, y_train_pred))

            test_model_score = float(f1_score(y_test, y_test_pred))

            report[model_name] = test_model_score

            logging.info(
                f"{model_name} - "
                f"Train F1: {train_model_score:.4f}, "
                f"Test F1: {test_model_score:.4f}"
            )

        return report

    except Exception as e:
        raise CustomException(e)
