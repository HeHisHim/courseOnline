from django.urls import path, include
from .views import OrgView, AddUserAskVies, OrgHomeView, OrgCourseView, OrgDescView, OrgTeacherView, AddFavView
from .views import TeacherListView, TeacherDetailView

app_name = '[organization]'

urlpatterns = [
    # 课程首页
    path('list/', OrgView.as_view(), name="org_list"),
    path('add_ask/', AddUserAskVies.as_view(), name="add_ask"),
    path('home/<org_id>/', OrgHomeView.as_view(), name="org_home"),
    path('course/<org_id>/', OrgCourseView.as_view(), name="org_course"),
    path('desc/<org_id>/', OrgDescView.as_view(), name="org_desc"),
    path('teacher/<org_id>/', OrgTeacherView.as_view(), name="org_teacher"),

    # 机构收藏
    path('add_fav/', AddFavView.as_view(), name="add_fav"),

    # 教师列表页
    path('teachers/list/', TeacherListView.as_view(), name="teacher_list"),

    # 教师详情页
    path('teachers/<teacher_id>/', TeacherDetailView.as_view(), name="teacher_detail"),

]