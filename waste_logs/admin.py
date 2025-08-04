from django.contrib import admin
from .models import (
    WasteCategory, WasteSubcategory, WasteLog, 
    WasteEntry, WasteAttachment, WasteGoal
)
from .facilitator_models import (
    RecyclingFacilitator, RecyclingProcess,
    FacilitatorCollection, RecyclingImpactMetric
)

class WasteSubcategoryInline(admin.TabularInline):
    model = WasteSubcategory
    extra = 1

class WasteEntryInline(admin.TabularInline):
    model = WasteEntry
    extra = 0

class WasteAttachmentInline(admin.TabularInline):
    model = WasteAttachment
    extra = 0

@admin.register(WasteCategory)
class WasteCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_recyclable', 'is_compostable', 'is_hazardous')
    search_fields = ('name', 'description')
    list_filter = ('is_recyclable', 'is_compostable', 'is_hazardous')
    inlines = [WasteSubcategoryInline]

@admin.register(WasteSubcategory)
class WasteSubcategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'category')
    search_fields = ('name', 'description')
    list_filter = ('category',)

@admin.register(WasteLog)
class WasteLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'category', 'quantity_kg', 'date_logged', 'location')
    list_filter = ('category', 'user', 'date_logged', 'is_recurring')
    search_fields = ('title', 'description', 'location', 'user__username')
    date_hierarchy = 'date_logged'
    inlines = [WasteEntryInline, WasteAttachmentInline]
    fieldsets = (
        ('Basic Information', {
            'fields': ('user', 'title', 'description', 'category', 'subcategory', 'quantity_kg', 'date_logged')
        }),
        ('Location Information', {
            'fields': ('location', 'latitude', 'longitude'),
            'classes': ('collapse',),
        }),
        ('Additional Details', {
            'fields': ('is_recurring', 'recurrence_pattern', 'source', 'measurement_method'),
            'classes': ('collapse',),
        }),
    )

@admin.register(WasteEntry)
class WasteEntryAdmin(admin.ModelAdmin):
    list_display = ('user', 'waste_log', 'category', 'quantity_kg', 'date_logged')
    list_filter = ('category', 'user', 'date_logged')
    search_fields = ('notes', 'user__username')
    date_hierarchy = 'date_logged'

@admin.register(WasteAttachment)
class WasteAttachmentAdmin(admin.ModelAdmin):
    list_display = ('waste_log', 'title', 'file_type', 'uploaded_at')
    list_filter = ('file_type', 'uploaded_at')
    search_fields = ('title', 'description', 'waste_log__title')

@admin.register(WasteGoal)
class WasteGoalAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'target_quantity', 'current_quantity', 'unit', 'progress_percentage', 'is_completed')
    list_filter = ('is_completed', 'unit', 'start_date', 'category')
    search_fields = ('title', 'description', 'user__username')
    date_hierarchy = 'start_date'
    readonly_fields = ('progress_percentage', 'remaining_quantity')
    fieldsets = (
        ('Basic Information', {
            'fields': ('user', 'title', 'description', 'category')
        }),
        ('Goal Details', {
            'fields': ('target_quantity', 'current_quantity', 'unit', 'progress_percentage', 'remaining_quantity')
        }),
        ('Timeline', {
            'fields': ('start_date', 'end_date', 'is_completed')
        })
    )

@admin.register(RecyclingFacilitator)
class RecyclingFacilitatorAdmin(admin.ModelAdmin):
    list_display = ('name', 'website', 'phone', 'date_joined', 'is_active')
    search_fields = ('name', 'description', 'email')
    list_filter = ('is_active', 'date_joined')

class RecyclingProcessInline(admin.TabularInline):
    model = RecyclingProcess
    extra = 1

@admin.register(RecyclingProcess)
class RecyclingProcessAdmin(admin.ModelAdmin):
    list_display = ('title', 'facilitator', 'waste_category')
    search_fields = ('title', 'description', 'facilitator__name')
    list_filter = ('waste_category', 'facilitator')

@admin.register(FacilitatorCollection)
class FacilitatorCollectionAdmin(admin.ModelAdmin):
    list_display = ('facilitator', 'waste_category', 'quantity_kg', 'collection_date')
    search_fields = ('facilitator__name', 'notes', 'source_location')
    list_filter = ('waste_category', 'collection_date', 'facilitator')
    date_hierarchy = 'collection_date'

@admin.register(RecyclingImpactMetric)
class RecyclingImpactMetricAdmin(admin.ModelAdmin):
    list_display = ('facilitator', 'metric_name', 'metric_value', 'unit', 'metric_type', 'date_recorded')
    search_fields = ('metric_name', 'description', 'facilitator__name')
    list_filter = ('metric_type', 'date_recorded', 'facilitator')
