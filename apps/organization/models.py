from django.db import models
from datetime import  datetime
# Create your models here.


class CityDict(models.Model):
    name = models.CharField(max_length=20, verbose_name=u"城市")
    desc = models.CharField(max_length=200, verbose_name=u"描述")
    add_time = models.DateTimeField(default=datetime.now)

    class Meta:
        verbose_name = u"城市"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class CourseOrg(models.Model):
    name = models.CharField(max_length=50, verbose_name=u"机构名称")
    desc = models.TextField(verbose_name=u"机构描述")
    category = models.CharField(default="pxjg", max_length=20, verbose_name=u"机构类别", choices=(("pxjg", "培训机构"), ("gr", "个人"), ("gx", "高校")))
    click_nums = models.IntegerField(default=0, verbose_name=u"点击数")
    fav_nums = models.IntegerField(default=0, verbose_name=u"收藏数")
    tag = models.CharField(default="全国知名", max_length=10, verbose_name=u"机构标签")
    image = models.ImageField(upload_to="org/%Y/%m", verbose_name=u"logo", max_length=100)
    address = models.CharField(max_length=150, verbose_name=u"机构地址")
    city = models.ForeignKey(CityDict, verbose_name=u"所在城市", on_delete=models.CASCADE)
    add_time = models.DateTimeField(default=datetime.now)
    students = models.IntegerField(default=0, verbose_name=u"学习人数")
    course_nums = models.IntegerField(default=0, verbose_name=u"课程数")


    class Meta:
        verbose_name = u"课程机构"
        verbose_name_plural = verbose_name

    def get_teacher_nums(self):
        # 获取课程机构的教师数量
        return self.teacher_set.all().count()

    def __str__(self):
        return self.name


class Teacher(models.Model):
    org = models.ForeignKey(CourseOrg, verbose_name=u"所属机构", on_delete=models.CASCADE)
    name = models.CharField(max_length=50, verbose_name=u"教师名称")
    work_years = models.IntegerField(default=0, verbose_name=u"工作年限")
    work_company = models.CharField(max_length=50, verbose_name=u"就职公司")
    work_position = models.CharField(max_length=50, verbose_name=u"就职职位")
    points = models.CharField(max_length=50, verbose_name=u"教学特点")
    age = models.IntegerField(default=18, verbose_name="年龄")
    click_nums = models.IntegerField(default=0, verbose_name=u"点击数")
    fav_nums = models.IntegerField(default=0, verbose_name=u"收藏数")
    image = models.ImageField(upload_to="teacher/%Y/%m", verbose_name=u"头像", max_length=100, default="")
    add_time = models.DateTimeField(default=datetime.now)

    class Meta:
        verbose_name = u"教师"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def get_course_num(self):
        return self.course_set.all().count()

