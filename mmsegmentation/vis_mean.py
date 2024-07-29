import matplotlib
import random
import os
import pandas as pd
import matplotlib.pyplot as plt

matplotlib.rc("font", family='SimHei')

log_path = 'path/to/log'
output_folder = 'path/to/save'

os.makedirs(output_folder, exist_ok=True)

with open(log_path, "r") as f:
    json_list = f.readlines()

len(json_list)
eval(json_list[4])
df_train = pd.DataFrame()
df_test = pd.DataFrame()
for each in json_list[:-1]:
    if 'aAcc' in each:
        df_test = df_test.append(eval(each), ignore_index=True)
    else:
        df_train = df_train.append(eval(each), ignore_index=True)

train_csv_path = os.path.join(output_folder, 'train set log.csv')
test_csv_path = os.path.join(output_folder, 'test set log.csv')

df_train.to_csv(train_csv_path, index=False)
df_test.to_csv(test_csv_path, index=False)

random.seed(124)
colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'tab:blue', 'tab:orange', 'tab:green', 'tab:red', 'tab:purple', 'tab:brown', 'tab:pink', 'tab:gray', 'tab:olive', 'tab:cyan', 'black', 'indianred', 'brown', 'firebrick', 'maroon', 'darkred', 'red', 'sienna', 'chocolate', 'yellow', 'olivedrab', 'yellowgreen', 'darkolivegreen', 'forestgreen', 'limegreen', 'darkgreen', 'green', 'lime', 'seagreen', 'mediumseagreen', 'darkslategray', 'darkslategrey', 'teal', 'darkcyan', 'dodgerblue', 'navy', 'darkblue', 'mediumblue', 'blue', 'slateblue', 'darkslateblue', 'mediumslateblue', 'mediumpurple', 'rebeccapurple', 'blueviolet', 'indigo', 'darkorchid', 'darkviolet', 'mediumorchid', 'purple', 'darkmagenta', 'fuchsia', 'magenta', 'orchid', 'mediumvioletred', 'deeppink', 'hotpink']
markers = [".",",","o","v","^","<",">","1","2","3","4","8","s","p","P","*","h","H","+","x","X","D","d","|","_",0,1,2,3,4,5,6,7,8,9,10,11]
linestyle = ['--', '-.', '-']

def get_line_arg():
    line_arg = {}
    line_arg['color'] = random.choice(colors)
    line_arg['linestyle'] = random.choice(linestyle)
    line_arg['linewidth'] = random.randint(1, 4)
    return line_arg

metrics = ['loss', 'decode.loss_ce', 'aux.loss_ce']

plt.figure(figsize=(16, 8))

x = df_train['step']
for y in metrics:
    try:
        plt.plot(x, df_train[y], label=y, **get_line_arg())
    except:
        pass

plt.tick_params(labelsize=20)
plt.xlabel('step', fontsize=20)
plt.ylabel('Loss', fontsize=20)
plt.title('loss of train set', fontsize=25)

plt.legend(fontsize=20)

train_loss_png_path = os.path.join(output_folder, 'loss of train set.png')
plt.savefig(train_loss_png_path, dpi=120, bbox_inches='tight', format='png')

metrics = ['decode.acc_seg', 'aux.acc_seg']

plt.figure(figsize=(16, 8))

x = df_train['step']
for y in metrics:
    try:
        plt.plot(x, df_train[y], label=y, **get_line_arg())
    except:
        pass

plt.tick_params(labelsize=20)
plt.xlabel('step', fontsize=20)
plt.ylabel('Metrics', fontsize=20)
plt.title('train set acc', fontsize=25)

plt.legend(fontsize=20)

train_acc_png_path = os.path.join(output_folder, 'train set acc.png')
plt.savefig(train_acc_png_path, dpi=120, bbox_inches='tight', format='png')

df_test.columns

metrics = ['aAcc', 'mIoU', 'mAcc', 'mDice', 'mFscore', 'mPrecision', 'mRecall']

plt.figure(figsize=(16, 8))

x = df_test['step']
for y in metrics:
    try:
        plt.plot(x, df_test[y], label=y, **get_line_arg())
    except:
        pass

plt.tick_params(labelsize=20)
plt.ylim([0, 100])
plt.xlabel('step', fontsize=20)
plt.ylabel('Metrics', fontsize=20)
plt.title('test set title', fontsize=25)

plt.legend(fontsize=20)

test_metrics_png_path = os.path.join(output_folder, 'test set title.png')
plt.savefig(test_metrics_png_path, dpi=120, bbox_inches='tight', format='png')
