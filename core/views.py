import time
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from .models import portofolio, Inquiry


def home(request):
    portofolios = portofolio.objects.all()[:3]
    return render(request, 'index.html', {'portofolios': portofolios})


def profile_view(request):
    return render(request, 'profile.html')


def portofolio_view(request):
    portofolios = portofolio.objects.all()
    return render(request, 'portofolio.html', {'portofolios': portofolios})


def contact_view(request):
    if request.method == 'POST':
        # 1. Proteksi Anti-Spam (Jeda minimal 60 detik antar pengiriman per pengguna)
        last_submit = request.session.get('last_inquiry_submit', 0)
        now = time.time()
        if now - last_submit < 60:
            messages.error(request, 'Mohon tunggu 1 menit sebelum mengirim permintaan penawaran kembali.')
            return redirect('kontak')

        full_name = request.POST.get('full_name', '').strip()
        organization = request.POST.get('organization', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        message_text = request.POST.get('message', '').strip()
        document_file = request.FILES.get('document')

        # 2. Validasi Kolom Wajib & Nomor Telepon di Server (Wajib Angka, 8-15 digit)
        if not all([full_name, email, phone, message_text]):
            messages.error(request, 'Seluruh kolom bertanda bintang (*) wajib diisi.')
            return redirect('kontak')

        if not phone.isdigit() or not (8 <= len(phone) <= 15):
            messages.error(request, 'Nomor WhatsApp / Telepon hanya boleh berisi angka (8-15 digit).')
            return redirect('kontak')

        # 3. Validasi Struktur Alamat Email
        try:
            validate_email(email)
            if '.' not in email.split('@')[-1]:
                raise ValidationError("Domain tidak lengkap.")
        except ValidationError:
            messages.error(request, 'Alamat email tidak valid. Masukkan email lengkap (contoh: nama@domain.com).')
            return redirect('kontak')

        # 4. Validasi Berlapis Berkas Unggahan (Ekstensi, Ukuran, MIME Type, & Magic Bytes)
        if document_file:
            if not document_file.name.lower().endswith('.pdf') or document_file.content_type != 'application/pdf':
                messages.error(request, 'Format berkas ditolak! Hanya dokumen PDF asli yang diperbolehkan.')
                return redirect('kontak')

            if document_file.size > 2 * 1024 * 1024:
                messages.error(request, 'Ukuran dokumen terlalu besar! Maksimal ukuran berkas adalah 2 MB.')
                return redirect('kontak')

            # Membaca 4 byte pertama untuk memastikan file benar-benar PDF (%PDF), bukan file samaran
            header_bytes = document_file.read(4)
            document_file.seek(0)  # Kembalikan posisi baca file ke awal
            if header_bytes != b'%PDF':
                messages.error(request, 'File terdeteksi rusak atau bukan dokumen PDF yang sah.')
                return redirect('kontak')

        # Simpan ke database dan catat waktu pengiriman di session
        Inquiry.objects.create(
            full_name=full_name,
            organization=organization,
            email=email,
            phone=phone,
            message=message_text,
            document=document_file
        )
        request.session['last_inquiry_submit'] = now
        messages.success(request, 'Permintaan proposal Anda telah berhasil dikirim. Tim kami akan segera menindaklanjuti.')
        return redirect('kontak')

    return render(request, 'contact.html')