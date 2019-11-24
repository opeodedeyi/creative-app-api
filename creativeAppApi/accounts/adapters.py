from allauth.account.adapter import DefaultAccountAdapter


class CustomUserAccountAdapter(DefaultAccountAdapter):

    def save_user(self, request, user, form, commit=True):
        """
        Saves a new `User` instance using information provided in the
        signup form. The default all-auth only provides some fields like:
        username, email and password. This function allows you to add other
        fields like the fullname added in this field. assuming you are trying 
        to add other fields, you would have to add it in a user_field function

        user_field(user, '#field', request.data.get('#field', ''))
        where #field is the name of the field you want to add, which in the case 
        below is the fullname
        """
        from allauth.account.utils import user_field

        user = super().save_user(request, user, form, False)
        user_field(user, 'fullname', request.data.get('fullname', ''))
        user.save()
        return user