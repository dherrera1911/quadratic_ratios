##################
#
# TESTS FOR THE FUNCTIONS THAT COMPUTE MOMENTS
# OF QUADRATIC FORMS OF GAUSSIAN RANDOM VARIABLES
#
##################

import pytest
import torch
import numpy as np
import qr_library as qr
import torch.distributions.multivariate_normal as mvn
from test_functions import *

# Parameters of simulation
nDim = 30
nSamples = 500000

# Parameters of distribution
mu = make_mu_sin(nDim=nDim)
sigma = 0.7
covariance = make_covariance(nDim=nDim, sigmaScale=sigma, covType='random')
randMat1 = torch.randn(nDim, nDim)
M1 = torch.matmul(randMat1, randMat1.transpose(0, 1))
randMat2 = torch.randn(nDim, nDim)
M2 = torch.matmul(randMat2, randMat2.transpose(0, 1))

# Get empirical estimates
momentsE = qr.empirical_moments_quadratic_form(mu, covariance, M1,
                                               nSamples=nSamples)
covE = qr.empirical_covariance_quadratic_form(mu, covariance, M1, M2,
                                           nSamples=nSamples)

# Get theoretical moments
meanT = qr.quadratic_form_mean(mu, covariance, M1)
varT = qr.quadratic_form_var(mu, covariance, M1)
covT = qr.quadratic_form_cov(mu, covariance, M1, M2)

# Compare moments
error1 = (momentsE['mean'] - meanT)/meanT
error2 = (momentsE['var'] - varT)/varT
error3 = (covE - covT)/covT

maxError = torch.max(torch.tensor([error1, error2, error3]))
assert maxError < 0.02

