from functools import lru_cache
from django.db import models
from django.conf import settings
import uuid

from django.db.models.fields import TextField
Usuario = settings.AUTH_USER_MODEL
# Create your models here.

METODO_PAGO=((1, 'Efectivo'), (2, 'Tarjeta debito/credito'))
STATUS_VENTA=((1, 'No Pagado'), (2, 'Parcialmente pagado'), (3, 'Pagado'),)
TIPO_VENTA=((1, 'Pieza'), (2, 'Paquete'), (3, 'Kit'))
IMPUESTOS=((1, 'ISR'), (2, 'IVA'), (3, 'IEPS'))

class Media(models.Model):
    m_nombre=models.CharField(verbose_name="Nombre", max_length=100)
    m_img=models.ImageField(verbose_name="Imagen ilustrativa", upload_to="media/img", help_text="Formato JPG, BMP o PNG")


class Tienda(models.Model):
    t_logo=models.ForeignKey(Media, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Imagen")
    t_nombre = models.CharField(verbose_name="Nombre", max_length=100)
    t_slogan = models.CharField(verbose_name="Slogan", max_length=150)
    t_direccion = models.CharField(verbose_name="Dirección", max_length=250)
    def __str__(self):
        return self.t_nombre
    class Meta:
        verbose_name_plural="A.- Tienda"


class Categoria(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    d_img=models.ForeignKey(Media, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Imagen")
    d_nombre = models.CharField(verbose_name="Nombre", max_length=80)
    def __str__(self):
        return self.d_nombre
class Marca(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    m_img=models.ForeignKey(Media, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Imagen")
    m_nombre = models.CharField(verbose_name="Nombre", max_length=80)
    def __str__(self):
        return self.m_nombre

class Cfdi(models.Model):
    cfdi_nombre=models.CharField(verbose_name="Nombre", max_length=150)
    def __str__(self):
        return self.cfdi_nombre
    # class Meta:
    #     verbose_name_plural="D.- CFDI"



class Impuesto(models.Model):    
    imp_valor=models.IntegerField(verbose_name="Valor", help_text="Expresado en enteros sin el signo de %")
    imp_nombre=models.CharField(verbose_name="Nombre", max_length=80, unique=True)
    imp_tipo=models.IntegerField(verbose_name="Tipo de impuesto", choices=IMPUESTOS)
    def __str__(self):
        return self.imp_nombre
    


class Producto(models.Model):
    id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    p_codigo_barras=models.CharField(verbose_name="Codigo de barras", max_length=150, unique=True)
    p_descripcion=models.CharField(verbose_name="Descripción", max_length=150)
    p_precio_costo=models.FloatField(verbose_name="Precio costo")
    p_precio_venta=models.FloatField(verbose_name="Precio Venta")
    p_precio_mayoreo=models.FloatField(verbose_name="Precio Mayoreo")
    p_categoria=models.ForeignKey(Categoria, verbose_name="Categorias", on_delete=models.SET_NULL, null=True, blank=True)
    p_marca=models.ForeignKey(Marca, verbose_name="Marca", on_delete=models.SET_NULL, null=True, blank=True)
    p_codigo_cfdi=models.ForeignKey(Cfdi, verbose_name="CFDI", help_text="Indispensable para emitir facturas electronicas", on_delete=models.SET_NULL, blank=True, null=True)    
    p_tipo_venta=models.IntegerField(verbose_name="Tipo de venta", choices=TIPO_VENTA)
    p_existencia=models.FloatField(verbose_name="Existencia", default=0.0)
    p_img=models.ForeignKey(Media, on_delete=models.SET_NULL, blank=True, related_name="only_img", null=True, verbose_name="Imagen")
    p_medias=models.ManyToManyField(Media, blank=True, verbose_name="Imagen")
    p_impuestos=models.ManyToManyField(Impuesto, blank=True, verbose_name="Impuestos")
    def __str__(self):
        return self.p_codigo_barras





class Venta(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    v_cliente=models.ForeignKey(Usuario, verbose_name="Cliente", on_delete=models.CASCADE)
    v_fecha=models.DateTimeField(auto_now_add=True, verbose_name="Fecha venta")
    v_fehcha_final=models.DateTimeField(auto_now=True, verbose_name="Fecha actualizacion")   
    v_status=models.IntegerField(verbose_name="Estatus", choices=STATUS_VENTA)
    def __str__(self):
        return f'{self.id}'
    


class Partida(models.Model):
    pr_venta=models.ForeignKey(Venta, verbose_name="Venta", on_delete=models.CASCADE)
    pr_producto=models.ForeignKey(Producto, verbose_name="Producto", on_delete=models.CASCADE)
    pr_precio_venta=models.FloatField(verbose_name="Precio Venta")
    pr_cantidad=models.FloatField(verbose_name="Cantidad")
    pr_impuestos=models.ManyToManyField(Impuesto, blank=True, verbose_name="Impuestos")
    pr_tipo_venta=models.IntegerField(verbose_name="Tipo de venta", choices=TIPO_VENTA)

    def __str__(self):
        return f'{self.pr_producto}'


class PublicidadProducto(models.Model):
    pp_nombre=models.CharField(verbose_name="Nobre", max_length=120)
    pp_descripcion=models.CharField(verbose_name="Breve descripcion", max_length=600)
    pp_producto=models.ForeignKey(Producto, verbose_name="Producto relacionado", on_delete=models.CASCADE)
    pp_img=models.ForeignKey(Media, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Imagen")
    def __str__(self):
        return f'{self.pp_nombre}'