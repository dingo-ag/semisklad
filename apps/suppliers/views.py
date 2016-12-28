from django.shortcuts import redirect
from django.views.generic import ListView, DetailView
from apps.suppliers.models import Supplier, SupplierContact


class SuppliersList(ListView):
    template_name = 'suppliers/suppliers_list.html'
    queryset = Supplier.objects.all()
    context_object_name = 'suppliers'


class SupplierDetail(DetailView):
    # template_name = 'suppliers/supplier_detail.html'
    model = Supplier
    context_object_name = 'supplier'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['contacts'] = SupplierContact.objects.filter(employer=self.kwargs['pk'])
        return context
