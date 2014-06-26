#!/usr/bin/python                                                                                                                             \
"""
	Wordpress Auto Featured Image
	Combs through posts and assigns a featured image to posts which are missing one.
"""

import os
import sys
import re
import MySQLdb as mdb
import urllib
import hashlib

wp_database     = 'blog_turpin2'
wp_table_prefix = 'wp_'
wp_upload_dir   = '/srv/wordpress/turpin2/'
wp_img_url       = 'turpinrealtors.com/blog/wp-content/'

db_host = ''
db_user = ''
db_pass = ''

import includes.ImageManipulation as ImageManipulation
IM = ImageManipulation.ImageManipulation()
image_extensions = [ 'jpeg', 'jpg', 'png', 'gif' ]

con = mdb.connect('localhost', 'root', 'cleancut', use_unicode = False)
cur = con.cursor()

def start():
	print 'Searching for posts '
	qry = """ SELECT * FROM `%(db)s`.`%(prefix)sposts`; """ % {
		'db'      : wp_database,
		'prefix' : wp_table_prefix,
	}
	cur.execute( qry )
	all_posts = cur.fetchall()

	posts_with_out_featured_images = []
	for post in all_posts:
		qry = """ SELECT * FROM `%(db)s`.`%(prefix)spostmeta`
			WHERE 
				`meta_key` = "_thumbnail_id" AND
				`post_id`     = %(post_id)s; """ % {
			'db'        : wp_database,
			'prefix'   : wp_table_prefix,
			'post_id' : post[0]
		}
		cur.execute( qry )
		post_image_meta = cur.fetchall()

		# If there's no image thumbnail, lets try and set one with an image currently hosted on the server
		possible_featured_image_candidates = [ ]
		if len( post_image_meta ) == 0:
			posts_with_out_featured_images.append( post[0] )
			images = __extract_images_from_string( post[4] )
			if len( images ) > 0:
				best_post_image = __evaluate_images( images )
				sys.exit()	

"""
	Extract Images from String
	@desc
		Will find all unique image urls in a block of text
"""
def __extract_images_from_string( the_string ):
	found_images = []
	for ext in image_extensions:
		if ext in the_string:
			for found in [ m.start() for m in re.finditer( wp_img_url, the_string ) ]:
				segment =  the_string[ found : ]
				segment = segment[ : segment.find( '>' ) ]
				segment = segment.split(' ')[0]
				segment = segment.replace( '"', '' )
				img_url = segment.replace( "'", '' )
				found_images.append( img_url )
	found_images = list( set( found_images ) )
	return found_images

def __evaluate_images( images ):
	if not os.path.exists( './tmp'):
		os.makedirs( './tmp' )
	# Download the images
	downloaded_images = []
	for img_url in images:
		img_url    = 'http://' + img_url
		img_path = './tmp/' + hashlib.md5( img_url ).hexdigest()
		try:
			urllib.urlretrieve( img_url , img_path )
			downloaded_images.append( { 'img_url' : img_url, 'img_path' : img_path } )
		except:
			print 'Error downloading image ', img_url

	# Check and store the image sizes
	largest_pic  = 0
	largest_size = 0
	c            = 0
	for img in downloaded_images:
		dimensions = IM.find_image_dimensions( img['img_path'] )
		downloaded_images[ c ][ 'dimensions' ] = dimensions
		if dimensions['total'] > largest_size:
			largest_size = dimensions['total']
			largest_pic = c
		c = c + 1
	# print downloaded_images
	print downloaded_images[ largest_pic ]
	

	sys.exit()


if __name__ == "__main__":
	start()
	# find posts with out featured images

	# check if they have an image in the post_content

	# write the image record
		# wp_posts
		# 	post_author
		# 	post_date
		# 	post_date_gmt
		# 	post_title           : try and set
		# 	post_status        : inherit
		# 	comment_status
		# 	ping_status
		# 	post_password
		# 	post_name
		# 	to_ping
		# 	pinged
		# 	post_modified
		# 	post_content_filterred
		# 	post_parent
		# 	guid
		# 	menu_order
		# 	post_type
		# 	post_mime_type
		# 	comment_count

		# wp_postmeta
		# 	post_id : the image post_id
		# 	meta_key    :   _( %wp_table_prefix% )_attatched_file 
		# 	meta_value :'2014/06/run21.jpg'

		# 	post_id : the image post_id
		# 	meta_key    :   _( %wp_table_prefix% )_attachment_metadata 
		# 	meta_value : a:5:{s:5:"width";i:3008;s:6:"height";i:2000;s:4:"file";s:17:"2014/06/run21.jpg";s:5:"sizes";a:4:{s:9:"thumbnail";a:4:{s:4:"file";s:17:"run21-150x150.jpg";s:5:"width";i:150;s:6:"height";i:150;s:9:"mime-type";s:10:"image/jpeg";}s:6:"medium";a:4:{s:4:"file";s:17:"run21-300x199.jpg";s:5:"width";i:300;s:6:"height";i:199;s:9:"mime-type";s:10:"image/jpeg";}s:5:"large";a:4:{s:4:"file";s:18:"run21-1024x680.jpg";s:5:"width";i:1024;s:6:"height";i:680;s:9:"mime-type";s:10:"image/jpeg";}s:13:"single-header";a:4:{s:4:"file";s:17:"run21-651x285.jpg";s:5:"width";i:651;s:6:"height";i:285;s:9:"mime-type";s:10:"image/jpeg";}}s:10:"image_meta";a:10:{s:8:"aperture";d:32;s:6:"credit";s:0:"";s:6:"camera";s:9:"NIKON D50";s:7:"caption";s:0:"";s:17:"created_timestamp";i:1179049187;s:9:"copyright";s:0:"";s:12:"focal_length";s:2:"60";s:3:"iso";s:3:"200";s:13:"shutter_speed";s:17:"0.066666666666667";s:5:"title";s:0:"";}}