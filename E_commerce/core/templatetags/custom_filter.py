from django import template

register = template.Library()

@register.filter(name='currency')
def currency(number):
    tmp = str(round(number))
     
    if(int(tmp) > 1000000000):
        num = tmp[:-9] + "." + tmp[-9:-6] + "." + tmp[-6:-3] + "." + tmp[-3:] 
    elif(int(tmp) > 1000000):
        num = tmp[:-6] + "." + tmp[-6:-3] + "." + tmp[-3:]
    else:
        num = tmp[:-3]+"."+tmp[len(tmp)-3:]
    return num+" VNĐ"


@register.filter(name='multiply')
def multiply(number , number1):
    return number * number1


