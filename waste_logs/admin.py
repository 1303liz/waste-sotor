from django.contrib import admin
from .models import (
    WasteCategory, WasteSubcategory, WasteLog, 
    WasteEntry, WasteAttachment, WasteGoal
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
        }),
    )
