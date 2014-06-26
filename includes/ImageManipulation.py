#!/usr/bin/python
"""
	Image Manipulation
	Assortment of image adjustment methods
"""

import sys
import os
import Image
import ImageOps
import struct

class ImageManipulation( object ):

	def __init__( self ):
		self.local_path = ''
		self.img        = ''
		self.args       = False
		self.bg         = False

	def get( self, local_path, args ):
		Log.write(' ')
		Log.write( '  Image Resizing' )
		Log.write( '    Args: %s' % str( args ) )      
		self.local_path = local_path
		self.img        = Image.open( self.local_path )
		self.args       = args
		if self.args:
			for key, value in self.args.iteritems():
				if key == 'crop':
					self.img = self.crop()
				elif key == 'maxWidth' or key == 'maxHeight':
					self.img = self.maxSize( dimension = key )
				if key == 'wattermark':
					self.img = self.wattermark()
				if key == 'flip':
					self.img = self.flip( args )
				if key == 'bg':
					self.bg = struct.unpack( 'BBB', args['bg'].decode('hex') )
		return self.img

	def maxSize( self, dimension ):
		print 'force either width or height to be a max size'
		if dimension == 'width':
			print 'the max width is ', self.args['maxWidth']
		elif dimension == 'height':
			print 'the max height is', self.args['maxHeight']

	def resize( self, extra_args = None ):
		print 'max width of height here'

	def crop( self, extra_args = None ):
		d_width  = self.args['crop']['width']
		d_height = self.args['crop']['height']
		im = self.img
		# Prepare to resize the image
		o_width  = im.size[0] 
		o_height = im.size[1]
		Log.write( '    Original Width: %spx, Original Height: %spx' % ( o_width, o_height ) )
		if d_width < d_height:
			d_smaller = d_width
		else:
			d_smaller = d_height

		if o_width < o_height:
			o_smaller = o_width
		else:
			o_smaller = o_height
		divisor = 2  
		while True:
			result = o_smaller / divisor
			if result < d_smaller:
				divisor = divisor - 1
				break
			divisor = divisor + 1

		n_width  = o_width / divisor
		n_height = o_height / divisor
		Log.write( '    Scaled Width: %spx, Scaled Height: %spx' % ( n_width, n_height ) )
		# Prepare the Crop
		if n_width > n_height:
			crop_left  = ( n_width / 2 ) - ( d_width / 2 )
			crop_upper = 0
			crop_right = crop_left + d_width 
			crop_lower = d_height
		else:
			crop_left  = 0
			crop_upper = ( n_height / 2 ) - ( d_width / 2 )
			crop_right = d_width
			crop_lower = crop_upper + d_width

		crop_cords = ( crop_left, crop_upper, crop_right, crop_lower )
		Log.write( '    Crop Cords: Left %spx, Upper: %spx, Right: %s, Lower: %s' % ( crop_left, crop_upper, crop_right, crop_lower ) )    
		im = im.resize((n_width, n_height), Image.ANTIALIAS) # best down-sizing filter
		im = im.crop( crop_cords )
		if self.bg:
			new_im = Image.new('RGBA', ( d_width, d_height  ), ( self.bg[0], self.bg[1], self.bg[2], 0) )
			new_im.paste( im )
			im = new_im
		return im

	def flip( self, extra_args ):
		if 'flip' in extra_args:
			if extra_args['flip'] == 'vertical' or extra_args['flip'] == 'v':
				return self.img.transpose( Image.FLIP_TOP_BOTTOM )
			else:
				return self.img.transpose( Image.FLIP_LEFT_RIGHT )

	def matte( self, extra_args = None ):
		print 'were matting now and shit'

	def wattermark( self ):
		print ''
		print ''
		print ''
		print 'wattermarkign'
		print self.args['wattermark']
		print ''
		print ''
		print ''
		return self.img

	def mirror( self ):
		print 'mirror'

	def find_image_dimensions( self, img_path = None ):
		if img_path:
			phile = img_path
			img   = Image.open( phile )
			return {
				'height' : img.size[0],
				'width'  : img.size[1],
				'total'  : img.size[0] * img.size[1]
			}

# End File: includes/ImageManipulation.py
