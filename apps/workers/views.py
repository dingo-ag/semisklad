from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import login
from django.contrib import messages

from django.shortcuts import redirect
from django.utils.translation import ugettext_lazy as _
from django.views.generic import FormView, CreateView, UpdateView

from django.http import Http404

from apps.workers.forms import RegistrationForm, ChangePasswordForm, ForgetPasswordForm, EnterNewPasswordForm
from apps.workers.models import Worker, Recovery


def workers_list(request):
    return redirect('/', request)


class WorkerRegistration(CreateView):
    template_name = 'workers/registration.html'
    form_class = RegistrationForm
    success_url = '/'
    model = Worker

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        messages.success(self.request, 'User %s registered successfully' % user.name)
        return redirect(self.success_url)


class ChangePassword(FormView):
    template_name = 'workers/change_password.html'
    form_class = ChangePasswordForm
    success_url = '/'
    model = Worker

    def form_valid(self, form):
        user = form.instance
        form.save()
        messages.success(self.request, 'Password for %s changed successfully' % user.get_full_name())
        return redirect(self.success_url, messages={'success': 'Password for %s changed successfully'})


class ForgetPassword(FormView):
    """
    Check the existence of a user by email and sending letter with recovery code on their email address.
    Sets all previously created Recovery objects for selected user to INACTIVE status.
    """
    success_url = '/'
    template_name = 'workers/forget_password.html'
    form_class = ForgetPasswordForm

    def form_valid(self, form):
        recovery_object = form.save()
        if Recovery.objects.filter(code=recovery_object.code).exists():  # check for Recovery was created
            messages.success(self.request, _('Message with restore code was send to your email address'))
        else:
            messages.error(self.request, _('Sorry, but something went wrong :('))
        return redirect('login')


class RestorePassword(UpdateView):
    """
    Checks code got from url exists and active.
    If it is ok ask for email and password. If not, raise 404 error.
    Checks that code is created for entered email.
    If all is ok - change password
    If something go wrong code.status sets to INACTIVE and it can't be used anymore.
    """
    success_url = 'login'
    template_name = 'workers/restore_password.html'
    form_class = EnterNewPasswordForm
    model = Worker

    def get_context_data(self, **kwargs):
        if 'code' not in kwargs:
            kwargs['code'] = self.kwargs.get('code')
        return super().get_context_data(**kwargs)

    def get_object(self, queryset=None):
        code = self.kwargs.get('code')
        recovery = Recovery.objects.get(code=code)
        if not recovery.is_active():
            raise Http404(_('Code is not active'))
        try:
            instance = recovery.worker
        except ObjectDoesNotExist:
            raise Http404(_('Code is not valid'))
        return instance

    def form_valid(self, form):
        worker = form.save()
        if form.changed:
            messages.success(request=self.request, message='Password for %s changed successful' % worker.name)
        else:
            messages.error(request=self.request, message='Password for %s do not changed' % worker.name)
        return redirect(self.success_url)
