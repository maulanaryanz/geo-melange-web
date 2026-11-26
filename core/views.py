from django.shortcuts import render, redirect
from django.contrib import messages
from .models import BidangLayanan, portofolio, Inquiry


def home(request):
    projects = portofolio.objects.select_related('category').all().order_by('-year', 'id')[:3]
    return render(request, 'index.html', {
        'featured_projects': projects,
        'portofolios': projects,
    })


def profile_view(request):
    return render(request, 'profile.html')


def portofolio_view(request):
    selected_category = request.GET.get('category', '')
    projects = portofolio.objects.select_related('category').all().order_by('-year', 'id')

    if selected_category:
        projects = projects.filter(category__name=selected_category)

    categories = BidangLayanan.objects.values_list('name', flat=True)

    return render(request, 'portofolio.html', {
        'projects': projects,
        'categories': categories,
        'selected_category': selected_category,
    })


def contact_view(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name', '').strip()
        organization = request.POST.get('organization', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        message = request.POST.get('message', '').strip()
        document = request.FILES.get('document')

        if full_name and email and phone and message:
            Inquiry.objects.create(
                full_name=full_name,
                organization=organization,
                email=email,
                phone=phone,
                message=message,
                document=document,
            )
            messages.success(
                request,
                'Terima kasih! Pesan dan proposal Anda telah berhasil dikirim. Tim CV. Geo Melange akan segera menghubungi Anda.'
            )
            return redirect('kontak')
        else:
            messages.error(request, 'Harap lengkapi seluruh kolom wajib sebelum mengirim pesan.')

    return render(request, 'contact.html')


# Alias cadangan jika core/urls.py memanggil nama tanpa akhiran _view
profil = profile_view
kontak = contact_view