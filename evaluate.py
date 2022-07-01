
import os
import sys
import pandas as pd
import numpy as np
import math
from sklearn.metrics import mean_absolute_error, mean_squared_error

def check_valid_file(gt_df, pred_df):
    gt_columns = list(gt_df.columns)
    pred_columns = list(pred_df.columns)
    for pred_col in pred_columns:
        if pred_col not in gt_columns:
            print("{} is a wrong column name in the result file. Columns name must be {}, where the indexes _1, _2, etc. represent the order of the location needed to be predicted".format(pred_col, gt_columns))
            exit()
    for gt_col in gt_columns:
        if gt_col not in pred_columns:
            print("Missing the column {} in the result file. Columns name must be {}, where the indexes _1, _2, etc. represent the order of the location needed to be predicted".format(gt_col, gt_columns))
            exit()

def eval_mae(y_true, y_pred):
    return mean_absolute_error(y_true.flatten(), y_pred.flatten())

def eval_mape(y_true, y_pred): 
    return np.mean(np.abs((y_true.flatten() - y_pred.flatten()) / y_true.flatten())) * 100

def eval_rmse(y_true, y_pred):
    return math.sqrt(mean_squared_error(y_true.flatten(), y_pred.flatten()))

if __name__ == "__main__":
    [_, input_dir, output_dir] = sys.argv
    submission_dir = os.path.join(input_dir, 'res')
    truth_dir = os.path.join(input_dir, 'ref')
    gt_df = pd.read_csv(os.path.join(truth_dir, "gt.csv"))
    pred_df = pd.read_csv(os.path.join(submission_dir, "result.csv"))
    res_dict = {}
    check_valid_file(gt_df, pred_df)
    gt_np = gt_df.to_numpy()
    pred_np = pred_df.to_numpy()
    res_dict['mae'] = eval_mae(gt_np, pred_np)
    res_dict['mape'] = eval_mape(gt_np, pred_np)
    res_dict['rmse'] = eval_rmse(gt_np, pred_np)
    with open(os.path.join(output_dir, 'scores.txt'), 'w') as output_file:
        output_file.write("MAE: {:f}\n".format(round(res_dict['mae'], 4)))
        output_file.write("MAPE: {:f}\n".format(round(res_dict['mape'], 4)))
        output_file.write("RMSE: {:f}\n".format(round(res_dict['rmse'], 4)))