from mlaut.estimators.mlaut_estimator import properties
from mlaut.estimators.mlaut_estimator import mlautEstimator

from mlaut.shared.files_io import DiskOperations
from mlaut.shared.static_variables import(GENERALIZED_LINEAR_MODELS,
                                      ENSEMBLE_METHODS, 
                                      SVM,
                                      NEURAL_NETWORKS,
                                      NAIVE_BAYES,
                                      REGRESSION, 
                                      CLASSIFICATION)
from mlaut.shared.static_variables import PICKLE_EXTENTION, HDF5_EXTENTION

from sklearn.naive_bayes import GaussianNB
from sklearn.naive_bayes import BernoulliNB

@properties(estimator_family=[NAIVE_BAYES], 
            tasks=[CLASSIFICATION], 
            name='GaussianNaiveBayes')
class Gaussian_Naive_Bayes(mlautEstimator):
    """
    Wrapper for `sklearn Naive Bayes estimator <http://scikit-learn.org/stable/modules/generated/sklearn.naive_bayes.GaussianNB.html>`_.
    """
    def save(self, dataset_name):
        """
        Saves estimator on disk.

        :type dataset_name: string
        :param dataset_name: name of the dataset. Estimator will be saved under default folder structure `/data/trained_models/<dataset name>/<model name>`
        """
        #set trained model method is implemented in the base class
        trained_model = self._trained_model
        disk_op = DiskOperations()
        disk_op.save_to_pickle(trained_model=trained_model,
                             model_name=self.properties()['name'],
                             dataset_name=dataset_name)
    def build(self, **kwargs):
        """
        Builds and returns estimator class.
        
        Parameters
        ----------
        **kwargs : key-value arguments.
            Ignored in this implementation. Added for compatibility with :func:`mlaut.estimators.nn_estimators.Deep_NN_Classifier`.
        
        Returns
        -------
        `sklearn object`
            Instantiated estimator object.
        """
        return GaussianNB()

@properties(estimator_family=[NAIVE_BAYES], 
            tasks=[CLASSIFICATION], 
            name='BernoulliNaiveBayes')
class Bernoulli_Naive_Bayes(mlautEstimator):
    """
    Wrapper for `sklearn Bernoulli Naive Bayes estimator <http://scikit-learn.org/stable/modules/generated/sklearn.naive_bayes.BernoulliNB.html>`_.
    """
    

    def save(self, dataset_name):
        """
        Saves estimator on disk.

        :type dataset_name: string
        :param dataset_name: name of the dataset. Estimator will be saved under default folder structure `/data/trained_models/<dataset name>/<model name>`
        """
        #set trained model method is implemented in the base class
        trained_model = self._trained_model
        disk_op = DiskOperations()
        disk_op.save_to_pickle(trained_model=trained_model,
                             model_name=self.properties()['name'],
                             dataset_name=dataset_name)
    def build(self, **kwargs):
        """
        Builds and returns estimator class.

        Parameters
        ----------
        **kwargs : key-value arguments.
            Ignored in this implementation. Added for compatibility with :func:`mlaut.estimators.nn_estimators.Deep_NN_Classifier`.
        
        Returns
        -------
        `sklearn object`
            Instantiated estimator object.
        """
        return BernoulliNB()