from django.db import models
from django_extensions.db.models import TitleSlugDescriptionModel, \
	TimeStampedModel, TitleDescriptionModel

from master.models import ComponentType, WidgetType
from django.contrib.auth.models import User
from django.db.models.deletion import SET_NULL
from project.models import Project
from printformat.models import PrintFormat
from transactionview.models import Transactionview,Component

VIEW_TYPES = (
	('total','Total',),
	('avg','Average',),
	('percentage','Percentage',),
	)


FILL_COLOR_TYPES = (
	('red','Red',),
	('blue','Blue',),
	('green','Green',),
	('yellow','Yellow',),
	('purple','Purple',),

	)

STROKE_COLOR_TYPES = (
	('red','Red',),
	('blue','Blue',),
	('green','Green',),
	('yellow','Yellow',),
	('purple','Purple',),

	)

GRAPH_TYPES = (
	('column','Column chart',),
	('line','Line chart',),
	('pie','Pie chart',),	
	('bar','Bar chart',),
	('horizontalBar','Horizontal Bar')
	
	
	)

REPORT_TYPES= (

	('onlinereport','OnlineReport'),
	('offlinereport','OfflineReport'),
	('displayreport','Displayreport'),
	('graphicalreport','Graphicalreport')
	)

REPORT_FIELD_TYPES= (
    ('query-field','Query Field'),
    ('expression-field','Expression Field'),
    ) 
    
REPORT_DATA_TYPES = (
	('char','Char'),
	('numeric','Numeric'),
	('datetime','DateTime'),
	('template_column','Template Column'),
	('button','Button')
	)
ALIGNMENT_TYPES = (
	('left','Left'),
	('center','Center'),
	('right','Right'),
	)

BOX_TYPES = (
	('small-panel','Small Panel',),
	('large-panel','Large Panel',),
	('medium-panel','Medium Panel',),
	)

RESULT_JOIN_TYPES = (
	('none','None'),
    ('left-outer-join','Left Outer Join'),
    ('inner-join','Inner Join'),
    ('cross-join','Cross Join'),
    )

TEMPLATE_TYPE_CHOICES=(
	('card','Card'),
	('list','List')
	)

ICON_TYPE_CHOICES =(
	('add','Add'),
	('albums','Albums'),
	('logo-android','Android'),
	('logo-angular','Angular'),
	('aperture','Aperture'),
	('logo-apple','Apple'),
	('apps','Apps'),
	('archive','Archive'),
	('barcode','Barcode'),
	('basket','Basket'),
	('bicycle','Bicycle'),
	('logo-bitcoin','Bitcoin'),
	('bonfire','Bonefire'),
	('book','Book'),
	('bookmark','Bookmark'),
	('bookmarks','Bookmarks'),
	('briefcase','Briefcase'),
	('calculator','Calculator'),
	('calendar','Calendar'),
	('card','Card'),
	('cash','Cash'),
	('clock','Clock'),
	('cloud','Cloud'),
	('codepen','Codepen'),
	('construct','Construct'),
	('contact','Contact'),
	('copy','Copy'),
	('create','Create'),
	('cube','Cube'),
	('desktop','Desktop'),
	('disc','Disc'),
	('document','Document'),
	('flame','Flame'),
	('flower','Flower'),
	('floder','Floder'),
	('globe','Globe'),
	('grid','Grid'),
	('help-buoy','Help-Buoy'),
	('home','Home'),
	('images','Images'),
	('information-circle','Information-Circle'),
	('keypad','Keypad'),
	('laptop','Laptop'),
	('list-box','List-Box'),
	('lock','Lock')
		)    

PRINT_ACTION_TYPE_CHOICES  = (
	('Server','Server'),
	('Client','Client')
)
SQL_TYPE_CHOICES = (
	('Nongrid','Nongrid'),
	('Grid','Grid')
	
)

class Report(TitleDescriptionModel, TimeStampedModel):
	enable_header = models.BooleanField(default=True)
	slug =  models.CharField( max_length=255, blank=True,null=True)
	project = models.ForeignKey(Project, related_name='reportview_projects',blank=True,null=True)
	report_header_line1 = models.CharField( max_length=255, blank=True, null=True)
	report_header_line2 = models.CharField( max_length=255, blank=True, null=True)
	report_footer_line1 = models.CharField( max_length=255, blank=True, null=True)
	report_footer_line2 = models.CharField( max_length=255, blank=True, null=True)
	row_count = models.SmallIntegerField(default=10)
	is_hidden = models.BooleanField(default=False)
	report_type = models.CharField(choices=REPORT_TYPES, max_length=20, blank=True,null=True)
	report_description = models.CharField( max_length=2000, blank=True, null=True)
	lines_per_page = models.PositiveSmallIntegerField(default=0)
	show_grand_total = models.BooleanField(default=False)
	template_type = models.CharField(choices=TEMPLATE_TYPE_CHOICES, max_length=20, blank=True,null=True)
	rowtemplate= models.TextField(blank=True,null=True)
	identifiers = models.CharField(max_length=150,null=True, blank=True)
	dont_repeat_reference_field = models.ForeignKey('ReportField', blank=True,null=True , related_name='+')
	xcoordinates= models.ForeignKey('ReportField', blank=True,null=True , related_name='+')
	ycoordinates= models.ForeignKey('ReportField', blank=True,null=True , related_name='+')
	showxyaxis= models.BooleanField(default=False)
	graphtype=models.CharField(choices=GRAPH_TYPES, max_length=20, blank=True,null=True)
	class Meta:
	    verbose_name = "Report"
	    verbose_name_plural = "Reports"

	def __str__(self):
	    return self.title
    

class Query(TitleDescriptionModel, TimeStampedModel):
	slug = models.CharField( max_length=255, blank=True, null=True)
	report = models.ForeignKey(Report, related_name='report_queries')
	sql = models.TextField()
	is_main_query = models.BooleanField(default=False)
	join_type =  models.CharField(choices=RESULT_JOIN_TYPES, max_length=20 , blank=True,null=True) 

	class Meta:
	    verbose_name = "Query"
	    verbose_name_plural = "Querys"

	def __str__(self):
	    return self.title

class ReportField(TitleDescriptionModel, TimeStampedModel):
	slug =  models.CharField( max_length=255, blank=True,null=True)
	report = models.ForeignKey(Report, related_name='report_fields')
	query = models.ForeignKey(Query , blank=True,null=True,on_delete=SET_NULL)
	caption = models.CharField(max_length=255,null=True)
	data_type = models.CharField(choices=REPORT_DATA_TYPES, max_length=20, blank=True,null=True)
	iconcls = models.CharField(choices=ICON_TYPE_CHOICES,max_length=100,null=True,blank=True)
	no_of_decimal_digits = models.SmallIntegerField(default=0)
	show_running_total = models.BooleanField(default=False)
	show_total = models.BooleanField(default=False)
	is_hidden = models.BooleanField(default=False)
	apply_comma = models.BooleanField(default=False)
	dont_repeat = models.BooleanField(default=False)
	column_alignment = models.CharField(choices=ALIGNMENT_TYPES	, max_length=20,blank=True,null=True)
	dont_show_zero = models.BooleanField(default=False)
	display_order = models.PositiveSmallIntegerField(default=0)
	width = models.PositiveSmallIntegerField(default=0)
	height = models.PositiveSmallIntegerField(default=0)
	iconcls = models.CharField(choices=ICON_TYPE_CHOICES,max_length=100,null=True,blank=True)
	expression = models.TextField(blank=True,null=True)
	validate_expression = models.TextField(blank=True,null=True) 

	class Meta:
	    verbose_name = "ReportField"
	    verbose_name_plural = "ReportFields"

	def __str__(self):
	    return self.title

class ReportParamField(TitleDescriptionModel, TimeStampedModel):
	slug =  models.CharField( max_length=255, blank=True,null=True)
	caption = models.CharField( max_length=255, blank=True, null=True)
	report = models.ForeignKey(Report, related_name='report_params')
	query =  models.ForeignKey(Query, blank=True,null=True,on_delete=SET_NULL)
	display_order = models.PositiveSmallIntegerField(default=0)
	is_hidden = models.BooleanField(default=False)
	no_of_decimal_digits = models.PositiveSmallIntegerField(default=0)
	data_type = models.CharField(choices=REPORT_DATA_TYPES, max_length=20, blank=True,null=True)
	component_type = models.ForeignKey('master.ComponentType' , related_name='+', blank=True,null=True)
	widget_type = models.ForeignKey('master.WidgetType', related_name='+', blank=True,null=True)
	value_field = models.CharField( max_length=100, blank=True,null=True )
	display_field = models.CharField( max_length=100, blank=True,null=True )
	sql = models.TextField( max_length=1000, blank=True,null=True )

	allow_empty = models.BooleanField(default=False)
	expression = models.TextField(blank=True,null=True) 
	expression_postfix = models.TextField(blank=True,null=True)  
	validate_expression = models.TextField(blank=True,null=True)
	validate_expression_postfix = models.TextField(blank=True,null=True)
	identifiers = models.CharField(max_length=150,null=True, blank=True)

	class Meta:
	    verbose_name = "ReportParamField"
	    verbose_name_plural = "ReportParamFields"

	def __str__(self):
	    return self.title



class ReportGrouping(models.Model):
	report = models.ForeignKey(Report, related_name='report_groupings')
	groupby_field = models.ForeignKey(ReportField, blank=True,null=True,on_delete=SET_NULL)
	caption_field = models.ForeignKey(ReportField,blank=True,null=True, related_name='+')
	header_caption_template = models.CharField( max_length=255, blank=True,null=True)
	footer_caption_template = models.CharField( max_length=255, blank=True,null=True)
	show_line_space = models.BooleanField(default=False)
	display_order = models.PositiveSmallIntegerField(default=0)

	class Meta:
	    verbose_name = "ReportGrouping"
	    verbose_name_plural = "ReportGroupings"

	def __str__(self):
	    return str(self.id)
	    

class ReportAction(TitleDescriptionModel):
	report = models.ForeignKey(Report, related_name='report_actions',blank=True,null=True)
	report_action = models.CharField(max_length=50,blank=True,null=True)
	order = models.DecimalField(max_digits=5, decimal_places=2, default=0)

	class Meta:
	    verbose_name = "ReportAction"
	    verbose_name_plural = "ReportActions"

	def __str__(self):
	    return self.title


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'static/ionicmeta/{0}/mustachehtml/{1}'.format(instance.project.slug,filename)


class ReportPrintFormatAction(TitleDescriptionModel):

	report_action = models.ForeignKey(ReportAction,blank=True,null=True,related_name='print_formats')
	pfconfig =  models.ForeignKey(PrintFormat,on_delete=models.SET_NULL,blank=True,null=True)
	# click_event = models.CharField(max_length = 1000,blank=True,null=True)
	
	class Meta:
		verbose_name = "PrintFormatAction"
		verbose_name_plural = "PrintFormatActions"

	def __str__(self):
	    return self.title

	

class ReportPDF(TitleDescriptionModel):
	iconcls = models.CharField(choices=ICON_TYPE_CHOICES,max_length=100,null=True,blank=True) 
	report_action = models.ForeignKey(ReportAction,blank=True,null=True)
	report = models.ForeignKey(Report, related_name='+',blank=True,null=True)
	class Meta:
		verbose_name = "ReportPDF"
		verbose_name_plural = "ReportPDFs"

	def __str__(self):
	    return self.title


class ReportCSV(TitleDescriptionModel):
	iconcls = models.CharField(choices=ICON_TYPE_CHOICES,max_length=100,null=True,blank=True) 
	report_action = models.ForeignKey(ReportAction,blank=True,null=True)
	report = models.ForeignKey(Report, related_name='+',blank=True,null=True)
	class Meta:
		verbose_name="ReportCSV"
		verbose_name_plural="ReportCSVs"

	def __str__(self):
	    return self.title

class ReportHTML(TitleDescriptionModel):
	iconcls = models.CharField(choices=ICON_TYPE_CHOICES,max_length=100,null=True,blank=True) 
	report = models.ForeignKey(Report, related_name='+',blank=True,null=True)
	report_action = models.ForeignKey(ReportAction,blank=True,null=True)
	class Meta:
		verbose_name="ReportHTML"
		verbose_name_plural="ReportHTMLs"

	
	def __str__(self):
	    return self.title


class ReportSubmit(TitleDescriptionModel):
	expression = models.TextField(null=True,blank=True)
	epost_target = models.ForeignKey(Transactionview,on_delete=models.SET_NULL,related_name='report_epost',null=True, blank=True)
	report = models.ForeignKey(Report, related_name='rpsubmit',blank=True,null=True)
	report_action = models.ForeignKey(ReportAction,blank=True,null=True)
	click_event = models.CharField(max_length = 1000)
	iconcls = models.CharField(choices=ICON_TYPE_CHOICES,max_length=100,null=True,blank=True) 

	def __str__(self):
	    return self.title

class Payment(TitleDescriptionModel):
	expression = models.TextField(null=True,blank=True)
	report = models.ForeignKey(Report, related_name='payment',blank=True,null=True)
	report_action = models.ForeignKey(ReportAction,blank=True,null=True)
	click_event = models.CharField(max_length = 1000)
	iconcls = models.CharField(choices=ICON_TYPE_CHOICES,max_length=100,null=True,blank=True) 

	def __str__(self):
	    return self.title

class NewAction(TitleDescriptionModel):
	expression = models.TextField(null=True,blank=True)
	report = models.ForeignKey(Report, related_name='newaction',blank=True,null=True)
	report_action = models.ForeignKey(ReportAction,blank=True,null=True)
	click_event = models.CharField(max_length = 1000)
	iconcls = models.CharField(choices=ICON_TYPE_CHOICES,max_length=100,null=True,blank=True) 

	def __str__(self):
	    return self.report

class ReportEpostMap(TimeStampedModel,models.Model):
	reportsubmit = models.ForeignKey(ReportSubmit,on_delete=models.CASCADE)
	source_ui_field =  models.ForeignKey(ReportField,on_delete=models.SET_NULL ,related_name='report_epost_source',null=True, blank=True) 
	target_ui_field =  models.ForeignKey(Component,on_delete=models.SET_NULL ,related_name='report_epost_target',null=True, blank=True)
	is_grid_field = models.BooleanField(default=False)
	expression = models.CharField(max_length = 1000,blank = True,null = True)

