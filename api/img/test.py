import scipy
from sklearn.decomposition import PCA
from svm import *
from svmutil import *

v, vf = svm_read_problem("./data/valenceT.scale")
#a, af = svm_read_problem("arousal.txt", return_scipy=True)

# scale_param_v = csr_find_scale_param(vf, lower=0)
# print(csr_find_scale_param)
# scaled_vf = csr_scale(vf, scale_param_v)
# print(scaled_vf)

#pca
# pca = PCA(n_components=5)
# pca.fit(scaled_vf)

# print(pca.explained_variance_)

# valence_model = svm_train(v, vf, '-s 3 -t 2')
#scale_param_a = csr_find_scale_param(af, lower=0, upper=1)
#scaled_af = csr_scale(af, scale_param_a)

valence_model = svm_load_model("./data/valence.model")
#arousal_model = svm_load_model("arousal.model")

p_label_v, p_acc_v, p_val_v = svm_predict(v, vf, valence_model)
#p_label_a, p_acc_a, p_val_a = svm_predict(a, scaled_af, arousal_model, '-b 1')

ACC, MSE, SCC = evaluations(v, p_label_v)
print("pre:", p_label_v)
