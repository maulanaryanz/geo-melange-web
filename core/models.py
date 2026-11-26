import os
from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver


class BidangLayanan(models.Model):
    name = models.CharField(max_length=150, unique=True, verbose_name="Nama Bidang / Layanan Pekerjaan")

    class Meta:
        ordering = ['name']
        verbose_name = "Bidang / Layanan"
        verbose_name_plural = "Daftar Bidang / Layanan"

    def __str__(self):
        return self.name


class portofolio(models.Model):
    year = models.IntegerField(verbose_name="Tahun Anggaran / Pelaksanaan")
    title = models.CharField(max_length=255, verbose_name="Nama Paket Pekerjaan")
    category = models.ForeignKey(
        BidangLayanan,
        on_delete=models.PROTECT,
        verbose_name="Bidang / Layanan Pekerjaan"
    )
    location = models.CharField(max_length=150, verbose_name="Lokasi")
    
    # Kolom Pemberi Tugas / Pengguna Jasa
    client_name = models.CharField(max_length=200, verbose_name="Nama Pemberi Tugas")
    client_address = models.TextField(blank=True, null=True, verbose_name="Alamat & Telepon Pemberi Tugas")
    
    # Kolom Kontrak
    contract_info = models.CharField(max_length=150, blank=True, null=True, verbose_name="No. & Tanggal Kontrak")
    contract_value = models.CharField(max_length=100, blank=True, null=True, verbose_name="Nilai Kontrak (Rp)")
    
    # Kolom Tanggal Selesai Menurut
    contract_end_date = models.CharField(max_length=100, blank=True, null=True, verbose_name="Tanggal Selesai (Kontrak)")
    handover_date = models.CharField(max_length=100, blank=True, null=True, verbose_name="Tanggal Selesai (BA. Penyerahan)")
    
    # Opsional jika masih ingin menyimpan foto dokumentasi
    image = models.ImageField(upload_to='portofolio/', blank=True, null=True, verbose_name="Foto Dokumentasi (Opsional)")

    class Meta:
        ordering = ['-year', 'id']
        verbose_name = "Portofolio Proyek"
        verbose_name_plural = "Daftar Portofolio Proyek"

    def __str__(self):
        return f"[{self.year}] {self.title}"


class Inquiry(models.Model):
    full_name = models.CharField(max_length=150, verbose_name="Nama Lengkap")
    organization = models.CharField(max_length=200, blank=True, null=True, verbose_name="Instansi / Perusahaan")
    email = models.EmailField(verbose_name="Alamat Email")
    phone = models.CharField(max_length=30, verbose_name="Nomor Telepon / WhatsApp")
    message = models.TextField(verbose_name="Detail Kebutuhan Proyek")
    document = models.FileField(upload_to='proposals/', blank=True, null=True, verbose_name="Lampiran Dokumen (PDF)")
    is_processed = models.BooleanField(default=False, verbose_name="Sudah Ditindaklanjuti")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Waktu Masuk")

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Pesan Masuk"
        verbose_name_plural = "Daftar Pesan Masuk"

    def __str__(self):
        return f"{self.full_name} - {self.organization or 'Personal'}"


# Sinyal otomatis menghapus file fisik dari folder media saat data dihapus dari database
@receiver(post_delete, sender=portofolio)
def delete_portofolio_image(sender, instance, **kwargs):
    if instance.image and os.path.isfile(instance.image.path):
        os.remove(instance.image.path)


@receiver(post_delete, sender=Inquiry)
def delete_inquiry_document(sender, instance, **kwargs):
    if instance.document and os.path.isfile(instance.document.path):
        os.remove(instance.document.path)