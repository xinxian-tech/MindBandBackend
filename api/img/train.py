from scipy import *
from svm import *
from svmutil import *
import os

input_img = '1.jpg'

os.system("D:\\train1\\for_testing\\train.exe " + input_img)

os.system("svm-scale -l 0 -u 1 -r ../windows/v_scale D:\\train1\\for_testing\\valence.txt>./data/valence_scale")
os.system("svm-scale -l 0 -u 1 -r ../windows/a_scale D:\\train1\\for_testing\\arousal.txt>./data/arousal_scale")
v, vf = svm_read_problem("./data/valence_scale")
a, af = svm_read_problem("./data/arousal_scale")

valence_model = svm_load_model("./data/valence.model")
arousal_model = svm_load_model("./data/arousal.model")

p_label_v, p_acc_v, p_val_v = svm_predict(v, vf, valence_model)
p_label_a, p_acc_a, p_val_a = svm_predict(a, af, arousal_model)

ACC, MSE, SCC = evaluations(v, p_label_v)
ACC, MSE, SCC = evaluations(a, p_label_a)
print("pre_val_v:", p_label_v)
print("pre_val_a:", p_label_a)
