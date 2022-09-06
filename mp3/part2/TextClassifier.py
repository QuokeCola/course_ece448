# TextClassifier.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
#
# Created by Dhruv Agarwal (dhruva2@illinois.edu) on 02/21/2019

"""
You should only modify code within this file -- the unrevised staff files will be used for all other
files and classes when code is run, so be careful to not modify anything else.
"""
import numpy as np


class TextClassifier(object):
    def __init__(self):
        """Implementation of Naive Bayes for multiclass classification

        :param lambda_mixture - (Extra Credit) This param controls the proportion of contribution of Bigram
        and Unigram model in the mixture model. Hard Code the value you find to be most suitable for your model
        """
        self.lambda_mixture = 0.0
        self.likelihood = []
        self.class_probability = []
        self.class_word_count = []
        self.occurrence = []
        self.unique_words = []

    def fit(self, train_set, train_label):
        """
        :param train_set - List of list of words corresponding with each text
            example: suppose I had two emails 'i like pie' and 'i like cake' in my training set
            Then train_set := [['i','like','pie'], ['i','like','cake']]

        :param train_label - List of labels corresponding with train_set
            example: Suppose I had two texts, first one was class 0 and second one was class 1.
            Then train_labels := [0,1]
        """
        for i in range(14):
            self.occurrence.append({})
            self.likelihood.append({})
            self.class_word_count.append(0)
        for i in range(len(train_set)):
            self.class_word_count[train_label[i] - 1] += len(train_set[i])
            for word in train_set[i]:
                if not self.occurrence[train_label[i] - 1].__contains__(word):
                    self.occurrence[train_label[i]-1][word] = 0
                self.occurrence[train_label[i]-1][word] += 1
        for i in range(14):
            for key in self.occurrence[i]:
                # self.likelihood[i][key] = np.log(self.occurrence[i][key]/self.class_word_count[i])
                if not key in self.unique_words:
                    self.unique_words.append(key)
            self.class_probability.append(np.log(self.class_word_count[i]/sum(self.class_word_count)))


    def predict(self, dev_set, dev_label, lambda_mix=0.0):
        """
        :param dev_set: List of list of words corresponding with each text in dev set that we are testing on
              It follows the same format as train_set
        :param dev_label : List of class labels corresponding to each text
        :param lambda_mix : Will be supplied the value you hard code for self.lambda_mixture if you attempt extra credit

        :return:
                accuracy(float): average accuracy value for dev dataset
                result (list) : predicted class for each text
        """

        accuracy = 0.0
        result = []

        # TODO: Write your code here
        for i in range(len(dev_set)):
            candidate_likelihoods = []
            for j in range(14):
                candidate_likelihood = 0
                for word in dev_set[i]:
                    if not self.occurrence[j].__contains__(word):
                        self.occurrence[j][word] = 0
                for word in dev_set[i]:
                    candidate_likelihood += np.log((self.occurrence[j][word]+1) /
                                                   (self.class_word_count[j] + len(self.unique_words)))
                candidate_likelihoods.append(candidate_likelihood+self.class_probability[j])
            result.append(candidate_likelihoods.index(max(candidate_likelihoods))+1)

        accuracy = np.sum(np.array(result) == np.array(dev_label)) / np.size(np.array(result))

        return accuracy, result