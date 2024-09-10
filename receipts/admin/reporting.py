from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from django.contrib.admin import DateFieldListFilter
import nested_admin

from receipts.models.reporting import Reporting
