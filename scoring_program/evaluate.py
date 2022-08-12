
import os
from pprint import pprint
import sys
import pandas as pd
import numpy as np
import math
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# def check_valid_file(gt_df, pred_df):
#     gt_columns = list(gt_df.columns)
#     pred_columns = list(pred_df.columns)
#     for pred_col in pred_columns:
#         if pred_col not in gt_columns:
#             print("{} is a wrong column name in the result file. Columns name must be {}, where the indexes _1, _2, etc. represent the order of the location needed to be predicted".format(pred_col, gt_columns))
#             exit()
#     for gt_col in gt_columns:
#         if gt_col not in pred_columns:
#             print("Missing the column {} in the result file. Columns name must be {}, where the indexes _1, _2, etc. represent the order of the location needed to be predicted".format(gt_col, gt_columns))
#             exit()


def eval_mae(y_true, y_pred):
    return mean_absolute_error(y_true.flatten(), y_pred.flatten())


def eval_mape(y_true, y_pred):
    return np.mean(np.abs((y_true.flatten() - y_pred.flatten()) / y_true.flatten())) * 100


def eval_rmse(y_true, y_pred):
    return math.sqrt(mean_squared_error(y_true.flatten(), y_pred.flatten()))


def eval_mdape(y_true, y_pred):
    return np.median(np.abs((y_true.flatten() - y_pred.flatten()) / y_true.flatten())) * 100


def eval_r2(y_true, y_pred):
    return r2_score(y_true.flatten(), y_pred.flatten())


def count_files(folder):
    list = os.listdir(folder)
    count = len(list)
    # count = 0
    # for path in os.scandir(folder):
    #     if path.is_file():
    #         count += 1
    return count


def count_folders(truth_dir):
    # return len(os.walk(truth_dir).next()[1])
    return len(next(os.walk(truth_dir))[1])


if __name__ == "__main__":
    [_, input_dir, output_dir] = sys.argv
    submission_dir = os.path.join(input_dir, 'res')
    truth_dir = os.path.join(input_dir, 'ref')

    num_files = count_files(os.path.join(truth_dir, "1"))
    num_folders = count_folders(truth_dir)
    horizon = 24

    gt_np = np.zeros((num_folders, num_files, horizon))
    pred_np = np.zeros((num_folders, num_files, horizon))

    for folder_th in range(1, num_folders+1):
        res_folder = os.path.join(submission_dir, str(folder_th))
        ref_folder = os.path.join(truth_dir, str(folder_th))
        num_files_res = count_files(res_folder)
        num_files_ref = count_files(ref_folder)
        if num_files_ref > num_files_res:
            print("Missing {} files in the folder res/{}".format(num_files_ref -
                  num_files_res, folder_th))
            exit()
        elif num_files_ref < num_files_res:
            print("Exceeding {} files in the folder res/{}".format(num_files_res -
                  num_files_ref, folder_th))
            exit()
        else:
            for file_th in range(1, num_files+1):
                gt_df = pd.read_csv(os.path.join(ref_folder, "gt_{}_{}.csv".format(
                    folder_th, file_th)), usecols=["PM2.5"])
                pred_df = pd.read_csv(os.path.join(
                    res_folder, "res_{}_{}.csv".format(folder_th, file_th)), usecols=["PM2.5"])
                if len(pred_df) < len(gt_df):
                    print("Missing {} values in the file res_{}_{}.csv".format(
                        len(gt_df)-len(pred_df), folder_th, file_th))
                    exit()
                if len(pred_df) > len(gt_df):
                    print("Exceeding {} values in the file res_{}_{}.csv".format(
                        len(pred_df)-len(gt_df), folder_th, file_th))
                    exit()
                else:
                    gt_np[folder_th-1, file_th-1, :] = gt_df.values.flatten()
                    pred_np[folder_th-1, file_th-1,
                            :] = pred_df.values.flatten()

    res_dict = {}
    res_dict['mae'] = eval_mae(gt_np, pred_np)
    res_dict['mape'] = eval_mape(gt_np, pred_np)
    res_dict['rmse'] = eval_rmse(gt_np, pred_np)
    res_dict['mdape'] = eval_mdape(gt_np, pred_np)
    # res_dict['r2'] = eval_r2(gt_np, pred_np)
    with open(os.path.join(output_dir, 'scores.txt'), 'w') as output_file:
        output_file.write("mdape: {:f}\n".format(round(res_dict['mdape'], 4)))
        output_file.write("mape: {:f}\n".format(round(res_dict['mape'], 4)))
        output_file.write("mae: {:f}\n".format(round(res_dict['mae'], 4)))
        output_file.write("rmse: {:f}\n".format(round(res_dict['rmse'], 4)))
        # output_file.write("r2: {:f}\n".format(round(res_dict['r2'], 4)))
