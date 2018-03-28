from django.shortcuts import render
from django.views.generic import View
from django.shortcuts import render_to_response
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import CourseOrg, CityDict, Teacher
from .forms import UserAskForm
from operation.models import UserFavorite
from courses.models import Course
# Create your views here.


class OrgView(View):
    """课程列表功能"""
    def get(self, request):

        # 课程机构
        all_orgs = CourseOrg.objects.all()
        # 城市
        all_citys = CityDict.objects.all()
        # 取出筛选城市
        # city_id = request.GET.get("city", "")
        # if city_id:
        #     all_orgs = all_orgs.filter(city_id=int(city_id))

        city_name = request.GET.get("city", "")
        if city_name:
            # print(city_name)
            for all_city in all_citys:
                if str(all_city) == str(city_name):
                    all_orgs = all_orgs.filter(city_id=all_city.id)


        # 类别筛选
        category = request.GET.get('ct', "")
        if category:
            all_orgs = all_orgs.filter(category=category)

        sort = request.GET.get("sort", "")
        if sort:
            if sort == "students":
                all_orgs = all_orgs.order_by("-students")
            elif sort == "courses":
                all_orgs = all_orgs.order_by("-course_nums")

        # 课程搜索
        search_keywords = request.GET.get('keywords', "")
        if search_keywords:
            all_orgs = all_orgs.filter(
                Q(name__icontains=search_keywords) |
                Q(desc__icontains=search_keywords)
            )
        # 数量统计
        org_nums = all_orgs.count()

        # 热门机构排序(倒序)
        hot_orgs = all_orgs.order_by("-click_nums")[:3]
        # 对课程机构进行分页面
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        # Provide Paginator with the request object for complete querystring generation

        p = Paginator(all_orgs, 2, request=request)

        orgs = p.page(page)
        return render(request, "org-list.html", {
            "all_orgs": orgs,
            "all_citys": all_citys,
            "org_nums": org_nums,
            "city_name": city_name,
            "category": category,
            "hot_orgs": hot_orgs,
            "sort": sort,
        })


class AddUserAskVies(View):
    """
    用户添加咨询
    """
    def post(self, request):
        userask_form = UserAskForm(request.POST)
        if userask_form.is_valid():
            user_ask = userask_form.save(commit=True)

            # return HttpResponse("{'status':'success'}", content_type='application/json')
            # return HttpResponseRedirect(reverse("{'status':'success'}", content_type='application/json'))
            return JsonResponse({'status': 'success'})

        else:
            # return HttpResponse("{'status':'fail', 'msg':'添加出错'}", content_type='application/json')
            # return HttpResponseRedirect(reverse("{'status':'fail', 'msg':'添加出错'}", content_type='application/json'))
            return JsonResponse({'status': 'fail', 'msg': '添加出错'})


class OrgHomeView(View):
    """机构首页"""
    def get(self, request, org_id):
        current_page = "home"
        course_org = CourseOrg.objects.get(id=int(org_id))
        course_org.click_nums += 1
        course_org.save()

        # --判断用户是否已经收藏
        has_fav = has_favorite(request, course_org, 2)
        # 判断用户是否已经收藏--

        all_courses = course_org.course_set.all()[:3]
        all_teachers = course_org.teacher_set.all()[:1]

        return render(request, 'org-detail-homepage.html', {
            "all_courses": all_courses,
            "all_teachers": all_teachers,
            "course_org": course_org,
            "current_page": current_page,
            "has_fav": has_fav,
        })


class OrgCourseView(View):
    """机构课程列表页"""
    def get(self, request, org_id):
        current_page = "course"
        course_org = CourseOrg.objects.get(id=int(org_id))
        all_courses = course_org.course_set.all()

        # --判断用户是否已经收藏
        has_fav = has_favorite(request, course_org, 2)
        # 判断用户是否已经收藏--

        return render(request, 'org-detail-course.html', {
            "all_courses": all_courses,
            "course_org": course_org,
            "current_page": current_page,
            "has_fav": has_fav,
        })


class OrgDescView(View):
    """机构介绍页"""
    def get(self, request, org_id):
        current_page = "desc"
        course_org = CourseOrg.objects.get(id=int(org_id))

        # --判断用户是否已经收藏
        has_fav = has_favorite(request, course_org, 2)
        # 判断用户是否已经收藏--

        return render(request, 'org-detail-desc.html', {
            "course_org": course_org,
            "current_page": current_page,
            "has_fav": has_fav,
        })


class OrgTeacherView(View):
    """机构教师页"""
    def get(self, request, org_id):
        current_page = "teacher"
        course_org = CourseOrg.objects.get(id=int(org_id))
        all_teachers = course_org.teacher_set.all()

        # --判断用户是否已经收藏
        has_fav = has_favorite(request, course_org, 2)
        # 判断用户是否已经收藏--

        return render(request, 'org-detail-teachers.html', {
            "all_teachers": all_teachers,
            "course_org": course_org,
            "current_page": current_page,
            "has_fav": has_fav,
        })


class AddFavView(View):
    """用户收藏， 用户取消收藏"""

    def post(self, request):
        fav_id = request.POST.get("fav_id", 0)
        fav_type = request.POST.get("fav_type", 0)

        if not request.user.is_authenticated:
            # 判断用户登录状态
            return JsonResponse({'status': 'fail', 'msg': '用户未登录'})

        exist_records = UserFavorite.objects.filter(user=request.user, fav_id=int(fav_id), fav_type=int(fav_type))
        if exist_records:
            # 如果记录已经存在，则表示用户取消收藏
            exist_records.delete()
            if int(fav_type) == 1:
                course = Course.objects.get(id=int(fav_id))
                course.fav_nums -= 1
                if course.fav_nums < 0:
                    course.fav_nums = 0
                course.save()
            elif int(fav_type == 2):
                course_org = CourseOrg.objects.get(id=int(fav_id))
                course_org.fav_nums -= 1
                if course_org.fav_nums < 0:
                    course_org.fav_nums = 0
                course_org.save()
            elif int(fav_type == 3):
                teacher = Teacher.objects.get(id=int(fav_id))
                teacher.click_nums -= 1
                if teacher.fav_nums < 0:
                    teacher.fav_nums = 0
                teacher.save()

            return JsonResponse({'status': 'success', 'msg': '收藏'})

        else:
            user_fav = UserFavorite()
            if int(fav_id) > 0 and int(fav_type) > 0:
                user_fav.user = request.user
                user_fav.fav_id = int(fav_id)
                user_fav.fav_type = int(fav_type)
                user_fav.save()

                if int(fav_type) == 1:
                    course = Course.objects.get(id=int(fav_id))
                    course.fav_nums += 1
                    course.save()
                elif int(fav_type == 2):
                    course_org = CourseOrg.objects.get(id=int(fav_id))
                    course_org.fav_nums += 1
                    course_org.save()
                elif int(fav_type == 3):
                    teacher = Teacher.objects.get(id=int(fav_id))
                    teacher.click_nums += 1
                    teacher.save()

                return JsonResponse({'status': 'success', 'msg': '已收藏'})

            else:
                return JsonResponse({'status': 'fail', 'msg': '收藏出错'})


class TeacherListView(View):
    """教师列表页"""
    def get(self, request):
        all_teachers = Teacher.objects.all()

        # 课程搜索
        search_keywords = request.GET.get('keywords', "")
        if search_keywords:
            all_teachers = all_teachers.filter(
                Q(name__icontains=search_keywords) |
                Q(work_company__icontains=search_keywords) |
                Q(work_position__icontains=search_keywords)
            )

        teacher_nums = all_teachers.count()

        sort = request.GET.get("sort", "")
        if sort:
            if sort == "hot":
                all_teachers = all_teachers.order_by("-click_nums")

        sorted_teacher = Teacher.objects.all().order_by("-click_nums")[:3]
        # 对教师进行分页面
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        # Provide Paginator with the request object for complete querystring generation

        p = Paginator(all_teachers, 1, request=request)

        teachers = p.page(page)

        return render(request, "teachers-list.html", {
            "all_teachers": teachers,
            "sorted_teacher": sorted_teacher,
            "sort": sort,
            "teacher_nums": teacher_nums,
        })


class TeacherDetailView(View):
    def get(self, request, teacher_id):
        teacher = Teacher.objects.get(id=int(teacher_id))
        all_coursers = Course.objects.filter(teacher=teacher)
        teacher.click_nums += 1
        teacher.save()

        #排行
        sorted_teacher = Teacher.objects.all().order_by("-click_nums")[:3]

        has_teacher_faved = False
        if UserFavorite.objects.filter(user=request.user, fav_type=3, fav_id=teacher_id):
            has_teacher_faved = True

        has_org_faved = False
        if UserFavorite.objects.filter(user=request.user, fav_type=2, fav_id=teacher.org.id):
            has_org_faved = True

        return render(request, "teacher-detail.html", {
            "teacher": teacher,
            "all_coursers": all_coursers,
            "sorted_teacher": sorted_teacher,
            "has_teacher_faved": has_teacher_faved,
            "has_org_faved": has_org_faved,
        })


def has_favorite(request, course_org, fav_type):
    has_fav = False
    if request.user.is_authenticated:
        if UserFavorite.objects.filter(user=request.user, fav_id=int(course_org.id), fav_type=fav_type):
            has_fav = True

    return has_fav