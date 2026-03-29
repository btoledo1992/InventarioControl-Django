from django.db import models

class Categoria(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"


class Producto(models.Model):

    TALLES = [
        ('XS', 'XS'),
        ('S', 'S'),
        ('M', 'M'),
        ('L', 'L'),
        ('XL', 'XL'),
        ('XXL', 'XXL'),
    ]

    nombre    = models.CharField(max_length=200)
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True)
    talle     = models.CharField(max_length=10, choices=TALLES)
    color     = models.CharField(max_length=50)
    precio    = models.DecimalField(max_digits=10, decimal_places=2)
    stock     = models.PositiveIntegerField(default=0)
    foto      = models.ImageField(upload_to='productos/', blank=True, null=True)
    creado    = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre} - {self.talle} - {self.color}"

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"