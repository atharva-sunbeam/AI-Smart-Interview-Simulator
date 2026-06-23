from ml_models.role_prediction.train_role_classifier import (
RoleClassifier,
)

def test_classifier_creation():


    classifier = RoleClassifier()

    assert classifier is not None
    

def test_predict_role_method_exists():
    
    classifier = RoleClassifier()

    assert hasattr(
        classifier,
        "predict_role",
    )

