from django.db import models
from django.urls import reverse

from .utils import (unique_slug_generator, get_filename_ext)


def image_upload_path(instance, filename):
    name, ext = get_filename_ext(filename)
    new_filename = f'{ instance.slug }{ ext }'
    return f'products/{new_filename}'


class Product(models.Model):

    name = models.CharField(max_length=500)
    slug = models.SlugField(blank=True, unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=12, decimal_places=2, default=9.99)
    # image = models.ImageField(upload_to='image_upload_path', null=True, blank=True)
    image = models.FileField(upload_to=image_upload_path, null=True, blank=True)
    featured = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_digital = models.BooleanField(default=False)


    class Meta:
        verbose_name = 'product'
        verbose_name_plural = 'products'
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('products:detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slug_generator(self)
        super(Product, self).save(*args, **kwargs)
