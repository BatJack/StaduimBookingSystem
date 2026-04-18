from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.utils import timezone
from django.http import JsonResponse
from django.views.decorators.http import require_POST, require_GET
from datetime import datetime, timedelta, time
from .models import Court, CourtAvailability, Booking, Profile


def is_admin_user(user):
    try:
        return user.profile.user_type == 'admin'
    except Profile.DoesNotExist:
        return False


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            if is_admin_user(user):
                return redirect('admin_dashboard')
            return redirect('court_list')
        else:
            messages.error(request, '用户名或密码错误')
    return render(request, 'booking/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def court_list(request):
    courts = Court.objects.all()
    today = timezone.now().date()
    return render(request, 'booking/court_list.html', {'courts': courts, 'today': today})


@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(
        user=request.user,
        status='active'
    ).order_by('date', 'start_time')
    return render(request, 'booking/my_bookings.html', {'bookings': bookings})


@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    
    if booking.user != request.user and not is_admin_user(request.user):
        messages.error(request, '您没有权限取消此预约')
        return redirect('my_bookings')
    
    booking.status = 'cancelled'
    booking.save()
    messages.success(request, '预约已取消')
    
    if is_admin_user(request.user):
        return redirect('admin_bookings')
    return redirect('my_bookings')


@login_required
def admin_dashboard(request):
    if not is_admin_user(request.user):
        messages.error(request, '您没有权限访问此页面')
        return redirect('court_list')
    
    courts_count = Court.objects.count()
    bookings_count = Booking.objects.count()
    availabilities_count = CourtAvailability.objects.count()
    
    return render(request, 'booking/admin_dashboard.html', {
        'courts_count': courts_count,
        'bookings_count': bookings_count,
        'availabilities_count': availabilities_count
    })


@login_required
def admin_court_list(request):
    if not is_admin_user(request.user):
        messages.error(request, '您没有权限访问此页面')
        return redirect('court_list')
    
    courts = Court.objects.all()
    return render(request, 'booking/admin_court_list.html', {'courts': courts})


@login_required
def admin_court_add(request):
    if not is_admin_user(request.user):
        messages.error(request, '您没有权限访问此页面')
        return redirect('court_list')
    
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        
        Court.objects.create(name=name, description=description)
        messages.success(request, '场地添加成功')
        return redirect('admin_court_list')
    
    return render(request, 'booking/admin_court_form.html')


@login_required
def admin_court_edit(request, court_id):
    if not is_admin_user(request.user):
        messages.error(request, '您没有权限访问此页面')
        return redirect('court_list')
    
    court = get_object_or_404(Court, id=court_id)
    
    if request.method == 'POST':
        court.name = request.POST.get('name')
        court.description = request.POST.get('description')
        court.save()
        messages.success(request, '场地更新成功')
        return redirect('admin_court_list')
    
    return render(request, 'booking/admin_court_form.html', {'court': court})


@login_required
def admin_court_delete(request, court_id):
    if not is_admin_user(request.user):
        messages.error(request, '您没有权限访问此页面')
        return redirect('court_list')
    
    court = get_object_or_404(Court, id=court_id)
    court.delete()
    messages.success(request, '场地删除成功')
    return redirect('admin_court_list')


@login_required
def admin_availability_list(request):
    if not is_admin_user(request.user):
        messages.error(request, '您没有权限访问此页面')
        return redirect('court_list')
    
    courts = Court.objects.all()
    today = timezone.now().date()
    
    availabilities = CourtAvailability.objects.filter(
        end_date__gte=today
    ).select_related('court').order_by('start_date', 'start_time')
    
    return render(request, 'booking/admin_availability_list.html', {
        'availabilities': availabilities,
        'courts': courts,
    })


@login_required
def admin_availability_add(request):
    if not is_admin_user(request.user):
        messages.error(request, '您没有权限访问此页面')
        return redirect('court_list')
    
    if request.method == 'POST':
        court_id = request.POST.get('court')
        start_date_str = request.POST.get('start_date')
        end_date_str = request.POST.get('end_date')
        start_time_str = request.POST.get('start_time')
        end_time_str = request.POST.get('end_time')
        
        try:
            court = Court.objects.get(id=court_id)
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
            start_time = datetime.strptime(start_time_str, '%H:%M').time()
            end_time = datetime.strptime(end_time_str, '%H:%M').time()
            
            if start_date > end_date:
                messages.error(request, '结束日期必须大于等于开始日期')
                return render(request, 'booking/admin_availability_form.html', {
                    'courts': Court.objects.all(),
                })
            
            if start_time >= end_time:
                messages.error(request, '结束时间必须大于开始时间')
                return render(request, 'booking/admin_availability_form.html', {
                    'courts': Court.objects.all(),
                })
            
            CourtAvailability.objects.create(
                court=court,
                start_date=start_date,
                end_date=end_date,
                start_time=start_time,
                end_time=end_time
            )
            
            messages.success(request, '可用时间段设置成功')
            return redirect('admin_availability_list')
            
        except ValueError:
            messages.error(request, '时间格式错误')
        except Court.DoesNotExist:
            messages.error(request, '场地不存在')
    
    return render(request, 'booking/admin_availability_form.html', {
        'courts': Court.objects.all(),
    })


@login_required
def admin_bookings(request):
    if not is_admin_user(request.user):
        messages.error(request, '您没有权限访问此页面')
        return redirect('court_list')
    
    bookings = Booking.objects.all().select_related('user', 'court').order_by('date', 'start_time')
    return render(request, 'booking/admin_bookings.html', {'bookings': bookings})


@login_required
def admin_booking_add(request):
    if not is_admin_user(request.user):
        messages.error(request, '您没有权限访问此页面')
        return redirect('court_list')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        court_id = request.POST.get('court')
        date_str = request.POST.get('date')
        start_time_str = request.POST.get('start_time')
        end_time_str = request.POST.get('end_time')
        
        try:
            user = User.objects.get(username=username)
            court = Court.objects.get(id=court_id)
            booking_date = datetime.strptime(date_str, '%Y-%m-%d').date()
            start_time = datetime.strptime(start_time_str, '%H:%M').time()
            end_time = datetime.strptime(end_time_str, '%H:%M').time()
            
            if start_time >= end_time:
                messages.error(request, '结束时间必须大于开始时间')
                return render(request, 'booking/admin_booking_form.html', {
                    'courts': Court.objects.all(),
                    'users': User.objects.all(),
                })
            
            if start_time.minute not in [0, 30] or end_time.minute not in [0, 30]:
                messages.error(request, '时间必须是整点或半点')
                return render(request, 'booking/admin_booking_form.html', {
                    'courts': Court.objects.all(),
                    'users': User.objects.all(),
                })
            
            availability = CourtAvailability.objects.filter(
                court=court,
                start_date__lte=booking_date,
                end_date__gte=booking_date
            ).first()
            
            if not availability:
                messages.error(request, '该日期场地未开放')
                return render(request, 'booking/admin_booking_form.html', {
                    'courts': Court.objects.all(),
                    'users': User.objects.all(),
                })
            
            if start_time < availability.start_time or end_time > availability.end_time:
                messages.error(request, '预约时间不在场地开放时间内')
                return render(request, 'booking/admin_booking_form.html', {
                    'courts': Court.objects.all(),
                    'users': User.objects.all(),
                })
            
            conflicting_bookings = Booking.objects.filter(
                court=court,
                date=booking_date,
                status='active'
            ).exclude(
                end_time__lte=start_time
            ).exclude(
                start_time__gte=end_time
            )
            
            if conflicting_bookings.exists():
                messages.error(request, '该时间段已被预约')
                return render(request, 'booking/admin_booking_form.html', {
                    'courts': Court.objects.all(),
                    'users': User.objects.all(),
                })
            
            Booking.objects.create(
                user=user,
                court=court,
                date=booking_date,
                start_time=start_time,
                end_time=end_time,
                status='active'
            )
            
            messages.success(request, '预约添加成功')
            return redirect('admin_bookings')
            
        except User.DoesNotExist:
            messages.error(request, '用户不存在')
        except Court.DoesNotExist:
            messages.error(request, '场地不存在')
        except ValueError:
            messages.error(request, '时间格式错误')
    
    return render(request, 'booking/admin_booking_form.html', {
        'courts': Court.objects.all(),
        'users': User.objects.all(),
    })


@login_required
@require_GET
def get_time_slots(request):
    date_str = request.GET.get('date')
    court_id = request.GET.get('court_id')

    if not date_str:
        return JsonResponse({'error': '缺少日期参数'}, status=400)

    try:
        selected_date = datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        return JsonResponse({'error': '日期格式错误'}, status=400)

    courts = Court.objects.all()
    if court_id:
        courts = courts.filter(id=court_id)
    data = []
    
    for court in courts:
        availability = CourtAvailability.objects.filter(
            court=court,
            start_date__lte=selected_date,
            end_date__gte=selected_date
        ).first()
        
        court_data = {
            'id': court.id,
            'name': court.name,
            'description': court.description,
            'is_available': availability is not None,
            'start_time': availability.start_time.strftime('%H:%M') if availability else None,
            'end_time': availability.end_time.strftime('%H:%M') if availability else None,
            'time_slots': []
        }
        
        if availability:
            bookings = Booking.objects.filter(
                court=court,
                date=selected_date,
                status='active'
            ).values_list('start_time', 'end_time')
            
            booked_slots = set()
            for start, end in bookings:
                current = datetime.combine(selected_date, start)
                end_dt = datetime.combine(selected_date, end)
                while current < end_dt:
                    booked_slots.add(current.time())
                    current += timedelta(minutes=30)
            
            current_time = datetime.combine(selected_date, availability.start_time)
            end_time_dt = datetime.combine(selected_date, availability.end_time)
            
            while current_time < end_time_dt:
                slot_time = current_time.time()
                slot_end = (current_time + timedelta(minutes=30)).time()
                
                is_booked = slot_time in booked_slots
                
                court_data['time_slots'].append({
                    'start': slot_time.strftime('%H:%M'),
                    'end': slot_end.strftime('%H:%M'),
                    'label': f"{slot_time.strftime('%H:%M')}-{slot_end.strftime('%H:%M')}",
                    'is_booked': is_booked
                })
                
                current_time += timedelta(minutes=30)
        
        data.append(court_data)
    
    return JsonResponse({'courts': data})


@login_required
@require_POST
def create_booking_api(request):
    import json
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': '无效的请求数据'}, status=400)
    
    court_id = data.get('court_id')
    date_str = data.get('date')
    start_time_str = data.get('start_time')
    end_time_str = data.get('end_time')
    
    if not all([court_id, date_str, start_time_str, end_time_str]):
        return JsonResponse({'error': '缺少必要参数'}, status=400)
    
    try:
        court = Court.objects.get(id=court_id)
        booking_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        start_time = datetime.strptime(start_time_str, '%H:%M').time()
        end_time = datetime.strptime(end_time_str, '%H:%M').time()
    except (Court.DoesNotExist, ValueError):
        return JsonResponse({'error': '参数错误'}, status=400)
    
    if start_time >= end_time:
        return JsonResponse({'error': '结束时间必须大于开始时间'}, status=400)
    
    availability = CourtAvailability.objects.filter(
        court=court,
        start_date__lte=booking_date,
        end_date__gte=booking_date
    ).first()
    
    if not availability:
        return JsonResponse({'error': '该日期场地未开放'}, status=400)
    
    if start_time < availability.start_time or end_time > availability.end_time:
        return JsonResponse({'error': '预约时间不在场地开放时间内'}, status=400)
    
    conflicting_bookings = Booking.objects.filter(
        court=court,
        date=booking_date,
        status='active'
    ).exclude(
        end_time__lte=start_time
    ).exclude(
        start_time__gte=end_time
    )
    
    if conflicting_bookings.exists():
        return JsonResponse({'error': '该时间段已被预约'}, status=400)
    
    Booking.objects.create(
        user=request.user,
        court=court,
        date=booking_date,
        start_time=start_time,
        end_time=end_time,
        status='active'
    )
    
    return JsonResponse({'success': True, 'message': '预约成功'})
