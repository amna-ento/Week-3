from sklearn.datasets import load_iris
from sklearn.tree import DecisionTreeClassifier
import joblib


iris = load_iris()



X = iris.data
y = iris.target


model = DecisionTreeClassifier(random_state=42)

# Train the model
model.fit(X, y)


joblib.dump(model, "model.joblib")

print("Model trained and saved successfully!")


print("\nClass Mapping:")
for index, flower in enumerate(iris.target_names):
    print(f"{index} -> {flower}")
    
    
    
    
    


    