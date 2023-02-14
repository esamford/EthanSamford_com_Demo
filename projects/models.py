import datetime
import os.path

from django.db import models
from django.forms import forms


class Technology(models.Model):
    CONST_TYPES = (
        # The first value appears in the database, while the second appears online.
        ("Programming language", "Programming language"),
        ("Library/framework", "Library/framework"),
        ("Database", "Database"),
        ("Cloud computing service", "Cloud computing service"),
        ("Other", "Other"),
    )
    name = models.CharField(max_length=50, unique=True)
    type = models.CharField(max_length=50, choices=CONST_TYPES)

    def clean(self):
        for existing_tech in Technology.objects.all():
            if self.id == existing_tech.id:
                continue
            if self.name.lower() == existing_tech.name.lower():
                raise forms.ValidationError("That technology already exists.")

    def __str__(self):
        return str(self.name)


class Project(models.Model):
    def get_upload_path(self, filename):
        extension = os.path.splitext(filename)[1].strip('.')
        return "static/uploaded_files/project_background_images/{}.{}".format(
            str(self.name).replace(" ", "_"), extension.lower()
        )

    name = models.CharField(max_length=200)
    start_date = models.DateField()
    end_date = models.DateField()
    short_description = models.TextField(max_length=200)
    page_description = models.TextField()
    make_public = models.BooleanField(default=True)
    tools_used = models.ManyToManyField(Technology)
    background_image = models.ImageField(upload_to=get_upload_path, blank=True)

    def save(self, *args, **kwargs):
        # On file change, delete the old image to save space on the server.
        instance = Project.objects.filter(id=self.id).first()
        if instance is not None and instance.background_image != self.background_image:
            try:
                if os.path.exists(instance.background_image.path):
                    os.remove(instance.background_image.path)
            except ValueError:
                # Skip over "The '____' attribute has no file associated with it" error.
                # This happens because the attribute used to not exist until after a migration.
                pass
        super(Project, self).save(*args, **kwargs)

    def get_technologies(self):
        return Technology.objects.filter(project__id=self.id).order_by('name')

    def get_project_images(self):
        return ProjectImage.objects.filter(project__id=self.id).order_by('display_order')

    def clean(self):
        super().clean()
        if self.start_date > self.end_date:
            raise forms.ValidationError("The start date cannot be after the end date.")

    def __str__(self):
        return str(self.name)

    @staticmethod
    def __date_as_month(date: datetime.date):
        return date.strftime("%b. %Y")

    def start_date_as_month(self):
        return self.__date_as_month(self.start_date)

    def end_date_as_month(self):
        return self.__date_as_month(self.end_date)

    @staticmethod
    def __split_paragraphs(text: str):
        paragraphs = [x for x in str(text).split('\n') if len(x) > 0]
        return paragraphs

    def page_description_paragraphs(self):
        return self.__split_paragraphs(str(self.page_description))


class ProjectImage(models.Model):
    def get_upload_path(self, filename):
        extension = os.path.splitext(filename)[1].strip('.')
        return "static/uploaded_files/project_images/{}/{}.{}".format(
            self.project.name, str(self.name).replace(" ", "_"), extension.lower()
        )

    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    upload_time = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to=get_upload_path)
    display_order = models.PositiveIntegerField(
        default=0, help_text="Lower values will be shown before higher values."
    )
    show = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        # On file change, delete the old image to save space on the server.
        instance = ProjectImage.objects.filter(id=self.id).first()
        if instance is not None and instance.image != self.image:
            if os.path.exists(instance.image.path):
                os.remove(instance.image.path)
        super(ProjectImage, self).save(*args, **kwargs)

    def __str__(self):
        return "{} - {}".format(self.project, self.name)
