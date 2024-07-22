import pandas as pd
import numpy as np
import random
import pickle
import os
from itertools import product

from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

from django.conf import settings

# used_ids = set()

# def generate_unique_id(used_ids, id_range=(1000, 9999)):
#     while True:
#         unique_id = random.randint(*id_range)
#         if unique_id not in used_ids:
#             used_ids.add(unique_id)
#             return unique_id

def calculate_compatibility(combined_features):
    weights = {
        "strongest_subject_match": 0.1,
        "weak_subject_match": 0.2,
        "medium_match": 0.05,
        "dropper_match": 0.1,
        "medium_change_match": 0.5,
        "state_match": 0.05
    }
    student_strongest = combined_features[["student_maths_rank", "student_physics_rank", "student_chemistry_rank"]].idxmax(axis=1).replace({
        "student_maths_rank": "maths",
        "student_physics_rank": "physics",
        "student_chemistry_rank": "chemistry"
    })
    mentor_strongest = combined_features[["mentor_maths_rank", "mentor_physics_rank", "mentor_chemistry_rank"]].idxmax(axis=1).replace({
        "mentor_math_rank": "maths",
        "mentor_physics_rank": "physics",
        "mentor_chemistry_rank": "chemistry"
    })
    combined_features["strongest_subject_match"] = (student_strongest == mentor_strongest).astype(int)

    student_weakest = combined_features[["student_maths_rank", "student_physics_rank", "student_chemistry_rank"]].idxmin(axis=1).replace({
        "student_maths_rank": "maths",
        "student_physics_rank": "physics",
        "student_chemistry_rank": "chemistry"
    })
    mentor_weakest = combined_features[["mentor_maths_rank", "mentor_physics_rank", "mentor_chemistry_rank"]].idxmin(axis=1).replace({
        "mentor_maths_rank": "maths",
        "mentor_physics_rank": "physics",
        "mentor_chemistry_rank": "chemistry"
    })
    combined_features["weak_subject_match"] = (student_weakest == mentor_weakest).astype(int)

    combined_features["medium_match"] = (combined_features["student_medium"] == combined_features["mentor_medium"]).astype(int)
    combined_features["dropper_match"] = (combined_features["mentor_dropper"] == combined_features["student_dropper"]).astype(int)
    combined_features["state_match"] = (combined_features["mentor_state"] == combined_features["student_state"]).astype(int)
    combined_features["medium_change_match"] = (combined_features["student_medium_change"] == combined_features["mentor_medium_change"]).astype(int)

    score = 0
    for feature, weight in weights.items():
        score += combined_features[feature] * weight
    return score

def train(mentors):
    
    
    print(type(mentors), mentors)
    # students = pd.read_csv("csv/students.csv") 
    students = pd.read_csv('./csv/students.csv') 
    
    students = students[['id','Name','dropper_status', 'state','physics','chemistry','maths','medium','did_you_change ','student_gender']]
    mentors = mentors[['id','Name', 'IIT','state','dropper_status','physics_rank','chemistry_rank','maths_rank','medium','did_you_change','mentor_gender']]

    mentors = mentors.rename(columns = {'id':'mentor_id','Name':'mentor_name','dropper_status':'mentor_dropper','maths_rank':'mentor_maths_rank','physics_rank':'mentor_physics_rank','chemistry_rank':'mentor_chemistry_rank','medium':'mentor_medium','did_you_change':'mentor_medium_change', 'state':'mentor_state','IIT':'mentor_iit'})
    students = students.rename(columns = {'id':'student_id','Name':'student_name','dropper_status':'student_dropper','maths':'student_maths_rank','physics':'student_physics_rank','chemistry':'student_chemistry_rank','medium':'student_medium','did_you_change ':'student_medium_change', 'state':'student_state'})

    desired_order = ['mentor_id','mentor_name','mentor_iit','mentor_dropper','mentor_physics_rank','mentor_chemistry_rank','mentor_maths_rank','mentor_medium','mentor_medium_change','mentor_state','mentor_gender']
    mentors = mentors.reindex(columns=desired_order)

    # students['student_id']=students['student_id'].apply(lambda x : x.lower())
    students['student_name']=students['student_name'].apply(lambda x : x.lower())
    students['student_dropper']=students['student_dropper'].apply(lambda x : x.lower())
    students['student_medium']=students['student_medium'].apply(lambda x : x.lower())
    students['student_medium_change']=students['student_medium_change'].apply(lambda x : x.lower())
    students['student_state']=students['student_state'].apply(lambda x : x.lower())
    students['student_gender']=students['student_gender'].apply(lambda x : x.lower())
    
    # mentors['mentor_id']=mentors['mentor_id'].apply(lambda x : x.lower())
    mentors['mentor_name']=mentors['mentor_name'].apply(lambda x : x.lower())
    mentors['mentor_dropper']=mentors['mentor_dropper'].apply(lambda x : x.lower())
    mentors['mentor_medium']=mentors['mentor_medium'].apply(lambda x : x.lower())
    mentors['mentor_medium_change']=mentors['mentor_medium_change'].apply(lambda x : x.lower())
    mentors['mentor_state']=mentors['mentor_state'].apply(lambda x : x.lower())
    mentors['mentor_gender']=mentors['mentor_gender'].apply(lambda x : x.lower())
    mentors['mentor_iit']=mentors['mentor_iit'].apply(lambda x : x.lower())
    
    # global used_ids 
    # students['student_id'] = [generate_unique_id(used_ids) for _ in students['student_name']]
    # mentors['mentor_id'] = [generate_unique_id(used_ids) for _ in mentors['mentor_name']]
    
    rows_mentors = mentors.to_dict('records')
    rows_students = students.to_dict('records')
    all_pairs = list(product(rows_mentors, rows_students))
    combined_features = pd.DataFrame([{**x, **y} for x, y in all_pairs])
    
    combined_features['compatibility_score'] = calculate_compatibility(combined_features)
    combined_features = combined_features[['student_id', 'mentor_id','mentor_iit','mentor_gender','student_gender','strongest_subject_match','weak_subject_match','medium_match', 'dropper_match','medium_change_match','state_match','compatibility_score']]
    
    combined_features['mentor_iit'] = combined_features['mentor_iit'].apply(lambda x: x.replace(" ", ""))
    
    mentor_encoder = LabelEncoder()
    student_encoder = LabelEncoder()
    combined_features['mentor_iit'] = mentor_encoder.fit_transform(combined_features['mentor_iit'])

    def gender_code(gender):
        if gender.lower() == 'female':
            return 0
        elif gender.lower() == 'male':
            return 1
        else:
            return None

    combined_features['student_gender'] = combined_features['student_gender'].apply(gender_code)
    combined_features['mentor_gender'] = combined_features['mentor_gender'].apply(gender_code)
    
    X = combined_features.drop("compatibility_score", axis=1)
    y = combined_features["compatibility_score"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    y_pred_train = model.predict(X_train)
    y_pred_test = model.predict(X_test)
    mse_train = mean_squared_error(y_train, y_pred_train)
    mse_test = mean_squared_error(y_test, y_pred_test)
    print("mse for test:", mse_test)
    print("mse for train:", mse_train)

    with open('./models/model_saved_mediumchange_priority.pkl', 'wb') as f:
        pickle.dump(model, f)
    with open('./models/mentor_encoder_mediumchange_priority.pkl', 'wb') as f:
        pickle.dump(mentor_encoder, f)

# if __name__ == "__main__":
#     mentors_final = pd.read_csv("csv/Mentors_Database (corrected).csv") 
#     train(mentors_final)
