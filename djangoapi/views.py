from django.shortcuts import render
from . forms import ApprovalForm
from rest_framework import viewsets,status
from rest_framework.decorators import api_view
from django.core import serializers
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework.parsers import JSONParser
from . models import approvals
from . serializers import approvalsSerializers
import pickle
from django.contrib import messages
import joblib
import json
import numpy as np
from sklearn import preprocessing
import pandas as pd
# Create your views here.
class ApprovalsView(viewsets.ModelViewSet):
    queryset=approvals.objects.all()
    serializer_class=approvalsSerializers
def myform(request):
    if request.method=="POST":
        form=MyForm(request.POST)
        if form.is_valid():
            myform=form.save(commit=False)
        else:
            form=MyForm()

def ohevalue(df):
    ohe_col=['Loan_Amount_Term', 'Credit_History', 'Balance_Income_log',
       'Gender_Female', 'Gender_Male', 'Married_No', 'Married_Yes',
       'Dependents_3', 'Dependents_0', 'Dependents_1', 'Dependents_2',
       'Education_Graduate', 'Education_Not Graduate', 'Self_Employed_No',
       'Self_Employed_Yes', 'Property_Area_Rural', 'Property_Area_Semiurban',
       'Property_Area_Urban' ]
    balanceamount=int(df._get_value(0,'ApplicantIncome'))+int(df._get_value(0,'CoApplicantIncome'))
    emi=(int(df._get_value(0,'Loan_Amount'))*1000)/int(df._get_value(0,'Loan_Amount_Term'))
    balanceamount-=emi
    df=df.drop(['ApplicantIncome','CoApplicantIncome','Loan_Amount'],1)
    print(balanceamount)
    if balanceamount>0:
        df['Balance_Income_log']=np.log(balanceamount)
        cat_columns=['Dependants','Gender','Married','Education','Self_Employed','Property_Area']
        df_processed = pd.get_dummies(df, columns=cat_columns)
        newdict={}
        for i in ohe_col:
            if i in df_processed.columns:
                newdict[i]=df_processed[i].values
            else:
                newdict[i]=0
        newdf=pd.DataFrame(newdict)
        return newdf
    else:
        return None
        
        

def approvereject(unit):
    try:
        mdl=joblib.load("/Users/ishrath/djangoapi/djangoapi/MyAPI/model.pkl")
        scalers=joblib.load("/Users/ishrath/djangoapi/djangoapi/MyAPI/scaler.pkl")
        X=scalers.transform(unit)
        y_pred=mdl.predict(X)
        y_pred=(y_pred>0.58)
        newdf=pd.DataFrame(y_pred,columns=['Status'])
        newdf=newdf.replace({True:'Approved',False:'Rejected'})
        return (newdf.values[0][0],X[0])
    except ValueError as e:
        return (e.args[0])

def cxcontact(request):
    if request.method=="POST":
        form=ApprovalForm(request.POST)
        if form.is_valid():
            Dependants=form.cleaned_data['Dependants']
            ApplicantIncome=form.cleaned_data['ApplicantIncome']
            CoApplicantIncome=form.cleaned_data['CoApplicantIncome']
            Loan_Amount=form.cleaned_data['Loan_Amount']
            Loan_Amount_Term=form.cleaned_data['Loan_Amount_Term']
            Credit_History=form.cleaned_data['Credit_History']
            Gender=form.cleaned_data['Gender']
            Married=form.cleaned_data['Married']
            Education=form.cleaned_data['Education']
            Self_Employed=form.cleaned_data['Self_Employed']
            Property_Area=form.cleaned_data['Property_Area']
            myDict = (request.POST).dict()
            df=pd.DataFrame(myDict, index=[0])
            # print(df)
            temp=ohevalue(df)
            print(temp)
            if temp is not None:
                print('Appeoved')
                answer=approvereject(temp)[0]
                print(answer)
                messages.success(request,'Yay!! Your Loan has been {}'.format(answer))
            else:
                messages.success(request,'Ooops!! Your Loan Application has been Rejected')
    form=ApprovalForm()
    return render(request,'myform/cxform.html',{'form':form})



