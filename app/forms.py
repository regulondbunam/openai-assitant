from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, SubmitField, TextAreaField, IntegerField
from wtforms.validators import DataRequired, NumberRange

class LoginForm(FlaskForm):
    """
    Represents a login form.

    Attributes:
        username (StringField): The field for entering the username.
        password (PasswordField): The field for entering the password.
        submit (SubmitField): The button for submitting the form.
    """
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Enviar')
    
class MessageForm(FlaskForm):
    """
    A form class for capturing user messages.

    Attributes:
        prompt (StringField): The input field for the user's message.
        submit (SubmitField): The button to submit the form.
    """
    prompt = StringField(label="This is an experimental generative AI chatbot. All information should be verified prior to use.", render_kw={"placeholder": "Preguntame lo que quieras"}, validators=[DataRequired()])
    submit = SubmitField('Enter')
    
class EvaluationForm(FlaskForm):
    """
    A form for evaluating a certain item.

    Attributes:
        rating (IntegerField): The rating given to the item, ranging from 1 to 5.
        comment (StringField): An optional comment about the item.
        submit (SubmitField): A button to submit the evaluation.
    """
    rating = IntegerField('Calificación:', validators=[DataRequired(),NumberRange(min=1, max=5)], default=5)
    comment = StringField('Comentario:')
    submit = SubmitField('Enviar')