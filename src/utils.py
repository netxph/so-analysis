import re
import seaborn as sns
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import r2_score, mean_squared_error

def to_snake_case(name):
    name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    name = re.sub('__([A-Z])', r'_\1', name)
    name = re.sub('([a-z0-9])([A-Z])', r'\1_\2', name)
    return name.lower()

def count_percentage(x, y, data):
    return data \
        .groupby(x)[y] \
        .value_counts(normalize=True) \
        .mul(100) \
        .rename('percent') \
        .reset_index()

def plot_cat(x, y, data, aspect=2):
    df = data[[x, y]].dropna()
    df[y] = df[y].str.split(";")

    df_exp = df.explode(y)

    df_g = count_percentage(x, y, df_exp)

    g = sns.catplot(x = x, y = "percent", hue = y, kind="bar", aspect = aspect, data = df_g)

def clean_data(data):

    # simplify job_sat

    data.loc[data.job_sat.notnull(), "is_satisfied"] = data.job_sat.apply(lambda s: True if s in ["Very satisfied", "Slightly satisfied"] else False)

    # drop null job_sat

    satisfy = data.dropna(subset=["job_sat"])

    # create response vars
    y = satisfy.is_satisfied.astype(int)

    # drop respondent, age, comp_total, converted_comp, job_sat
    cols = ["hobbyist" ,"age1st_code" ,"comp_freq" ,\
        "country" ,"dev_type" ,"ed_level" ,"employment" ,"ethnicity" ,"gender" ,"new_dev_ops" ,\
        "new_dev_ops_impt" ,"new_ed_impt" ,"new_learn" ,"new_onboard_good" ,"new_other_comms" ,\
        "new_overtime" ,"op_sys" ,"org_size" ,"purchase_what" ,"sexuality" ,"undergrad_major" ,\
        "work_week_hrs" ,"years_code" ,"years_code_pro"]


    satisfy = satisfy.drop(satisfy.columns.difference(cols), axis=1)

    # for each numeric, fill with mean

    num_vars = satisfy.select_dtypes(include=['float', 'int']).columns

    for col in num_vars:
        satisfy[col].fillna((satisfy[col].mean()), inplace=True)

    # create dummies

    cat_vars = satisfy.select_dtypes(include=['object']).copy().columns
    for var in  cat_vars:
        # for each cat add dummy var, drop original column
        satisfy = pd.concat([satisfy.drop(var, axis=1), pd.get_dummies(satisfy[var], prefix=var, prefix_sep='_', drop_first=True)], axis=1)
    
    X = satisfy

    return X, y

def find_optimal_mod(X, y, cutoffs, test_size = .30, random_state=42, plot=True):
    '''
    INPUT
    X - pandas dataframe, X matrix
    y - pandas dataframe, response variable
    cutoffs - list of ints, cutoff for number of non-zero values in dummy categorical vars
    test_size - float between 0 and 1, default 0.3, determines the proportion of data as test data
    random_state - int, default 42, controls random state for train_test_split
    plot - boolean, default 0.3, True to plot result

    OUTPUT
    r2_scores_test - list of floats of r2 scores on the test data
    r2_scores_train - list of floats of r2 scores on the train data
    lm_model - model object from sklearn
    X_train, X_test, y_train, y_test - output from sklearn train test split used for optimal model
    '''
    r2_scores_test, r2_scores_train, num_feats, results = [], [], [], dict()
    for cutoff in cutoffs:

        #reduce X matrix
        reduce_X = X.iloc[:, np.where((X.sum() > cutoff) == True)[0]]
        num_feats.append(reduce_X.shape[1])

        #split the data into train and test
        X_train, X_test, y_train, y_test = train_test_split(reduce_X, y, test_size = test_size, random_state=random_state)

        #fit the model and obtain pred response
        lm_model = LogisticRegression(max_iter=1000)
        lm_model.fit(X_train, y_train)
        y_test_preds = lm_model.predict(X_test)
        y_train_preds = lm_model.predict(X_train)

        #append the r2 value from the test set
        r2_scores_test.append(r2_score(y_test, y_test_preds))
        r2_scores_train.append(r2_score(y_train, y_train_preds))
        results[str(cutoff)] = r2_score(y_test, y_test_preds)

    if plot:
        plt.plot(num_feats, r2_scores_test, label="Test", alpha=.5)
        plt.plot(num_feats, r2_scores_train, label="Train", alpha=.5)
        plt.xlabel('Number of Features')
        plt.ylabel('Rsquared')
        plt.title('Rsquared by Number of Features')
        plt.legend(loc=1)
        plt.show()

    best_cutoff = max(results, key=results.get)

    #reduce X matrix
    reduce_X = X.iloc[:, np.where((X.sum() > int(best_cutoff)) == True)[0]]
    num_feats.append(reduce_X.shape[1])

    #split the data into train and test
    X_train, X_test, y_train, y_test = train_test_split(reduce_X, y, test_size = test_size, random_state=random_state)

    #fit the model
    lm_model = LogisticRegression(max_iter=1000)
    lm_model.fit(X_train, y_train)

    return r2_scores_test, r2_scores_train, lm_model, X_train, X_test, y_train, y_test

def coef_weights(coefficients, X_train):
    '''
    INPUT:
    coefficients - the coefficients of the linear model 
    X_train - the training data, so the column names can be used
    OUTPUT:
    coefs_df - a dataframe holding the coefficient, estimate, and abs(estimate)
    
    Provides a dataframe that can be used to understand the most influential coefficients
    in a linear model by providing the coefficient estimates along with the name of the 
    variable attached to the coefficient.
    '''
    coefs_df = pd.DataFrame()
    coefs_df['est_int'] = X_train.columns
    coefs_df['coefs'] = coefficients
    coefs_df['abs_coefs'] = np.abs(coefficients)
    coefs_df = coefs_df.sort_values('abs_coefs', ascending=False)
    return coefs_df