from bs4 import BeautifulSoup
import os
import shutil
import io
import requests
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
import pickle


def get_data(source):
    soup = BeautifulSoup(source, 'lxml')
    list_urls = []
    download_url = 'https://football-data.co.uk/'
    for link in soup.find_all('a'):
        file = link.get('href')
        if file.endswith('E0.csv'):
            list_urls.append(download_url + file)
    try:
        shutil.rmtree('services/data')
        os.makedirs('services/data')

    except OSError:
        os.makedirs('services/data')

    for i in range(15):
        file_path = 'services/data'
        file_name = 'data'+str(i)+'.csv'
        with open((os.path.join(file_path, file_name)), 'wb') as f:
            for chunk in requests.get(list_urls[i]).iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)

    return "Successfully loaded data."



def save_data():
    try:
        os.remove('EPL.csv')
    except OSError:
        print("File 'EPL.csv' does not exist")

    all_match = pd.DataFrame()

    files = [file for file in os.listdir('services/data')]

    for file in files:
        df = pd.read_csv('services/data/'+file)
        all_match = pd.concat([all_match, df])

    all_df = all_match.dropna(how='all')

    all_df['Date'] = pd.to_datetime(all_df['Date'])
    all_df['Year'] = all_df['Date'].dt.year
    all_df = all_df.sort_values('Year')

    all_df = all_df.sort_values('Year', ascending=False)

    all_df.to_csv('EPL.csv')

    return "Successfully saved data."



def save_model(dataset):
    try:
        os.remove('saved.pkl')
    except OSError:
        print("File 'saved.pkl' does not exist.")

    le_home_team = LabelEncoder()
    dataset['HomeTeam'] = le_home_team.fit_transform(dataset['HomeTeam'])
    dataset['HomeTeam'].unique()

    le_away_team = LabelEncoder()
    dataset['AwayTeam'] = le_away_team.fit_transform(dataset['AwayTeam'])
    dataset['AwayTeam'].unique()

    X = dataset[['HomeTeam', 'AwayTeam']]
    y = dataset['Results']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=3)
    sc = StandardScaler()
    X_train = sc.fit_transform(X_train)
    X_test = sc.transform(X_test)
    model = LogisticRegression()
    model.fit(X_train, y_train)

    data = {'model':model, 'le_home_team':le_home_team, 'le_away_team':le_away_team}

    with open('saved.pkl', 'wb') as _file:
        pickle.dump(data, _file)

    with open('saved.pkl', 'rb') as _file:
        data = pickle.load(_file)

    model = data['model']

    accuracy = model.score(X_test,y_test)

    return f"Successfully saved prediction model with accuracy {accuracy}"