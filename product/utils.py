# -*- coding: utf-8 -*-
from django.db.models import Func, Avg
from django.template.loader import render_to_string


def arabic_slugify(string):
    """
    Slugify a given string. 
    """
    string = string.replace(" ", "-")
    string = string.replace(",", "-")
    string = string.replace("&", "-")
    string = string.replace("(", "-")
    string = string.replace(")", "")
    string = string.replace("؟", "")
    string = string.replace("!", "")
    return string.lower()


def unique_slug_generator(instance, new_slug=None):
    """
    Generate a unique slug for a given instance.
    """
    # check if the given arguments have a value of new slug
    # if yes, assign the given value to the slug field. 
    if new_slug is not None:
        slug = new_slug
    # if not, generate a slug using arabic slugify function.
    else:
        slug = arabic_slugify(instance.name)
    # get the instance class. 
    Klass = instance.__class__
    # check if there's any item with the same slug.
    qs = Klass.objects.filter(slug=slug).order_by('-id') 
    if qs.count() == 1 and qs.first().id == instance.id: 
        return slug   
    # if yes, generate a new slug of a random string and return recursive function with the new slug.
    elif qs.exists():
        new_slug = f'{slug}-{qs.first().id}'
        return unique_slug_generator(instance, new_slug=new_slug)
    return slug    


def datetime_to_string(datetime):
    """
    Take a datetime object and return a nicely formatted string, eg: Aug 06, 2020 at 07:21 PM. 
    """
    return datetime.strftime("%b %d, %Y at %I:%M %p")
    

def get_product_reviews_avg_rate(product_reviews):
    """
    Take product's reviews, and get their count and avg rate.
    """
    data = dict()
    # get product's reviews count
    product_reviews_count = product_reviews.count()
    # get product average rate
    try:
        product_avg_rate = int(product_reviews.aggregate(rounded_avg_price=Round(Avg('rate')))['rounded_avg_price'])*20
    except:
        product_avg_rate = 0
    data['html_reviews_avg_rate'] = render_to_string('product/includes/partial_product_avg_rate.html', 
        {'reviews_count':product_reviews_count, 'avg_rate_precentage':product_avg_rate,})
    return data


class Round(Func):
    """
    Round number to the nearest integer.
    """
    function = 'ROUND'
    template='%(function)s(%(expressions)s, 0)'
