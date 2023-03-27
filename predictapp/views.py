from django.shortcuts import render
import pandas as pd
import pickle
from sklearn.linear_model import LinearRegression


csv_path = r'C:\Users\lenovo\amusementpark\AmusementPark\amusement_park_data.csv'
# Load the amusement park dataset
df = pd.read_csv(csv_path)

# Convert categorical variables to numerical variables
df = pd.get_dummies(df, columns=['Season'])
# Train a linear regression model on the dataset
X = df.drop('Num_Customers', axis=1)
y = df['Num_Customers']
model = LinearRegression()
model.fit(X, y)

def home(request):
    if request.method == 'POST':
        # Get the form data
        season = request.POST['season']
        offers = request.POST['offers']
        
        # Convert the categorical variable to numerical variable
        if season == 'Spring':
            season_spring = 1
            season_summer = 0
            season_fall = 0
            season_winter = 0
        elif season == 'Summer':
            season_spring = 0
            season_summer = 1
            season_fall = 0
            season_winter = 0
        elif season == 'Fall':
            season_spring = 0
            season_summer = 0
            season_fall = 1
            season_winter = 0
        else:
            season_spring = 0
            season_summer = 0
            season_fall = 0
            season_winter = 1
        
        # Make a prediction using the trained model
        prediction = round(model.predict([[season_spring, season_summer, season_fall, season_winter, offers]])[0],)
        
        # Render the result template with the prediction
        return render(request, 'predictapp/result.html', {'season':season ,'offers':offers,'prediction': prediction})
        
    else:
        # Render the home template
        return render(request, 'predictapp/home.html')
def result(request,prediction):
    return render(request, 'predictapp/home.html', {'prediction': prediction})



   