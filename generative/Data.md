# What is Data.py

So the goal is to build a generative model for our data. That is, given a few datapoints from some customer, how well does it match our own data distribution? What datapoints do we have that are most similar to the customers (so that we can provide them with new data)? How can we learn a few important features of our data so that it is easier to find similarities/trends and do analysis?

## Data.py is an entry-level attempt at this first question

From the existing datapoints, we estimate a mean and covariance from our data samples. Then, we just choose one data point from our sample (but this can ideally be set to a specific customer point that a customer gives us), and estimate the probability of that point coming from our data distribution (or how likely it is under our data distribution). This just gives us an estimate of how well that point fits our data.

# Bugs

So, it turns out that the covariance matrix is singular because the data matrix is ill-conditioned. Thus, data.py doesn't actually work right now. The data first needs to be featurized/extracted correctly into a proper data matrix, so that the covariance matrix is no longer singular. Then this approach should work.

# What's next

Try new methods for generative modeling. Clustering, and then doing some gaussian estimation. Or using a Gaussian Mixture Model. Or some type of deep generative modeling (probably should get the simple ones working first though). Also, if the customer gives us a distribution of datapoints, we can measure KL divergences (or any other distribution divergence measure, like a symmetric measure such as Shannon Jensen might be good) to measure how similar/dissimilar the distributions are. I think exploring along these lines is a good starting point.