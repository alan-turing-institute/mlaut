from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn import linear_model
from sklearn.naive_bayes import GaussianNB
from sklearn.naive_bayes import BernoulliNB
from sklearn.model_selection import GridSearchCV

from tensorflow.python.keras.models import Sequential
from tensorflow.python.keras.layers import Dense, Activation, Dropout
from tensorflow.python.keras.wrappers.scikit_learn import KerasRegressor, KerasClassifier
from tensorflow.python.keras import optimizers


import types
import tempfile
from tensorflow.python.keras import models as km

from .mleap_estimator import MleapEstimator

from ..shared.static_variables import GRIDSEARCH_CV_NUM_PARALLEL_JOBS
from ..shared.files_io import DiskOperations

"""
Each estimator is coitained it its own class.
Each estimator inherits from the abstract class MleapEstimator.
Each estimator must implement the following methods:
    1. get_estimator_name
    2. build
    3. save

Each estimator is built for a specific dataset. This is particularly necessary
for Neural Network classification models where the number of nodes in the last
layer depends on the number of classes.

The following methods are implemented in the MleapEstimator Abstract class and 
are inherited by all estimators:
    1. __init__
    2. set_trained_model
    3. get_trained_model

The set/get_trained_model methods are used to facilitate saving 
of the trined models. The pipeline is the following:
    1. The Experiments class evokes the set_trained_model method.
    2. The Test Orchestrator saves the trained model to disk
    3. The Experiments class evokes get_trained_model and makes predictions 
       on the test set. 
"""
#Generalized Linear Models

class Logistic_Regression(MleapEstimator):
    def __init__(self, verbose=0, n_jobs=GRIDSEARCH_CV_NUM_PARALLEL_JOBS, refit=True):
        self._verbose=verbose
        self._n_jobs=n_jobs
        self._refit=refit

    def build(self, hyperparameters=None):
        if hyperparameters is None:
            hyperparameters = {
                'C': [1e-6, 1] #[1e-6, 1e-5, 1e-4,1e-3, 1e-2, 1, 1e2,1e3,1e4,1e5,1e6]
            }
        return GridSearchCV(linear_model.LogisticRegression(), 
                            hyperparameters, 
                            verbose = self._verbose,
                            n_jobs=self._n_jobs,
                            refit=self._refit)
    
    def get_estimator_name(self):
        return 'LogisticRegression'

    def save(self, dataset_name):
        #set trained model method is implemented in the base class
        trained_model = self._trained_model
        disk_op = DiskOperations()
        disk_op.save_to_pickle(trained_model=trained_model,
                             model_name=self.get_estimator_name(),
                             dataset_name=dataset_name)

class Ridge_Regression(MleapEstimator):

    def __init__(self):
        super(Ridge_Regression, self).__init__()
    
    def get_estimator_name(self):
        return 'RidgeRegression'
    
    def build(self, hyperparameters=None):
        if hyperparameters is None:
            hyperparameters = {'alphas':[0.1, 1, 10.0],
            
            } # this is the alpha hyperparam
        
        return linear_model.RidgeCV(alphas=hyperparameters['alphas'],
                                cv=self._num_cv_folds)
    def save(self, dataset_name):
        disk_op = DiskOperations()
        disk_op.save_to_pickle(trained_model=self._trained_model,
                                model_name=self.get_estimator_name(),
                                dataset_name=dataset_name)
class Lasso(MleapEstimator):
    def __init__(self):
        super(Lasso, self).__init__()
    
    def get_estimator_name(self):
        return 'Lasso'
    def build(self, hyperparameters=None):
        if hyperparameters is None:
            hyperparameters = {'alphas':[0.1, 1, 10.0]}
        return linear_model.LassoCV(alphas=hyperparameters['alphas'],
                                    cv=self._num_cv_folds)
    def save(self, dataset_name):
        disk_op = DiskOperations()
        disk_op.save_to_pickle(trained_model=self._trained_model,
                                model_name=self.get_estimator_name(),
                                dataset_name=dataset_name)
class Lasso_Lars(MleapEstimator):
    def __init__(self):
        super(Lasso_Lars, self).__init__()
    
    def get_estimator_name(self):
        return 'LassoLars'
    def build(self, hyperparameters=None):
        if hyperparameters is None:
            hyperparameters = {'max_n_alphas':1000}
        return linear_model.LassoLarsCV(max_n_alphas=hyperparameters['max_n_alphas'],
                                    cv=self._num_cv_folds)
    def save(self, dataset_name):
        disk_op = DiskOperations()
        disk_op.save_to_pickle(trained_model=self._trained_model,
                                model_name=self.get_estimator_name(),
                                dataset_name=dataset_name)
###End of Generalized Linear Models
class Random_Forest_Classifier(MleapEstimator):

    def __init__(self):
        super(Random_Forest_Classifier, self).__init__()

    def build(self, hyperparameters=None):
        if hyperparameters is None:
            hyperparameters = {
                'n_estimators': [10, 20, 30],
                'max_features': ['auto', 'sqrt','log2', None],
                'max_depth': [5, 15, None]
            }
        return GridSearchCV(RandomForestClassifier(), 
                            hyperparameters, 
                            verbose = self._verbose,
                            n_jobs=self._n_jobs,
                            refit=self._refit)
    
    def get_estimator_name(self):
        return 'RandomForestClassifier'

    def save(self, dataset_name):
        #set trained model method is implemented in the base class
        trained_model = self._trained_model
        disk_op = DiskOperations()
        disk_op.save_to_pickle(trained_model=trained_model,
                             model_name=self.get_estimator_name(),
                             dataset_name=dataset_name)
        


class SVC_mleap(MleapEstimator):
    def __init__(self):
        super(SVC_mleap, self).__init__()

    def build(self, hyperparameters=None):
        if hyperparameters is None:
            hyperparameters = {
                            'C': [1e-6, 1], #[1e-6, 1e-5, 1e-4,1e-3, 1e-2, 1, 1e2,1e3,1e4,1e5,1e6]
                            'gamma': [1e-3, 1] #[1e-3, 1e-2, 1e-1, 1]
                        }
        return GridSearchCV(SVC(), 
                            hyperparameters, 
                            verbose = self._verbose,
                            n_jobs=self._n_jobs,
                            refit=self._refit)
    def get_estimator_name(self):
        return 'SVC'

    def save(self, dataset_name):
        #set trained model method is implemented in the base class
        trained_model = self._trained_model
        disk_op = DiskOperations()
        disk_op.save_to_pickle(trained_model=trained_model,
                             model_name=self.get_estimator_name(),
                             dataset_name=dataset_name)



class Gaussian_Naive_Bayes(MleapEstimator):
    def get_estimator_name(self):
        return 'GaussianNaiveBayes'
    def save(self, dataset_name):
        #set trained model method is implemented in the base class
        trained_model = self._trained_model
        disk_op = DiskOperations()
        disk_op.save_to_pickle(trained_model=trained_model,
                             model_name=self.get_estimator_name(),
                             dataset_name=dataset_name)
    def build(self):
        return GaussianNB()

class Bernoulli_Naive_Bayes(MleapEstimator):
    def get_estimator_name(self):
        return 'BernoulliNaiveBayes'
    def save(self, dataset_name):
        #set trained model method is implemented in the base class
        trained_model = self._trained_model
        disk_op = DiskOperations()
        disk_op.save_to_pickle(trained_model=trained_model,
                             model_name=self.get_estimator_name(),
                             dataset_name=dataset_name)
    def build(self):
        return BernoulliNB()

class Deep_NN_Classifier(MleapEstimator):
    def __init__(self):
        super(Deep_NN_Classifier, self).__init__()

    def _nn_deep_classifier_model(self, num_classes, 
                                  input_dim,
                                  loss='mean_squared_error',
                                  optimizer = 'Adam',
                                  metrics = ['accuracy'] ):
        nn_deep_model = Sequential()
        nn_deep_model.add(Dense(288, input_dim=input_dim, activation='relu'))
        nn_deep_model.add(Dense(144, activation='relu'))
        nn_deep_model.add(Dropout(0.5))
        nn_deep_model.add(Dense(12, activation='relu'))
        nn_deep_model.add(Dense(num_classes, activation='softmax'))
        
        
        if optimizer is 'Adam':
            model_optimizer  = optimizers.Adam(lr=0.001)
        
        nn_deep_model.compile(loss=loss, optimizer=model_optimizer, metrics=metrics)
        return nn_deep_model
    
    def build(self, num_classes, input_dim, num_samples, loss='mean_squared_error', hyperparameters = None):
        model = KerasClassifier(build_fn=self._nn_deep_classifier_model, 
                                num_classes=num_classes, 
                                input_dim=input_dim,
                                verbose=self._verbose,
                                loss=loss)
        if hyperparameters is None:
            hyperparameters = {'epochs': [50,100], 'batch_size': [num_samples]}
        return model
        # return GridSearchCV(model, 
        #                     hyperparameters, 
        #                     verbose = self._verbose,
        #                     n_jobs=self._n_jobs,
        #                     refit=self._refit)
    def get_estimator_name(self):
        return 'NeuralNetworkDeepClassifier'

    def save(self, dataset_name):
        #set trained model method is implemented in the base class
        trained_model = self._trained_model
        disk_op = DiskOperations()
        disk_op.save_keras_model(trained_model=trained_model,
                                 model_name=self.get_estimator_name(),
                                 dataset_name=dataset_name)


def instantiate_default_estimators(estimators, verbose=0):
    estimators_array = []
    if 'RandomForestClassifier' in estimators or 'all' in estimators:
        estimators_array.append(Random_Forest_Classifier())
    
    if 'SVC' in estimators or 'all' in estimators:
        estimators_array.append(SVC_mleap())

    if 'LogisticRegression' in estimators or 'all' in estimators:
        estimators_array.append(Logistic_Regression())
    
    if 'RidgeRegression' in estimators or 'all' in estimators:
        estimators_array.append(Ridge_Regression())
    if 'Lasso' in estimators or 'all' in estimators:
        estimators_array.append(Lasso())
    if 'LassoLars' in estimators or 'all' in estimators:
        estimators_array.append(Lasso_Lars())

    if 'GaussianNaiveBayes' in estimators or 'all' in estimators:
        estimators_array.append(Gaussian_Naive_Bayes())

    if 'BernoulliNaiveBayes' in estimators or 'all' in estimators:
        estimators_array.append(Bernoulli_Naive_Bayes())

    if 'NeuralNetworkDeepClassifier' in estimators or 'all' in estimators:
        estimators_array.append(Deep_NN_Classifier())
    return estimators_array