# ![](https://ga-dash.s3.amazonaws.com/production/assets/logo-9f88ae6c9c3871690e33280fcf557f33.png) Capstone Project: COVID-19 mRNA Vaccine Degradation Prediction

## Problem Statement
The goal of this project is to build a model which will predict the degradation rates at each base (A, C, G or U) of an RNA molecule which can be useful to develop models and design rules for RNA degradation to accelerate mRNA vaccine research and deliver a refrigerator-stable vaccine against SARS-CoV-2, the virus behind COVID-19.

## Background

mRNA vaccines have taken the lead as the fastest vaccine candidates for COVID-19, but currently, they face key potential limitations. One of the biggest challenges right now is how to design super stable messenger RNA molecules (mRNA). Conventional vaccines (like your seasonal flu shots) are packaged in disposable syringes and shipped under refrigeration around the world, but that is not currently possible for mRNA vaccines.

Researchers have observed that RNA molecules have the tendency to spontaneously degrade. This is a serious limitation--a single cut can render the mRNA vaccine useless. Currently, little is known on the details of where in the backbone of a given RNA is most prone to being affected. Without this knowledge, current mRNA vaccines against COVID-19 must be prepared and shipped under intense refrigeration, and are unlikely to reach more than a tiny fraction of human beings on the planet unless they can be stabilized.

Stanford’s School of Medicine are looking to leverage the data science expertise of the Kaggle community to develop models and design rules for RNA degradation.

## Dataset 
- The sequence data include two files for training and testing
- The training file contains 19 fields, and the test file contains 6 fields
- In train dataset, there are total 2400 rows of data. The sequence length is 107 characters each, but only 68 bases are measured.
- In test dataset, there are total 3634 rows of data. The sequence length contain 107 and 130 characters. 629 out of 3634 rows of data are seqence length with 107. The rest of 3005 data have sequence length of 130. For 130 sequence length, only 91 bases are measured.

## Data Dictionary

|Column|Type|Description|
|---|---|---|
|**id**|*integer*|Unique identifier sample.|
|**sequence**|*object*|Describes the RNA sequence, a combination of A, G, U, and C for each sample.|
|**structure**|*object*|An array of (, ), and. characters donate to the base is to be paired or unpaired.|
|**predicted_loop_type**|*object*|Describes the structural context of each character in sequence. S: paired "Stem" M: Multiloop I: Internal loop B: Bulge H: Hairpin loop E: dangling End X: external loop|
|**signal_to_noise**|*float*|Defined as mean( measurement value over 68 nts )/mean( statistical error in measurement value over 68 nts)|
|**SN_filter**|*integer*|Indicates if the sample passed filters.|
|**seq_length**|*integer*|The length of the sequence.|
|**seq_scored**|*integer*|This should match the length of reactivity, deg_* and error columns.|
|**reactivity_error**|*object*|Calculated errors in experimental values obtained in reactivity, and deg_* columns.|
|**deg_error_Mg_pH10**|*object*|Calculated errors in experimental values obtained in reactivity, and deg_* columns.|
|**deg_error_pH10**|*object*|Calculated errors in experimental values obtained in reactivity, and deg_* columns.|
|**deg_error_Mg_50C**|*object*|Calculated errors in experimental values obtained in reactivity, and deg_* columns.|
|**deg_error_50C**|*object*|Calculated errors in experimental values obtained in reactivity, and deg_* columns.|
|**reactivity**|*object*| These numbers are reactivity values for the first 68 bases used to determine the likely secondary structure of the RNA sample.|
|**deg_Mg_pH10**|*object*|The likelihood of degradation after incubating with magnesium on pH 10 at base or linkage.|
|**deg_pH10**|*object*|The likelihood of degradation after incubating without magnesium on pH10 at base or linkage.|
|**deg_Mg_50C**|*object*|The likelihood of degradation after incubating with magnesium at 50 degrees Celsius at base or linkage.|
|**deg_50C**|*object*|The likelihood of degradation after incubating without magnesium at 50 degrees Celsius at base or linkage.|

## EDA Summary

- Observed negative signal-to-noise value and also very high signal-to-noise value. This is an outlier which we will remove during modelling.
- Generally, there are high values of Degradation & Reactivity (all 5 targets) at the beginning of the sequence.
- There are high values of Errors in deg_error_pH10 & deg_error_50C but maybe we should not worry about these targets because evaluation is not based on these targets.
- - S (Paired "Stem") is the dominant loop type.
- E (Dangling End) and H (Hairpin Loop) are also highly represented in comparison with the rest
- . structure (unpaired) is dominating, the paired structures ) and ( are equally represented (sicne their pair together).
- A and G nucleotides are highly present in the sequences compared to C and U.
- Most correlation values (between targets) are around 0.5, we can consider our variables moderately correlated.
- The correlation between structure . and loop type S (Paired) is -1
- The correlation between structure ( and ) and loop type S is 0.58

## Regressor Model Evaluation

By refering to the published journal ([reference](https://iopscience.iop.org/article/10.1088/1742-6596/1997/1/012005)), model of Linear Regression (LR) and Light Gradient Boosting Machine (LGBM) are proposed for models development. However, with fitting the main 3 features of 'sequence', 'structure', 'predicted_loop_type' into 6 different models, none of the model performed well using multioutput regressor. The loss of all 6 models are not closed to 0. Therefore we further evaluate our model using one of the RNN (Recurrent Neural Networks) technique which is Gated Recurrent Unit (GRU) in Part 3 code 

## GRU Model Evaluation and Conceptual Understanding

Recurrent neural network (RNN) are used when the inputs are sequential i.e reading sequentially from left to right. This is perfect for modeling mRNA sequences because mRNA is a sequence of bases and each base is dependent on the bases that come before it. However, RNN suffers from short-term memory and thus often suffer from vanishing gradients problem. Long short Term Memory (LSTM) and Gated Recurrent Unit (GRU) models are the solution for this: they are cable of keeping long-term dependencies effectively while handling the vanishing/exploding gradient problems.

For this project, we used bidirectional GRU. Bidirectional GRUs are a type of bidirectional recurrent neural networks (RNN) with only the reset and update gates. It allows for the use of information from both previous time steps and later time steps to make predictions about the current state. Reset gate determines how to combine new input to previous memory and update gate determines how much of the previous state to keep.

During RNN-GRU modelling, there are 3 layers which are embedding layer, hidden later and dense layer in the model architect. The embedding layer extracts 200 features instead of the 14 input encoding features. The position of a base (A, C, G, or U) within the vector space is learned from the mRNA sequence and is based on the bases that surround the base when it is used. We set bidirectial GRU layer as our hidden layer. The hidden units have 256 in each direction, which means that the number of bidirectional layer units is equal to 256 + 256 = 512. The bidirectional layer is used to optimize the results as the data are passed in the forward and backward directions to better capture the information in the sequence data. The dense layer has 5 outputs (five target columns of reactivity) and the activation = ‘linear' because the problem is a regression problem.

Mean Columnwise Root Mean Square Error (MCRMSE) is used to validate the model. MCRMSE is the square root of the mean/average of the square of all of the error. The reason MCRMSE is used is because there are multiple outputs that we are trying to predict i.e. we need to predict degradation rates under multiple conditions, which normally would result in multiple RMSE values. The MCRMSE is simply an average across all RMSE values.

## Conclusion and Recommendations

The best model in our modelling is the GRU model, which provides an training MCRMSE of 0.2376. Train and test accuracy and loss are similar. Accuracy curve and loss curve of both train set and test set follow each other closely. Hence our model is not overfit. Accuracy improves overtime and loss decreases overtime. The model extracted 200 features using encoding and embedding layer extraction for the categorical features and five features as the numerical features. Then, the features are concatenated to the model. The models give promising results since they predict the five reactivity values with less validation MCRMSE of  0.2376 using bidirectional GRU. The sequence model is able to predict degradation by predicting five reactivity & degradation values for every position in the sequence on the testing dataset. 

GRU model is adopted for model deployment in part 4 code notebook. With the model deployement, we can recommend researchers to utilise the web application to do prediction on the reactivity and degradation at each base position. During the exploratory data analysis, it is noted that the first fews bases actually contributed to the highest reactivity & degradation. By combining the finding with the prediction model that we developed, we are able to help researchers in designing more stable covid-19 mRNA vaccine. 

## Future Work
- Perform data augmentation to increase the number of the training samples and overcome the problem of over-fitting
- Stack bidirectional GRU with bidirectional LSTM
- Try CNN
- Tune parameters such as learning rate, batch size, try another optimizer, number of layers, different types of layer, number of neurons per layer, and the type of activation functions for each layer.
# capstone
