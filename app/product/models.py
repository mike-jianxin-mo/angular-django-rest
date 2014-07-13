from django.db import models
from django.db.models import Max
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile

from app.sub_site.models import SubSite
from PIL import Image
from cStringIO import StringIO
import os

class Product(models.Model):
	name = models.CharField(max_length=500)
	desc = models.TextField()
	code = models.CharField(max_length=20)
	category = models.CharField(max_length=20)
	form = models.CharField(max_length=20)
	ingredients = models.TextField()
	site = models.ForeignKey(SubSite, related_name='products')
	order= models.IntegerField()

	def getThumbPhoto(self):
		photo = Photo.objects.filter(product = self.id).filter(is_default = True)
		return photo[0].thumbnail.url if photo else settings.MEDIA_URL + settings.DEFAULT_IMG['DIR'] + settings.DEFAULT_IMG['PRO_DEF_IMG']

	def getCurrentOrderNumber(self):
		curMaxDict = Product.objects.filter(site=self.site).aggregate(Max('order'))

		return 1 if curMaxDict['order__max'] is None else int(curMaxDict['order__max']) + 1

	def save(self, *args, **kwargs):

		if self.id:
			super(Product, self).save(*args, **kwargs)
		else :	
			self.order = self.getCurrentOrderNumber()
			super(Product, self).save(*args, **kwargs)


class Photo(models.Model):
	name = models.CharField(max_length=200)
	# image file 
	product = models.ForeignKey('Product', related_name='photos')
	is_default = models.BooleanField(default=True)

	image = models.ImageField(upload_to=settings.DEFAULT_IMG['DIR'], max_length=500,blank=True,null=True)
	thumbnail = models.ImageField(upload_to=settings.DEFAULT_IMG['DIR'], max_length=500,blank=True,null=True)

	def create_thumbnail(self):
		# original code for this method came from
		# http://snipt.net/danfreak/generate-thumbnails-in-django-with-pil/

		# If there is no image associated with this.
		# do not create thumbnail
		if not self.image:
			return

		# Set our max thumbnail size in a tuple (max width, max height)
		THUMBNAIL_SIZE = (200,200)

		DJANGO_TYPE = self.image.file.content_type

		if DJANGO_TYPE == 'image/jpeg':
			PIL_TYPE = 'jpeg'
			FILE_EXTENSION = 'jpg'
		elif DJANGO_TYPE == 'image/png':
			PIL_TYPE = 'png'
			FILE_EXTENSION = 'png'

		# Open original photo which we want to thumbnail using PIL's Image
		image = Image.open(StringIO(self.image.read()))

		# Convert to RGB if necessary
		# Thanks to Limodou on DjangoSnippets.org
		# http://www.djangosnippets.org/snippets/20/
		#
		# I commented this part since it messes up my png files
		#
		#if image.mode not in ('L', 'RGB'):
		#    image = image.convert('RGB')

		# We use our PIL Image object to create the thumbnail, which already
		# has a thumbnail() convenience method that contrains proportions.
		# Additionally, we use Image.ANTIALIAS to make the image look better.
		# Without antialiasing the image pattern artifacts may result.
		image.thumbnail(THUMBNAIL_SIZE, Image.ANTIALIAS)

		# Save the thumbnail
		temp_handle = StringIO()
		image.save(temp_handle, PIL_TYPE)
		temp_handle.seek(0)

		# Save image to a SimpleUploadedFile which can be saved into
		# ImageField
		suf = SimpleUploadedFile(os.path.split(self.image.name)[-1], temp_handle.read(), content_type=DJANGO_TYPE)
		# Save SimpleUploadedFile into image field
		self.thumbnail.save('%s_thumbnail.%s'%(os.path.splitext(suf.name)[0],FILE_EXTENSION), suf, save=False)

	def setDefaultState(self):
		photos = Photo.objects.filter(product = self.product).filter(is_default = True)

		self.is_default = False if len(photos) else True
		

	def save(self, *args, **kwargs):
		if self.id:
			super(Photo, self).save(*args, **kwargs)
		else :	
			# create a thumbnail
			self.create_thumbnail()
			# set photo default state
			self.setDefaultState()

		super(Photo, self).save(*args, **kwargs)

