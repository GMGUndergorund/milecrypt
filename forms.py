from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Length, Optional, NumberRange

class CreateLinksetForm(FlaskForm):
    folder_name = StringField('Folder Name', 
                             validators=[DataRequired(), Length(min=1, max=100)],
                             render_kw={'placeholder': 'e.g., Hellblade II Crack + ISO'})
    
    links = TextAreaField('Download Links', 
                         validators=[DataRequired()],
                         render_kw={'placeholder': 'Enter one URL per line\nhttps://example.com/file1.zip\nhttps://example.com/file2.zip',
                                   'rows': 6})
    
    password = PasswordField('Password (Optional)', 
                            validators=[Optional(), Length(max=50)],
                            render_kw={'placeholder': 'Leave empty for no password protection'})
    
    expiry_hours = IntegerField('Expires in (hours)', 
                               validators=[Optional(), NumberRange(min=1, max=8760)],
                               render_kw={'placeholder': 'Leave empty for no expiry'})
    
    submit = SubmitField('Create Protected Links')

class CaptchaForm(FlaskForm):
    password = PasswordField('Password', 
                            validators=[Optional()],
                            render_kw={'placeholder': 'Enter password if required'})
    
    submit = SubmitField('Verify & Access Links')
