import logging
import json

from flask import render_template
from flask_wtf import Form
from wtforms import fields
from wtforms.validators import Required

from . import app, estimator, target_names


logger = logging.getLogger('app')

class PredictForm(Form):
    """Fields for Predict"""
    
    avg_reordered_items = fields.IntegerField('Avg Reordered items per order:', validators=[Required()])
    avg_days_since_prior = fields.IntegerField('Avg days since prior order:', validators=[Required()])
    hour_of_the_day = fields.IntegerField('Avg hour of the day:', validators=[Required()])
    day_of_the_week = fields.IntegerField('Avg day of the week:', validators=[Required()])
	
    submit = fields.SubmitField('Submit')


@app.route('/', methods=('GET', 'POST'))
def index():
    """Index page"""
    form = PredictForm()
    predicted_pu = None
    
    if form.validate_on_submit():
        # store the submitted values
        submitted_data = form.data
		
        # Retrieve values from form
        
        avg_reordered_items = int(submitted_data['avg_reordered_items'])
        avg_days_since_prior = int(submitted_data['avg_days_since_prior'])
        hour_of_the_day = int(submitted_data['hour_of_the_day'])
        day_of_the_week = int(submitted_data['day_of_the_week'])

        # Create array from values
        ic_instance = [avg_reordered_items, avg_days_since_prior, hour_of_the_day, day_of_the_week]

        my_prediction = estimator.predict(ic_instance)
        print(my_prediction)
        # Return only the Predicted iris species
        #predicted_pu = my_prediction[0]
        predicted_pu = target_names[my_prediction]

    return render_template('index.html',
        form=form,
        prediction=predicted_pu)
