from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail

from django.contrib.auth.hashers import make_password
from django.contrib.auth import login
from django.contrib import messages

from django.shortcuts import redirect
from django.utils.translation import ugettext_lazy as _
from django.views.generic import FormView

from django.http import Http404

from semisklad.settings.local import HOST_NAME, HOST_PORT
from .forms import RegistrationForm, ChangePasswordForm, ForgetPasswordForm, EnterNewPasswordForm
from .models import Worker, Phone, Recovery
from utils.restore_password import create_code, check_code


def workers_list(request):
    return redirect('/', request)


class WorkerRegistration(FormView):
    template_name = 'workers/registration.html'
    form_class = RegistrationForm
    success_url = '/'

    def form_valid(self, form):
        email = form.cleaned_data.get('email')
        name = form.cleaned_data.get('name')
        surname = form.cleaned_data.get('surname')
        password = form.cleaned_data.get('password')
        hash_password = make_password(password)
        number = form.cleaned_data.get('phone_number')
        p = Phone.objects.create(number=number)
        user = Worker.objects.create(
            email=email,
            name=name,
            surname=surname,
            password=hash_password,
            phone=p
        )
        login(self.request, user)
        messages.success(self.request, 'User %s registered successfully' % name)
        return redirect(self.success_url)


class ChangePassword(FormView):
    template_name = 'workers/change_password.html'
    form_class = ChangePasswordForm
    success_url = '/'

    def form_valid(self, form):
        password = form.cleaned_data.get('new_password')
        user = Worker.objects.get(email=form.cleaned_data.get('email'))
        user.password = make_password(password)
        user.save()
        messages.success(self.request, 'Password for %s changed successfully' % user.get_full_name())
        return redirect(self.success_url, messages={'success': 'Password for %s changed successfully'})


class ForgetPassword(FormView):
    """
    Check the existence of a user by email and sending letter with recovery code on their email address.
    Sets all previously created Recovery objects to INACTIVE status.
    """
    success_url = '/'
    template_name = 'workers/forget_password.html'
    form_class = ForgetPasswordForm

    def form_valid(self, form):
        email = form.cleaned_data.get('email', '')
        if email:
            user = Worker.objects.get(email=email)
            code = create_code(user.id)
            link = HOST_NAME + ':' + HOST_PORT + '/workers/restore-password/' + code
            Recovery.objects.filter(worker=user).update(status=Recovery.Statuses.INACTIVE)
            Recovery.objects.create(code=code, worker=user, status=Recovery.Statuses.ACTIVE)
            if send_mail(
                'Semisklad password recovery',
                '',
                'support@semisklad.com',
                [email],
                html_message='<p>Follow the link below for recover your password.</p>'
                             '<p>The link is actual for 24 hours. </p>'
                             '<p><a href="{0}"><h2>LINK</h2><a></p>'.format(link)
            ):
                messages.success(self.request, _('Message with restore code was send to your email address'))
            else:
                messages.error(self.request, _('Sorry, but something went wrong :('))

        return redirect('login')


class RestorePassword(FormView):
    """
    Checks code got from url exists and active.
    If it is ok ask for email and password. If not, raise 404 error.
    Checks that code is created for entered email.
    If all is ok - change password
    If something go wrong code.status sets to INACTIVE and it can't be used anymore.
    """
    form_class = EnterNewPasswordForm
    template_name = 'workers/restore_password.html'

    def get(self, *args, **kwargs):
        code = self.kwargs.get('code', '')
        try:
            recovery = Recovery.objects.get(code=code)
        except ObjectDoesNotExist:
            raise Http404('Code wrong or expired')
        if not recovery.is_active():
            raise Http404('Code is not active')
        return self.render_to_response(self.get_context_data(code=code))

    def form_valid(self, form):
        code = self.kwargs.get('code', '')
        print('!!!!', code)
        email = form.cleaned_data.get('email', '')
        password = form.cleaned_data.get('new_password', '')
        if Recovery.objects.filter(code=code).exists():
            recovery = Recovery.objects.select_related('worker').get(code=code)
            # if not recovery.is_active():
            #     return Http404('Your recovery link is not active')
            if not check_code(code, recovery.worker.id):
                recovery.status = Recovery.Statuses.INACTIVE
                recovery.save()
                raise Http404('Your recovery link is not active')
            if recovery.worker.email == email:
                user = Worker.objects.get(email=email)
                user.set_password(password)
                user.save()
                recovery.status = Recovery.Statuses.INACTIVE
                recovery.save()
                print('user changed')
                messages.success(self.request, 'Password changed successfully')
            else:
                recovery.status = Recovery.Statuses.INACTIVE
                recovery.save()
                messages.error(self.request, 'Recovery code wrong')
                raise Http404('Recovery code wrong')

        else:
            raise Http404('Your recovery link is not active')
        return redirect('login')
