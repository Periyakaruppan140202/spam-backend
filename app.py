#from crypt import methods
from flask import Flask,request, url_for, redirect, render_template
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
import pandas as pd
app = Flask(__name__)

log_reg=pickle.load(open('model.pkl','rb'))
app.config['SERVER_NAME']="https://edp-spam-classifier.herokuapp.com"
@app.route('/')
def hello_world():
    return "hello"

@app.route('/predict/<string>',methods=['POST','GET'])
def predict(string):
    raw_mail_data = pd.read_csv('mail_data.csv')
    # print(raw_mail_data)
    mail_data = raw_mail_data.where((pd.notnull(raw_mail_data)), '')

    # print(mail_data.head())
    mail_data.loc[mail_data['Category'] == 'spam', 'Category', ] = 0
    mail_data.loc[mail_data['Category'] == 'ham', 'Category', ] = 1


    X = mail_data['Message']

    Y = mail_data['Category']
    # print(X)
    # print(Y)
    X_train, X_test, Y_train, Y_test = train_test_split(
        X, Y, test_size=0.2, random_state=3)
    # print(X.shape)
    # print(X_train.shape)
    # print(X_test.shape)

    feature_extraction = TfidfVectorizer(
        min_df=1, stop_words='english', lowercase='True')

    X_train_features = feature_extraction.fit_transform(X_train)
    X_test_features = feature_extraction.transform(X_test)

    input_mail=[string]
    print(len(input_mail[0]))
    if len(input_mail[0])<2:
        return redirect("http://192.168.143.122:5000/")
    input_data_features = feature_extraction.transform(input_mail)
    # making prediction
    prediction = log_reg.predict(input_data_features)
    pred="its a Spam  mail"
    prob=log_reg.predict_proba(input_data_features)
    if prediction[0] == 1:
        pred="its a Ham mail"
        return pred
        #return render_template("spam_detect.html",prediction=pred,prob="the probability of {} is {}".format(pred,round(prob[0][1],2)))
    return pred
    #return render_template("spam_detect.html",prediction=pred,prob="the probability of {}  is {}".format(pred,round(prob[0][0],2)))

if __name__=='__main__':
    app.run(debug=True)