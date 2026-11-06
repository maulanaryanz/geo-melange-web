from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from .models import portofolio, Inquiry


@admin.register(portofolio)
class portofolioAdmin(admin.ModelAdmin):
    # 1. Menghapus bar dropdown "Aksi" dan kotak centang (checkbox) di sisi kiri
    actions = None

    # 2. Menampilkan data utama beserta kolom ikon shortcut di sisi paling kanan
    list_display = (
        'title',
        'category',
        'client_name',
        'year',
        'location',
        'shortcut_aksi',
    )
    list_filter = ('category', 'year')
    search_fields = ('title', 'client_name', 'location')

    # 3. Membuat deretan ikon shortcut (Lihat Foto, Edit/Pensil, Hapus/Tempat Sampah)
    @admin.display(description='')
    def shortcut_aksi(self, obj):
        edit_url = reverse('admin:core_portofolio_change', args=[obj.pk])
        delete_url = reverse('admin:core_portofolio_delete', args=[obj.pk])

        # Tombol Ikon Mata (Hanya muncul jika proyek memiliki foto lapangan)
        if obj.image:
            view_btn = format_html(
                '<a href="{}" target="_blank" title="Lihat Foto Dokumentasi" '
                'style="display:inline-flex; align-items:center; justify-content:center; '
                'width:30px; height:30px; border-radius:6px; background:rgb(236,253,245); '
                'color:rgb(5,150,105); margin-right:6px; text-decoration:none; '
                'border:1px solid rgb(167,243,208);">'
                '<svg xmlns="http://www.w3.org/2000/svg" width="15" height="15" viewBox="0 0 24 24" '
                'fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">'
                '<path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/>'
                '</svg></a>',
                obj.image.url,
            )
        else:
            view_btn = ''

        # Menggabungkan Ikon Mata, Pensil (Ubah), dan Tempat Sampah (Hapus)
        return format_html(
            '<div style="display:flex; align-items:center; justify-content:flex-end; white-space:nowrap;">'
            '{}'
            '<a href="{}" title="Ubah Portofolio" '
            'style="display:inline-flex; align-items:center; justify-content:center; '
            'width:30px; height:30px; border-radius:6px; background:rgb(239,246,255); '
            'color:rgb(37,99,235); margin-right:6px; text-decoration:none; '
            'border:1px solid rgb(191,219,254);">'
            '<svg xmlns="http://www.w3.org/2000/svg" width="15" height="15" viewBox="0 0 24 24" '
            'fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">'
            '<path d="M12 20h9"/><path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z"/>'
            '</svg></a>'
            '<a href="{}" title="Hapus Portofolio" '
            'style="display:inline-flex; align-items:center; justify-content:center; '
            'width:30px; height:30px; border-radius:6px; background:rgb(254,242,242); '
            'color:rgb(220,38,38); text-decoration:none; border:1px solid rgb(254,202,202);">'
            '<svg xmlns="http://www.w3.org/2000/svg" width="15" height="15" viewBox="0 0 24 24" '
            'fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">'
            '<polyline points="3 6 5 6 21 6"/>'
            '<path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/>'
            '<line x1="10" y1="11" x2="10" y2="17"/><line x1="14" y1="11" x2="14" y2="17"/>'
            '</svg></a>'
            '</div>',
            view_btn,
            edit_url,
            delete_url,
        )

    # 4. Mengubah tombol teks "TAMBAHKAN PORTOFOLIO PROYEK +" menjadi ikon (+) saja
    class Media:
        css = {
            'all': (
                'data:text/css;charset=utf-8,'
                '.object-tools a.addlink{font-size:0!important;width:36px!important;height:36px!important;'
                'padding:0!important;border-radius:8px!important;background:rgb(2,132,199)!important;'
                'display:inline-flex!important;align-items:center!important;justify-content:center!important;'
                'box-shadow:0 2px 6px rgba(2,132,199,0.3)!important;}'
                '.object-tools a.addlink::after{content:"+"!important;font-size:22px!important;'
                'font-weight:700!important;color:rgb(255,255,255)!important;line-height:1!important;}'
                '.object-tools a.addlink:hover{background:rgb(3,105,161)!important;}'
                'td a.addlink{font-size:0!important;padding:4px 8px!important;background-position:center!important;}',
            )
        }


@admin.register(Inquiry)
class InquiryAdmin(admin.ModelAdmin):
    actions = None
    change_list_template = "inquiry_change_list.html"
    change_form_template = "inquiry_change_form.html"
    list_display = ('full_name', 'organization', 'email', 'phone', 'is_processed', 'created_at')
    list_filter = ('is_processed', 'created_at')
    search_fields = ('full_name', 'organization', 'email', 'message')
    readonly_fields = ('created_at',)


# Kustomisasi Identitas Branding Admin Panel
admin.site.site_header = "CV. Geo Melange — Panel Administrasi"
admin.site.site_title = "Geo Melange Admin"
admin.site.index_title = "Ringkasan Data & Manajemen Sistem"