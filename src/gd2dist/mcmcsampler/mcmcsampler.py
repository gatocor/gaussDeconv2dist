from .mcmcposteriorsampler import fit
from scipy.stats import norm
import pandas as pd
import numpy as np
import pickle as pk

from ..shared_functions import *

class mcmcsampler:
    """
    Class for the mcmc sampler of the deconvolution gaussian model
    """
    def __init__(self, K=1, Kc=1, alpha = 1, alphac = 1):
        """
        Constructor of the class


        Parameters
        -------------
            K: int, Number of components of the noise distribution
            Kc: int, Number of components of the convolved distribution
            **kwargs:
                alpha: float, parameter to determine the hyperprior of the noise weight components
                alphac: float, parameter to determine the hyperprior of the target weight components

        """
        
        self.K = K
        self.Kc = Kc
        self.alpha = alpha
        self.alphac = alphac

        self.fitted = False

        return

    def fit(self, dataNoise, dataConvolution, iterations = 1000, ignored_iterations = 1000, chains = 1, theta = None, kconst = 1, initial_conditions = [], show_progress = True, seed = 0):
        """
        Fit the model to the posterior distribution


        Parameters
        -------------
            dataNoise: list/npArray, 1D array witht he data of the noise
            dataConvolution: list/npArray, 1D array witht he data of the convolution
            iterations: int, number of samples to be drawn and stored for each chain during the sampling
            ignored_iterations: int, number of samples to be drawn and ignored for each chain during the sampling
            chains: int, number of independently initialised realisations of the markov chain
            theta: float, parameter of the prior gamma distribution acording to the definition of the wikipedia
            kconst: float, parameter k of the prior gamma distribution
            initialConditions: list, 1D array with all the parameters required to initialise manually all the components of all the chains the chains
            show_progress: bool, indicate if the method should show the progress in the generation of the new data
            seed: int, value to initialise the random generator and obtain reproducible results

        Returns
        ---------------
            Nothing
        """

        self.data = dataNoise
        self.datac = dataConvolution
        self.iterations = iterations
        self.ignored_iterations = ignored_iterations
        self.chains = chains
        self.theta = theta
        self.kconst = kconst 
        
        #Assign an approximate theta to make the prior vague
        if theta == None:
            self.theta = np.std(dataConvolution)

        self.samples = np.array(fit(dataNoise, dataConvolution, ignored_iterations, iterations, chains, self.K, self.Kc, self.alpha, self.alphac, self.theta, self.kconst, initial_conditions, show_progress, seed))
        
        self.fitted = True

        return

    def save(self, name):
        """
        Pickle save the model.

        Parameters
        ----------------
            name: string, name in which to store the model

        Return:
            nothing
        """
        if self.fitted:
            pickling_on = open(name+".pickle","wb")
            pk.dump({"K":self.K, "Kc":self.Kc, "alpha": self.alpha, "alphac": self.alphac, "iterations": self.iterations,
                     "ignored_iterations": self.ignored_iterations,
                     "chains":self.chains, "sigmawidth":self.sigmawidth, "samples":self.samples}, pickling_on)
            pickling_on.close()
        else:
            print("The model has not been fitted so there is nothing to save.")
        return

    def load(self, name):
        """
        Pickle load the model.

        Parameters
        ----------------
            name: string, name from which to recover the model

        Return:
            nothing
        """
        pickle_off = open(name+".pickle","rb")
        aux = pk.load(pickle_off)
        pickle_off.close()

        self.K = aux["K"]
        self.Kc = aux ["Kc"]
        self.alpha = aux["alpha"]
        self.alphac = aux["alphac"]
        self.iterations = aux["iterations"]
        self.ignored_iterations = aux["ignored_iterations"]
        self.chains = aux["chains"]
        self.sigmawidth = aux["sigmawidth"]
        self.samples = aux["samples"]

        self.fitted = True

        return

    def sample_autofluorescence(self, size = 1, style = "full", pos = None):
        """
        Generate samples from the fitted posterior distribution according to the noise distribution

        Parameters
        -------------
            size: int, number of samples to be drawn

        Returns 
        -------------
            list: list, 1D array with *size* samples from the model
        """

        if style=="full":
            return  np.array(sample_autofluorescence(self.samples,self.K,self.Kc,size=size))
        elif style=="single":
            if pos == None:
                pos = np.random.choice(range(len(self.samples))) 
                return  np.array(sample_autofluorescence(self.samples,self.K,self.Kc,size=size,pos=pos))
            else:
                return  np.array(sample_autofluorescence(self.samples,self.K,self.Kc,size=size,pos=pos))

        return  np.array(sample_autofluorescence(self.samples,self.K,self.Kc,size))

    def sample_deconvolution(self, size = 1, style = "full", pos = None):
        """
        Generate samples from the fitted posterior distribution according to the deconvolved distribution

        Parameters
        -------------
            size: int, number of samples to be drawn

        Returns
        -------------
            list: list, 1D array with *size* samples from the model
        """

        if style=="full":
            return  np.array(sample_deconvolution(self.samples,self.K,self.Kc,size=size))
        elif style=="single":
            if pos == None:
                pos = np.random.choice(range(len(self.samples))) 
                return  np.array(sample_deconvolution(self.samples,self.K,self.Kc,size=size,pos=pos))
            else:
                return  np.array(sample_deconvolution(self.samples,self.K,self.Kc,size=size,pos=pos))

        return  np.array(sample_deconvolution(self.samples,self.K,self.Kc,size))

    def sample_convolution(self, size = 1, style = "full", pos = None):
        """
        Generate samples from the fitted posterior distribution according to the convolved distribution

        Parameters
        -------------
            size: int, number of samples to be drawn

        Returns
        -------------
            list: list, 1D array with *size* samples from the model
        """

        if style=="full":
            return  np.array(sample_convolution(self.samples,self.K,self.Kc,size=size))
        elif style=="single":
            if pos == None:
                pos = np.random.choice(range(len(self.samples))) 
                return  np.array(sample_convolution(self.samples,self.K,self.Kc,size=size,pos=pos))
            else:
                return  np.array(sample_convolution(self.samples,self.K,self.Kc,size=size,pos=pos))

        return  np.array(sample_convolution(self.samples,self.K,self.Kc,size))

    def score_autofluorescence(self, x, percentiles = [0.05, 0.95], size = 100):
        """
        Evaluate the mean and percentiles of the the pdf at certain position acording to the convolved distribution

        Parameters
        -------------
            x: list/array, positions where to evaluate the distribution
            percentiles: list/array, percentiles to be evaluated
            size: int, number of samples to draw from the posterior to make the statistics, bigger numbers give more stability

        Returns
        -------------
            list: list, 2D array with the mean and all the percentile evaluations at all points in x
        """

        return  np.array(score_autofluorescence(self.samples, x, self.K, self.Kc, percentiles, size))

    def score_deconvolution(self, x, percentiles = [0.05, 0.95], size = 100):
        """
        Evaluate the mean and percentiles of the the pdf at certain position acording to the deconvolved distribution

        Parameters
        -------------
            x: list/array, positions where to evaluate the distribution
            percentiles: list/array, percentiles to be evaluated
            size: int, number of samples to draw from the posterior to make the statistics, bigger numbers give more stability

        Returns
        -------------
            list: list, 2D array with the mean and all the percentile evaluations at all points in x
        """

        return  np.array(score_deconvolution(self.samples, x, self.K, self.Kc, percentiles, size))

    def score_convolution(self, x, percentiles = [0.05, 0.95], size = 100):
        """
        Evaluate the mean and percentiles of the the pdf at certain position acording to the convolved distribution

        Parameters
        -------------
            x: list/array, positions where to evaluate the distribution
            percentiles: list/array, percentiles to be evaluated
            size: int, number of samples to draw from the posterior to make the statistics, bigger numbers give more stability

        Returns
        -------------
            list: list, 2D array with the mean and all the percentile evaluations at all points in x
        """

        return  np.array(score_convolution(self.samples, x, self.K, self.Kc, percentiles, size))

    def sampler_statistics(self, sort="weight"):
        """
        Show statistics of correct mixing of the mcmc sampler
        
        Args:
            sort: ["weight", "none", "means"], method for sorting the samples from the different chains

        Returns
        -------------
            DataFrame: DataFrame the mean, std, percentiles, mixing ratio(rhat) and effective number of samples for each parameter of the model
        """
        
        self.sampler_statistics = pd.DataFrame(columns=["Mean","Std","5%","50%","95%","Rhat","Neff"])

        samples = self.samples.copy()

        if sort == "weight":
            argsort = np.argsort(samples[:,0:self.K],axis=1)
            samples[:,0:self.K] = np.take_along_axis(samples[:,0:self.K],argsort,axis=1)
            samples[:,self.K:2*self.K] = np.take_along_axis(samples[:,self.K:2*self.K],argsort,axis=1)
            samples[:,2*self.K:3*self.K] = np.take_along_axis(samples[:,2*self.K:3*self.K],argsort,axis=1)

            argsort = np.argsort(samples[:,3*self.K:3*self.K+self.Kc],axis=1)
            samples[:,3*self.K:3*self.K+self.Kc] = np.take_along_axis(samples[:,3*self.K:3*self.K+self.Kc],argsort,axis=1)
            samples[:,(3*self.K+self.Kc):(3*self.K+2*self.Kc)] = np.take_along_axis(samples[:,(3*self.K+self.Kc):(3*self.K+2*self.Kc)],argsort,axis=1)
            samples[:,(3*self.K+2*self.Kc):(3*self.K+3*self.Kc)] = np.take_along_axis(samples[:,(3*self.K+2*self.Kc):(3*self.K+3*self.Kc)],argsort,axis=1)

        if sort == "mean":
            argsort = np.argsort(samples[:,self.K:2*self.K],axis=1)
            samples[:,0:self.K] = np.take_along_axis(samples[:,0:self.K],argsort,axis=1)
            samples[:,self.K:2*self.K] = np.take_along_axis(samples[:,self.K:2*self.K],argsort,axis=1)
            samples[:,2*self.K:3*self.K] = np.take_along_axis(samples[:,2*self.K:3*self.K],argsort,axis=1)

            argsort = np.argsort(samples[:,3*self.K+self.Kc:3*self.K+2*self.Kc],axis=1)
            samples[:,3*self.K:3*self.K+self.Kc] = np.take_along_axis(samples[:,3*self.K:3*self.K+self.Kc],argsort,axis=1)
            samples[:,(3*self.K+self.Kc):(3*self.K+2*self.Kc)] = np.take_along_axis(samples[:,(3*self.K+self.Kc):(3*self.K+2*self.Kc)],argsort,axis=1)
            samples[:,(3*self.K+2*self.Kc):(3*self.K+3*self.Kc)] = np.take_along_axis(samples[:,(3*self.K+2*self.Kc):(3*self.K+3*self.Kc)],argsort,axis=1)

        measures = np.zeros(7)
        for i in range(3*self.K+3*self.Kc):
            measures[0] = np.mean(samples[:,i])
            measures[1] = np.std(samples[:,i])
            measures[2:5] = np.percentile(samples[:,i],[5,50,95])
            measures[5] = rstat(samples[:,i],self.chains)
            measures[6] = effnumber(samples[:,i],self.chains)

            #Name the component
            if i < self.K:
                name = "weight_K"+str(1+i)
            elif i < 2*self.K:
                name = "mean_K"+str(1+i-self.K)
            elif i < 3*self.K:
                name = "std_K"+str(1+i-2*self.K)
            elif i < 3*self.K+self.Kc:
                name = "weight_Kc"+str(1+i-3*self.K)
            elif i < 3*self.K+2*self.Kc:
                name = "mean_Kc"+str(1+i-3*self.K-self.Kc)
            else:
                name = "std_Kc"+str(1+i-3*self.K-2*self.Kc)

            self.sampler_statistics = self.sampler_statistics.append(pd.Series(measures, ["Mean","Std","5%","50%","95%","Rhat","Neff"], name=name))

        return self.sampler_statistics
