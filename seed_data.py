import pandas as pd
from run import app, db, Passenger

# Load Titanic CSV
df = pd.read_csv('dataset/titanic.csv')

with app.app_context():
    for _, row in df.iterrows():
        passenger = Passenger(
            name=row['Name'],
            age=row['Age'],
            sex=row['Sex'],
            survived=row['Survived'],
            pclass=row['Pclass']
        )
        db.session.add(passenger)
    db.session.commit()

print("✅ Titanic data seeded into database!")
