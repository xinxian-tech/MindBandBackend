from scipy import *
from .svm import *
from .svmutil import *
import os


UPLOAD_FOLDER = r'D:\train1\for_testing'
allowed_extensions = set(['png', 'jpg', 'jpeg', 'pgm'])


def img2VA():
	os.chdir(r'D:\\train1\\for_testing')
	os.system("train.exe 1.jpg")
	print("!!!!!!!!!!")
	os.chdir(r'C:\Users\Administrator\Desktop\MindBandBackend\api\img')
	os.system("svm-scale -l 0 -u 1 -r ./data/v_scale D:\\train1\\for_testing\\valence.txt>./data/valence_scale")
	os.system("svm-scale -l 0 -u 1 -r ./data/a_scale D:\\train1\\for_testing\\arousal.txt>./data/arousal_scale")
	v, vf = svm_read_problem("./data/valence_scale")
	a, af = svm_read_problem("./data/arousal_scale")

	valence_model = svm_load_model("./data/valence.model")
	arousal_model = svm_load_model("./data/arousal.model")

	p_label_v, p_acc_v, p_val_v = svm_predict(v, vf, valence_model)
	p_label_a, p_acc_a, p_val_a = svm_predict(a, af, arousal_model)

	return p_label_v[0], p_label_a[0]


def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1] in allowed_extensions