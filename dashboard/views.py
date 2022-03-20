# Django Imports
from urllib import response
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.contrib.auth import authenticate, login

# Models
from signup.models import userprofile

# Package Imports
import requests
import os
import json
import pandas as pd
import numpy as np
from sklearn import linear_model
from sklearn.preprocessing import FunctionTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import OrdinalEncoder
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import StandardScaler
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.compose import make_column_selector
from sklearn.decomposition import PCA
from sklearn.impute import SimpleImputer

# Dashboard Render
def dashboard(request):
    user = User.objects.get(username = request.user)
    if (request.method=="GET") and ('code' in request.GET):

        # Grab Discord Client ID and Client Secret
        script_dir = os.path.dirname(os.path.realpath(__file__))
        config_file = open(os.path.join(script_dir, 'config.json'))
        config = json.load(config_file)
        config_file.close()
        cid = config['Discord Client ID']
        cis = config['Discord Client Secret']

        # Grab returned code from users auth
        code = request.GET['code']
        token = exchange_code(code, cid, cis)
        user_obj = get_user(token)
        
        # Updating user
        user.add(token['access_token'], token['refresh_token'])
        

    context = {
        "user": user
    }
    return render(request, "dashboard/dashboard.html", context)


# APIs
def get_data(request):
    labels = ["Thu, Fri, Sat, Sun"]
    payments = [40, 70, 40, 100]
    data = {
        "labels": labels,
        "data": payments
    }
    return JsonResponse(data)

def update_data(request):
    if request.method == "POST":
        transaction = request.GET['transaction']
        transaction_obj = Transaction(receiver = transaction['receiver'],
            ammount = transaction['ammount']
        )
        transaction_obj.save()
        return JsonResponse(status=200)
    return JsonResponse({"error": "something went wrong!"}, status=400)

def check_user(request):
    if request.method=="GET":
        pot_user = request.GET['user']
        if User.objects.filter(username = pot_user).exists():
            return JsonResponse({"user_exists": True}, status=200)
        return JsonResponse({"user_exists": False}, status=200)
    return JsonResponse({'error':'something bad'},status=400)


# Helper Functions
def exchange_code(code, client_id, client_secret):
    """ Exchanges Auth code for user token
    """
    url = 'https://discord.com/api/v8'
    data = {
        'client_id': client_id,
        'client_secret': client_secret,
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': 'http://127.0.0.1:8000/dashboard'
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    r = requests.post('%s/oauth2/token' % url, data=data, headers=headers)
    r.raise_for_status()
    return r.json()

def get_user(token):
    url = "https://discord.com/api/v8"
    auth = token['access_token']
    headers = {
        "Authorization": f"Bearer {auth}"
    }
    r = requests.get('%s/users/@me' % url, headers=headers)
    r.raise_for_status()
    return r.json()


# ML Analytics
def build_pipeline(model_df, train_test_split):
    categorical_features = ['Segments', 'BillingAddress', 'Transactions']
    categorical_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(missing_values=np.nan, strategy='most_frequent')),
        ('onehot', OneHotEncoder(handle_unknown='ignore'))])

    numeric_features = ['Spend']
    numeric_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(missing_values=np.nan, strategy='most_frequent')),
        ('stdscaler', StandardScaler())])

    base_preprocessor = ColumnTransformer(
        transformers=[('cat', categorical_transformer, categorical_features),
                    ('num', numeric_transformer, numeric_features)])

    baseline_pl = Pipeline(steps=[('preprocessor', base_preprocessor),
                        ('regression', linear_model.LinearRegression())])

    # Split the train and test portions (random state for reproducibility)
    baseX_train, baseX_test, basey_train, basey_test = train_test_split(model_df.drop('Impressions', axis=1), model_df.Impressions, test_size=0.2, random_state=54321)

class StdScalerByGroup(BaseEstimator, TransformerMixin):
    
    def __init__(self):
        pass

    def fit(self, X, y=None):
        """
        :Example:
        >>> cols = {'g': ['A', 'A', 'B', 'B'], 'c1': [1, 2, 2, 2], 'c2': [3, 1, 2, 0]}
        >>> X = pd.DataFrame(cols)
        >>> std = StdScalerByGroup().fit(X)
        >>> std.grps_ is not None
        True
        """
        # X may not be a pandas dataframe (e.g. a np.array)
        df = pd.DataFrame(X)
        # A dictionary of means/standard-deviations for each column, for each group.
        self.grps_ = {'means': (df.groupby('CountryCode').mean()).to_dict('index'), 'stds': (df.groupby('CountryCode').std()).to_dict('index')}
        return self

    def transform(self, X, y=None):
        """
        :Example:
        >>> cols = {'g': ['A', 'A', 'B', 'B'], 'c1': [1, 2, 3, 4], 'c2': [1, 2, 3, 4]}
        >>> X = pd.DataFrame(cols)
        >>> std = StdScalerByGroup().fit(X)
        >>> out = std.transform(X)
        >>> out.shape == (4, 2)
        True
        >>> np.isclose(out.abs(), 0.707107, atol=0.001).all().all()
        True
        """
        try:
            getattr(self, "grps_")
        except AttributeError:
            raise RuntimeError("You must fit the transformer before tranforming the data!")
        

        # Define a helper function here?
        
        def z_scale(df):
            means = df['CountryCode'].map(self.grps_['means'])
            stds = df['CountryCode'].map(self.grps_['stds'])
            big_df = pd.DataFrame()                  
            for val in self.grps_['means'].keys():
                new_df = df[df['CountryCode'] == val]
                            
                for col in new_df.drop('CountryCode', axis=1).columns:
                    new_df[col] = (new_df[col] - self.grps_['means'][val][col]) / self.grps_['stds'][val][col]
                                        
                big_df = pd.concat([big_df, new_df])
            
            return big_df
        # X may not be a dataframe (e.g. np.array)
        df = pd.DataFrame(X)   
        return z_scale(df).drop('CountryCode', axis=1)

def test_alpha(preprocessor):
    # Test multiple alpha values
    for alpha in np.arange(0,1.1,0.1):
        # Redefine the pipelines with a Ridge model
        pl = Pipeline(steps=[('preprocessor', preprocessor),
                        ('regression', linear_model.Lasso(alpha=alpha))])
