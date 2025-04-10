# ml_model.py
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

class RecoveryModel:
    def __init__(self):
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.scaler = StandardScaler()
        
    def train(self, training_data_path):
        # Load sample data (for hackathon, you can use simulated data)
        data = pd.read_csv(training_data_path)
        
        # Features from wearable data (heart rate, steps, sleep, etc.)
        X = data[['heart_rate_avg', 'steps_daily', 'sleep_hours', 'temperature', 
                 'pain_level', 'medication_adherence', 'days_since_surgery']]
        
        # Target: 0 = needs attention, 1 = normal recovery
        y = data['recovery_status']
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
        
        # Scale features
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Train model
        self.model.fit(X_train_scaled, y_train)
        
        # Evaluate (for demo purposes)
        accuracy = self.model.score(X_test_scaled, y_test)
        print(f"Model accuracy: {accuracy:.2f}")
        
        return accuracy
    
    def predict_recovery_status(self, patient_data):
        """
        Predict if patient recovery is on track or needs attention
        Returns: probability of normal recovery, alert flag, and recommendations
        """
        # Scale new data
        features = np.array([[patient_data['heart_rate_avg'], 
                             patient_data['steps_daily'],
                             patient_data['sleep_hours'],
                             patient_data['temperature'],
                             patient_data['pain_level'],
                             patient_data['medication_adherence'],
                             patient_data['days_since_surgery']]])
        
        features_scaled = self.scaler.transform(features)
        
        # Predict probability of normal recovery
        prob_normal = self.model.predict_proba(features_scaled)[0][1]
        
        # Determine if alert needed (probability below 0.7)
        needs_attention = prob_normal < 0.7
        
        # Generate recommendations
        recommendations = self._generate_recommendations(patient_data, prob_normal)
        
        return {
            'probability_normal': float(prob_normal),
            'needs_attention': bool(needs_attention),
            'recommendations': recommendations
        }
    
    def _generate_recommendations(self, data, prob_normal):
        """Generate personalized recovery recommendations"""
        recommendations = []
        
        if data['heart_rate_avg'] > 100:
            recommendations.append("Elevated heart rate detected. Try relaxation techniques.")
            
        if data['steps_daily'] < 1000 and data['days_since_surgery'] > 3:
            recommendations.append("Daily activity is below target. Consider gentle walking if approved by doctor.")
            
        if data['sleep_hours'] < 6:
            recommendations.append("Sleep duration is below recovery targets. Prioritize rest.")
            
        if data['pain_level'] > 7:
            recommendations.append("Pain levels are high. Contact your healthcare provider.")
            
        if data['medication_adherence'] < 0.8:
            recommendations.append("Medication adherence is important. Set reminders for medications.")
            
        return recommendations