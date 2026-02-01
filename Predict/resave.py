import joblib
import xgboost as xgb

# Load the model (this might trigger the warning once)
model = joblib.load('Predictors/FinalPred.pkl')

# Resave the model with the current version of joblib/xgboost
joblib.dump(model, 'Predictors/FinalPred.pkl')
print("Model resaved successfully with current XGBoost version.")