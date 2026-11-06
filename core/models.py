import os
from django.db import models
from django.core.validators import FileExtensionValidator
from django.db.models.signals import post_delete
from django.dispatch import receiver


class portofolio(models.Model):
    """
    Tabel untuk mendokumentasikan riwayat proyek dan studi teknis yang selesai dikerjakan.
    """
    CATEGORY_CHOICES = [
        ('studi_teknik', 'JASA STUDI, PENELITIAN & BANTUAN TEKNIK'),
        ('pariwisata', 'KEPARIWISATAAN'),
        ('survey', 'JASA SURVEY'),
    ]

    title = models.CharField(max_length=255, verbose_name="Judul Proyek")
    client_name = models.CharField(max_length=200, verbose_name="Nama Mitra / Klien")
    year = models.PositiveIntegerField(verbose_name="Tahun Pelaksanaan")
    location = models.CharField(max_length=200, verbose_name="Lokasi Lapangan")
    description = models.TextField(verbose_name="Deskripsi Pekerjaan")
    category = models.CharField(
        max_length=30, 
        choices=CATEGORY_CHOICES, 
        default='studi_teknik', 
        verbose_name="Kategori Proyek"
    )
    image = models.ImageField(
        upload_to='portofolio/', 
        blank=True, 
        null=True, 
        verbose_name="Foto Dokumentasi Lapangan"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Portofolio Proyek"
        verbose_name_plural = "Daftar Portofolio Proyek"
        ordering = ['-year', '-created_at']

    def __str__(self):
        return f"{self.title} ({self.year})"


class Inquiry(models.Model):
    """
    Tabel untuk menampung pesan, pertanyaan, dan pengajuan KAK/proposal dari calon klien.
    """
    full_name = models.CharField(max_length=200, verbose_name="Nama Lengkap")
    organization = models.CharField(max_length=200, blank=True, null=True, verbose_name="Instansi / Perusahaan")
    email = models.EmailField(verbose_name="Alamat Email")
    phone = models.CharField(max_length=50, verbose_name="Nomor Telepon / WhatsApp")
    message = models.TextField(verbose_name="Deskripsi Kebutuhan / Pesan")
    document = models.FileField(
        upload_to='proposals/', 
        blank=True, 
        null=True, 
        validators=[FileExtensionValidator(allowed_extensions=['pdf'])],
        verbose_name="Dokumen KAK / Proposal (PDF)"
    )
    is_processed = models.BooleanField(default=False, verbose_name="Sudah Diproses?")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Waktu Masuk")

    class Meta:
        verbose_name = "Pesan Masuk"
        verbose_name_plural = "Daftar Pesan Masuk"
        ordering = ['-created_at']

    def __str__(self):
        return f"Pesan dari {self.full_name} ({self.organization or 'Individu'})"


# ==============================================================================
# OTOMATIS HAPUS FILE FISIK SAAT DATA DIHAPUS DARI ADMIN
# ==============================================================================

@receiver(post_delete, sender=portofolio)
def hapus_foto_portofolio(sender, instance, **kwargs):
    """Menghapus file gambar portofolio dari folder media saat data proyek dihapus."""
    if instance.image and os.path.isfile(instance.image.path):
        os.remove(instance.image.path)


@receiver(post_delete, sender=Inquiry)
def hapus_dokumen_inquiry(sender, instance, **kwargs):
    """Menghapus file PDF proposal dari folder media saat pesan masuk dihapus."""
    if instance.document and os.path.isfile(instance.document.path):
        os.remove(instance.document.path)