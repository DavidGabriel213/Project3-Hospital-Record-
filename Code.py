import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
df=pd.read_csv("/storage/emulated/0/Download/hospital_data_messy.csv")
df=df.drop_duplicates()
df["Age"]=df["Age"].astype(str)
df["Age"]=df["Age"].str.replace("yrs","")
def age_correction(x):
    if len(x)==3:
        return x[:2]
    else:
        return x
df["Age"]=df["Age"].apply(lambda x: age_correction(x))
df["Age"]=pd.to_numeric(df["Age"],errors="coerce")
df["Age"]=np.abs(df["Age"])
df["Age"]=df["Age"].fillna(df["Age"].median()).astype(int)
df["Gender"]=df["Gender"].astype(str).str.strip()
def gender_correction(x):
    for c in ["M","m","1","mal","MALE","Male"]:
        if x==c:
            return "Male"
            break
    if x=="nan":
        return np.nan
    else:
        return "Female"
df["Gender"]=df["Gender"].apply(lambda x:gender_correction(x))
df["Gender"]=df["Gender"].fillna(df["Gender"].mode()[0])
df["BloodGroup"]=df["BloodGroup"].fillna(df["BloodGroup"].mode()[0]).astype(str)
df["Hospital"]=df["Hospital"].astype(str).str.strip()
def hospital_correction(x):
    if x=="NHA":
        return "National Hospital Abuja"
    elif x=="AKTH":
        return "Aminu Kano Teaching Hospital"
    elif (x=="ATBUTH" or x=="atbuth"):
        return "ATBUTH Bauchi"
    elif (x=="lagos uni hospital" or x=="LUTH Marina"):
        return "Lagos State Hospital"
    elif x=="abuth":
        return "ABUTH Zaria"
    elif x=="nan":
        return np.nan
    else:
        return x
df["Hospital"]=df["Hospital"].apply(lambda x: hospital_correction(x))
df["Hospital"]=df["Hospital"].fillna(df["Hospital"].mode()[0])
df["Department"]=df["Department"].fillna(df["Department"].mode()[0]).astype(str)
df["Diagnosis"]=df["Diagnosis"].fillna(df["Department"].mode()[0]).astype(str)
df["BloodPressure"]=df["BloodPressure"].astype(str).str.replace("/","-").str.replace(" over ","-").str.strip()
def systolic(x):
    if "-" in x:
       d=int(x.index("-"))
       return int(x[:d])
    else:
        return x
df["Systolic"]=df["BloodPressure"].apply(lambda x:systolic(x))
df["Systolic"]=pd.to_numeric(df["Systolic"],errors="coerce")
k=df.groupby("Diagnosis")["Systolic"].mean()
df=df.set_index("Diagnosis")
df["Systolic"]=df["Systolic"].fillna(k)
df=df.reset_index()
df["Systolic"]=df["Systolic"].astype(int)
def diabolic(x):
    if "-" in x:
       d=int(x.index("-"))
       return int(x[(d+1):])
    else:
        return np.nan
df["Diabolic"]=df["BloodPressure"].apply(lambda x:diabolic(x))
df["Diabolic"]=pd.to_numeric(df["Diabolic"],errors="coerce")
k=df.groupby("Diagnosis")["Diabolic"].mean()
df=df.set_index("Diagnosis")
df["Diabolic"]=df["Diabolic"].fillna(k)
df=df.reset_index()
df["Diabolic"]=df["Diabolic"].astype(int)
df["BloodPressure"]=(df["Systolic"].astype(str) + " - " + df["Diabolic"].astype(str)).str.strip()
df["BMI"]=df["BMI"].astype(str).str.replace("kg/m2","").str.strip()
df["BMI"]=np.abs(pd.to_numeric(df["BMI"],errors="coerce"))
df["BMI"]=df["BMI"].apply(lambda x:x/10 if x>100 else x)
df["BMI"]=df["BMI"].fillna(df["BMI"].mean())
df["BloodGlucose(mg/dL)"]=df["BloodGlucose(mg/dL)"].astype(str).str.replace("mg/dL","").str.strip()
df["BloodGlucose(mg/dL)"]=np.abs(pd.to_numeric(df["BloodGlucose(mg/dL)"],errors="coerce"))
df["BloodGlucose(mg/dL)"]=df["BloodGlucose(mg/dL)"].apply(lambda x: x/10 if x>1000 else x)
df["BloodGlucose(mg/dL)"]=df["BloodGlucose(mg/dL)"].fillna(df["BloodGlucose(mg/dL)"].mean())
df["LengthOfStay(days)"]=df["LengthOfStay(days)"].astype(str).str.replace("days","").str.strip()
df["LengthOfStay(days)"]=np.abs(pd.to_numeric(df["LengthOfStay(days)"],errors="coerce"))
df["LengthOfStay(days)"]=(df["LengthOfStay(days)"].fillna(df["LengthOfStay(days)"].median())).astype(int)
df["TreatmentCost(NGN)"]=df["TreatmentCost(NGN)"].astype(str).str.replace("\"","").str.replace("NGN","").str.replace("naira","").str.replace(",","").str.strip()
df["TreatmentCost(NGN)"]=np.abs(pd.to_numeric(df["TreatmentCost(NGN)"],errors="coerce"))
new_w=df.groupby(["Hospital","Diagnosis"])["TreatmentCost(NGN)"].mean()
df=df.set_index(["Hospital","Diagnosis"])
df["TreatmentCost(NGN)"]=df["TreatmentCost(NGN)"].fillna(new_w)
df=df.reset_index()
df["InsuranceProvider"]=df["InsuranceProvider"].astype(str).str.strip()
def insurance_correction(x):
    d={"AXA":"AXA Mansard","nhis":"NHIS","Leadway":"LEADWAY","NIL":"none","Hygeia":"Hygeia HMO","hygeia HMO":"Hygeia HMO"}
    key=list(d.keys())
    if x in key:
        return d[x]
    else:
        return x
df["InsuranceProvider"]=df["InsuranceProvider"].apply(lambda x : insurance_correction(x))
df["InsuranceProvider"]=df["InsuranceProvider"].apply(lambda x : np.nan if x=="nan" else x)
df["InsuranceProvider"] =       df["InsuranceProvider"].fillna(df.groupby("Hospital")["InsuranceProvider"].transform(lambda x: x.mode()[0]))
df["AdmissionDate"]=pd.to_datetime(df["AdmissionDate"],format="mixed")
df["AdmissionDate"]=df["AdmissionDate"].fillna(df["AdmissionDate"].mode()[0])
df["Recovered"]=df["Recovered"].astype(str).str.capitalize().str.strip()
df["Recovered"]=df["Recovered"].apply(lambda x: "Yes" if x=="1" else "No" if x=="0" else np.nan if x=="Nan" else x)
df["Recovered"] =df["Recovered"].fillna(df.groupby("Diagnosis")["Recovered"].transform(lambda x: x.mode()[0]))
df["PulsePressure"]=df["Systolic"]-df["Diabolic"]
df["MeanArterialPressure(MAP)"]=df["Diabolic"]+(df["PulsePressure"]/3)
TC_distribution=df.groupby(["Hospital","Diagnosis"])["TreatmentCost(NGN)"].sum().unstack()
fig=plt.figure(figsize=(9,9))
gs=fig.add_gridspec(2,2)
ax1=fig.add_subplot(gs[0,:])
TC_distribution.plot(kind="bar",ax=ax1)
ax1.set_ylabel("Cost")
ax1.set_title("Cost Per Hospital",color="red")
AverageBMI=df.groupby("Department")["BMI"].mean()
ax2=fig.add_subplot(gs[1,0])
AverageBMI.plot(kind="bar",ax=ax2,color="purple",alpha=0.7)
ax2.set_title("AverageBMI per dptmt",color="red")
ax2.set_ylabel("Average")
ax3=fig.add_subplot(gs[1,1])
ax3.hist(df["MeanArterialPressure(MAP)"],bins=30,color="teal")
ax3.set_ylabel("MAP")
ax3.set_xlabel("Range")
ax3.set_title("MAP Distribution",color="red")
hT=df.groupby("Diagnosis")["TreatmentCost(NGN)"].mean().reset_index()
print(hT)
plt.tight_layout()
plt.show()
