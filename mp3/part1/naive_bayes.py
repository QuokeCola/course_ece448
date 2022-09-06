import copy
import time

import numpy as np
import multiprocessing as mp
import matplotlib.pyplot as plt


class NaiveBayes(object):
    def __init__(self, num_class, feature_dim, num_value):
        """Initialize a naive bayes model.

        This function will initialize prior and likelihood, where 
        prior is P(class) with a dimension of (# of class,)
            that estimates the empirical frequencies of different classes in the training set.
        likelihood is P(F_i = f | class) with a dimension of 
            (# of features/pixels per image, # of possible values per pixel, # of class),
            that computes the probability of every pixel location i being value f for every class label.  

        Args:
            num_class(int): number of classes to classify
            feature_dim(int): feature dimension for each example 
            num_value(int): number of possible values for each pixel 
        """

        self.feature_likelihoods = None
        self.pred_label = None
        self.num_value = num_value
        self.num_class = num_class
        self.feature_dim = feature_dim

        self.prior = np.zeros(num_class)
        self.likelihood = np.zeros((feature_dim, num_value, num_class))
        self.occurrences = np.zeros((feature_dim, num_value, num_class))
        self.using_core = max(mp.cpu_count() - 2, 1)
        self.finished_task = 0
        print("This program will use " + str(self.using_core) + " logical processors.")

    def count_callback(self, callback_data):
        self.occurrences = self.occurrences + callback_data
        self.finished_task += 1
        process_bar(self.finished_task / self.using_core)

    def log_callback(self, callback_data):
        self.likelihood = self.likelihood + callback_data
        self.finished_task += 1
        process_bar(self.finished_task / self.using_core)

    def test_callback(self, callback_data):
        self.pred_label = self.pred_label + callback_data
        self.finished_task += 1
        process_bar(self.finished_task / self.using_core)

    def intensity_callback(self, callback_data):
        self.feature_likelihoods = self.feature_likelihoods + callback_data
        self.finished_task += 1
        process_bar(self.finished_task / 10)

    def error_callback(self, error_code):
        print(error_code)

    def train(self, train_set, train_label):

        """ Train naive bayes model (self.prior and self.likelihood) with training dataset.
            self.prior(numpy.ndarray): training set class prior (in log) with a dimension of (# of class,),
            self.likelihood(numpy.ndarray): traing set likelihood (in log) with a dimension of
                (# of features/pixels per image, # of possible values per pixel, # of class).
            You should apply Laplace smoothing to compute the likelihood.

        Args:
            train_set(numpy.ndarray): training examples with a dimension of (# of examples, feature_dim)
            train_label(numpy.ndarray): training labels with a dimension of (# of examples, )
        """
        # YOUR CODE HERE

        unique, counts = np.unique(train_label, return_counts=True)
        for i in range(len(unique)):
            self.prior[unique[i]] = np.log(counts[i] / len(train_label))
        data_slice_count = int(len(train_set) / self.using_core) + 1
        # count occurrences
        print("[Info] Start counting occurrences.")
        pool = mp.Pool(processes=self.using_core)
        self.finished_task = 0
        for i in range(self.using_core):
            sub_trainset = train_set[
                           i * data_slice_count:min(i * data_slice_count + data_slice_count, len(train_set) - 1)][:]
            sub_trainlabel = train_label[
                             i * data_slice_count:min(i * data_slice_count + data_slice_count, len(train_set) - 1)]
            processpool = pool.apply_async(process_count,
                                           args=(sub_trainset, sub_trainlabel, self.occurrences.shape,),
                                           callback=self.count_callback,
                                           error_callback=self.error_callback)
        pool.close()
        pool.join()

        print("\n[Info] Transforming into likelihood.")
        pool = mp.Pool(processes=self.using_core)
        self.finished_task = 0
        # transform data into possibilities
        data_slice_count = int(self.occurrences.shape[0] / self.using_core) + 1
        for i in range(self.using_core):
            processpool = pool.apply_async(process_log,
                                           (self.occurrences,
                                            counts,
                                            self.occurrences.shape,
                                            (i * data_slice_count, min(i * data_slice_count + data_slice_count,
                                                                       self.occurrences.shape[0]))
                                            ),
                                           callback=self.log_callback,
                                           error_callback=self.error_callback)
        pool.close()
        pool.join()

    def test(self, test_set, test_label):
        """ Test the trained naive bayes model (self.prior and self.likelihood) on testing dataset,
            by performing maximum a posteriori (MAP) classification.
            The accuracy is computed as the average of correctness
            by comparing between predicted label and true label.

        Args:
            test_set(numpy.ndarray): testing examples with a dimension of (# of examples, feature_dim)
            test_label(numpy.ndarray): testing labels with a dimension of (# of examples, )

        Returns:
            accuracy(float): average accuracy value
            pred_label(numpy.ndarray): predicted labels with a dimension of (# of examples, )
        """

        # YOUR CODE HERE

        print("\n[Info] Using trained data to recognize numbers.")
        pool = mp.Pool(processes=self.using_core)
        self.pred_label = np.zeros((len(test_set)))
        self.finished_task = 0
        data_slice_count = int(len(test_set) / self.using_core) + 1
        for i in range(self.using_core):
            processpool = pool.apply_async(process_test, (test_set,
                                                          self.likelihood,
                                                          self.prior,
                                                          (i * data_slice_count, min(i * data_slice_count + data_slice_count,
                                                                                     test_set.shape[0]))),
                                           callback=self.test_callback,
                                           error_callback=self.error_callback)
        pool.close()
        pool.join()

        accuracy = np.sum(test_label == self.pred_label) / np.size(test_label)
        print(accuracy)
        return accuracy, self.pred_label

    def save_model(self, prior, likelihood):
        """ Save the trained model parameters
        """
        np.save(prior, self.prior)
        np.save(likelihood, self.likelihood)

    def load_model(self, prior, likelihood):
        """ Load the trained model parameters
        """
        self.prior = np.load(prior)
        self.likelihood = np.load(likelihood)

    def intensity_feature_likelihoods(self, likelihood):
        """
        Get the feature likelihoods for high intensity pixels for each of the classes,
            by sum the probabilities of the top 128 intensities at each pixel location,
            sum k<-128:255 P(F_i = k | c).
            This helps generate visualization of trained likelihood images.

        Args:
            likelihood(numpy.ndarray): likelihood (in log) with a dimension of
                (# of features/pixels per image, # of possible values per pixel, # of class)
        Returns:
            feature_likelihoods(numpy.ndarray): feature likelihoods for each class with a dimension of
                (# of features/pixels per image, # of class)
        """
        # YOUR CODE HERE
        print("\n[Info] Calculating intensities.")
        self.feature_likelihoods = np.zeros((likelihood.shape[0], likelihood.shape[2]))
        self.finished_task = 0
        pool = mp.Pool(processes=self.using_core)
        for i in range(likelihood.shape[2]):
            pool.apply_async(process_feature_likelihood, (likelihood, i,), callback=self.intensity_callback, error_callback=self.error_callback)
        pool.close()
        pool.join()
        # print(self.feature_likelihoods)
        return self.feature_likelihoods


def process_count(img_subset, label_subset, shape):
    callback_data = np.zeros(shape)
    for img_idx in range(img_subset.shape[0]):
        # Iterate each image
        for i in range(shape[0]):
            # Iterate each pixel in image
            callback_data[i][int(img_subset[img_idx][i])][label_subset[img_idx]] += 1
    return callback_data


def process_log(occurrence, data_count, shape, index_range):
    callback_data = np.zeros(shape)
    for i in range(*index_range):
        for j in range(shape[1]):
            for k in range(shape[2]):
                callback_data[i][j][k] = np.log((occurrence[i][j][k] + 1) / (data_count[k] + 256))
    return callback_data


def process_test(test_set, train_set, prior, index_range):
    pred_label = np.zeros(len(test_set))
    for i in range(*index_range):
        possibilities = []
        for test_class in range(len(prior)):
            # Iterate possibilities
            possibility = prior[test_class]
            for index in range(len(test_set[i])):
                # Iterate pixels
                possibility += train_set[index][int(test_set[i][index])][test_class]
            possibilities.append(possibility)
        pred_label[i] = possibilities.index(max(possibilities))
    return pred_label


def process_feature_likelihood(likelihood, number):
    callback_data = np.zeros((likelihood.shape[0], likelihood.shape[2]))
    for i in range(likelihood.shape[0]):
        for j in range(int(likelihood.shape[1]/2), likelihood.shape[1]):
            callback_data[i][number] += likelihood[i][j][number]
    return callback_data


def process_bar(percent, start_str='[\033[1;33mProgress\033[0m]|', end_str='', total_length=15):
    bar = ''.join(['='] * int(percent * total_length)) + ''
    bar = '\r' + start_str + bar.ljust(total_length) + '| {:0>4.1f}%|'.format(percent * 100) + end_str
    print(bar, end='', flush=True)

