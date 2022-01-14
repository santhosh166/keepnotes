from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from notes.models import content
from.forms import registerform,loginform,createform
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout


import os
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.staticfiles import finders

# Create your views here.

def reg(request):
    if not request.user.is_authenticated:
        form=registerform()
        if request.method=="POST":
            form=registerform(request.POST)
            if form.is_valid():
                if not User.objects.filter(email=form.cleaned_data.get('email')).exists():
                    username=form.cleaned_data.get('username')
                    form.save()
                    messages.success(request,f'Account created Successfully for {username}')
                    return redirect('log')
                else:
                    messages.warning(request,'Email already verified one!')
                    return redirect('reg')
            else:
                return render(request,'reg.html',{'form':form})

        return render(request,'reg.html',{'form':form})
    else:return redirect('create')

def log(request):
    form=loginform()
    if request.user.is_authenticated:
           return redirect('create')
    else:
            if request.method=='POST':
                username=request.POST.get('username')
                password=request.POST.get('password1')
                user=authenticate(request,username=username,password=password)
                if user:
                    login(request,user)
                    return redirect('create')
                else:
                    messages.warning(request,'Username or Password is not valid one!')
                    return render(request,'log.html',{'form':form})
            else:return render(request,'log.html',{'form':form})

@login_required(login_url='log')
def log_out(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('log')
    else:
        return redirect('log')



@login_required(login_url='log')
def create(request):
    form=createform()
    if request.user.is_authenticated:
        if request.method=='POST':
            form=createform(request.POST,instance=request.user)
            if form.is_valid():
                tit=request.POST.get('title')
                des=request.POST.get('description')
                obj=content.objects.create(user=request.user,title=tit,description=des)
                obj.save()
                messages.success(request,f'Your note saved Successfully go to ShowMyNotes to check it out!')
                return redirect('create')
            else:
                return render(request,'create.html',{'form':form})

        else:return render(request,'create.html',{'form':form})
    else:return redirect('log')

           
@login_required(login_url='log')
def show(request):
    if  request.user.is_authenticated:
        objs=content.objects.filter(user=request.user)
        if objs:
            return render(request,'show.html',{'objs':objs})
        else:
            return render(request,'show.html')
    else:return redirect('log')

@login_required(login_url='log')
def update(request,id):
    obj=content.objects.get(id=id)
    form=createform(instance=obj)
    if request.method=='POST':
        form=createform(request.POST,instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request,'Updated Successfull!')
            return redirect('show')
        else:
            return render(request,'update.html',{'form':form})
    return render(request,'update.html',{'form':form})

@login_required(login_url='log')
def delete(request,id):
    obj=content.objects.get(id=id)
    if request.method=='POST':
        obj.delete()
        messages.success(request,'Deleted Successfull!')
        return redirect('show')
    return render(request,'delete.html',{'form':obj.title})



@login_required(login_url='log')
def download(request,id):
    note=content.objects.get(id=id)
    template_path = 'pdf.html'
    context = {'myvar': note}
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="report.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response)
    # if error then show some funy view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


