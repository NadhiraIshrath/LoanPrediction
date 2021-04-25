from django import forms
class ApprovalForm(forms.Form):
    Dependants=forms.ChoiceField(choices=[('0','0'),('1','1'),('2','2'),('3','3+')])
    ApplicantIncome=forms.IntegerField()
    CoApplicantIncome=forms.IntegerField()
    Loan_Amount=forms.IntegerField()
    Loan_Amount_Term=forms.IntegerField()
    Credit_History=forms.IntegerField()
    Gender=forms.ChoiceField(choices=[('Male','Male'),('Female','Female')])
    Married=forms.ChoiceField(choices=[('Yes','Yes'),('No','No')])
    Education=forms.ChoiceField(choices=[('Graduate','Graduate'),('Not_Graduate','Not_Graduate')])
    Self_Employed=forms.ChoiceField(choices=[('Yes','Yes'),('No','No')])
    Property_Area=forms.ChoiceField(choices=[('Rural','Rural'),('Semiurban','Semiurban'),('Urban','Urban')])
