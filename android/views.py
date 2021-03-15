from django.shortcuts import render, get_object_or_404
from django import forms
from django.http import HttpResponseRedirect, HttpResponse
import requests
from android.models import  VerifyMobile
from django.urls import reverse
from django.contrib import messages

import json
# Create your views here.

class RegisterForm(forms.Form):
    number = forms.CharField(max_length=12, required=True)

    def clean(self):
        cleaned_data = super().clean()
        mobile = cleaned_data['number']
        if not len(mobile) == 12 or not mobile.isnumeric():
            raise forms.ValidationError("not a valid number",code="invalid")


class OTPVerifyForm(forms.Form):

    otp = forms.CharField(max_length=6, required=True)

    def clean(self):
        cleaned_data = super().clean()
        otp = cleaned_data['otp']
        if not len(otp) == 6 or not otp.isnumeric():
            raise forms.ValidationError("not a valid otp",code="invalid")


def register(request):
    """ If we get number in url, we will directly send verify 
    button, else number then otp for verify
    """
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            number = form.cleaned_data['number']
            # generate otp
            number_clean = "+" + str(number)
            target_url = request.scheme +'://'+request.get_host() + "/accounts/phone/register"
            print('target url ', target_url)
            res = requests.post(target_url,
                      json={'phone_number':number_clean }
                     )
            res = json.loads(res.content)
            print(res)
            token = res['session_token']

            # we will save form and redirect to verify
            obj = VerifyMobile.objects.create(token=token, number=number_clean)
            return HttpResponseRedirect(reverse('verify_phone', args=(obj.token,)))
        else:
            return render(request, 'android/register.html', {'form':form})

    else:
        number = request.GET.get('n',None)
    
        form = RegisterForm(initial={'number':number})
        return render(request, 'android/register.html', {'form':form})
            


   
def verify_phone(request, token):
    obj = get_object_or_404(VerifyMobile, token=token)

    if request.method == "POST":
        form = OTPVerifyForm(request.POST)
        if form.is_valid():
            otp = form.cleaned_data['otp']
            target_url = request.scheme +'://'+request.get_host() + "/accounts/phone/verify"
            print('target url', target_url)

            data={'phone_number': obj.number,
                  'session_token': obj.token,
                  'security_code': otp
                 }

            res = requests.post(target_url, json=data)
            print(res.content)
          
            if res.status_code == 200:
                messages.success(request, "Mobile {} is verified ".format(obj.number))
                return HttpResponseRedirect(reverse('success'))
          
            else:
               #{"non_field_errors":["Security code is not valid"]}'
               res = json.loads(res.content)
               for k, v in res.items():
                   if isinstance(v, list):
                       for i in v:
                           messages.error(request, i)
                   else:
                       messages.error(request, v)

               return render(request, 'android/verify_mobile.html', {'form':form})
               
               
                 

        else:
            return render(request, 'android/verify_mobile.html', {'form': form })

    else:
        form = OTPVerifyForm()

        return render(request, 'android/verify_mobile.html', {'form':form})

            
    
def success_page(request):
    return render(request, 'android/success.html')
