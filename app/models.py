from django.db import models

class Branch(models.Model):
    id = models.CharField(max_length=255, primary_key=True, db_index=False)
    university = models.CharField(max_length=255)
    branch = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.university} - {self.branch}"

class Subject(models.Model):
    id = models.CharField(max_length=255, primary_key=True, db_index=False)
    year = models.CharField(max_length=255)
    semester = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=255)
    branches = models.ManyToManyField(Branch,related_name='subjects')

    def __str__(self):
        return self.name

class College(models.Model):
    id = models.CharField(max_length=255, primary_key=True, db_index=False)
    password =models.CharField(max_length=255)
    #from form
    email=models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=255)
    principal=models.CharField(max_length=255)
    mobile = models.CharField(max_length=255)
    role = models.CharField(max_length=255)
    address=models.CharField(max_length=255)
    state=models.CharField(max_length=255)
    city=models.CharField(max_length=255)
    pincode=models.CharField(max_length=255)
    affiliation=models.CharField(max_length=255)
    website=models.CharField(max_length=255)
    image = models.FileField(null=True, blank=True)
    #auto set
    status=models.CharField(max_length=255)
    payment=models.CharField(max_length=255)
    branches = models.ManyToManyField(Branch)

    #17
   
    def __str__(self):
        return self.name

class Student(models.Model):
    id = models.CharField(max_length=255, primary_key=True, db_index=False)
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    PRN = models.CharField(max_length=255, unique=True)
    mobile = models.CharField(max_length=15)
    dob = models.DateField()
    year = models.CharField(max_length=255)
    division=models.CharField(max_length=255)
    semester = models.CharField(max_length=255)
    code = models.CharField(max_length=255)
    address = models.TextField()
    password = models.CharField(max_length=128)  
    image = models.FileField(null=True, blank=True)

    branch = models.ManyToManyField('Branch', blank=True)
    subject = models.ManyToManyField('Subject', blank=True)

    def __str__(self):
        return self.name
class Teacher(models.Model):
    id = models.CharField(max_length=255, primary_key=True, db_index=False)
    name = models.CharField(max_length=255)
    mobile = models.CharField(max_length=15)
    email = models.EmailField(max_length=255, unique=True)
    code = models.CharField(max_length=255)
    qualification = models.CharField(max_length=255)
    experience = models.CharField(max_length=255)
    address = models.TextField()
    password = models.CharField(max_length=128)  # Should be hashed
    image = models.FileField(null=True, blank=True)
    post = models.CharField(max_length=255,blank=True)     # or FileField
    division = models.CharField(max_length=255,blank=True) # or FileField
    
    branch = models.ManyToManyField(Branch, blank=True)
    subject = models.ManyToManyField(Subject, blank=True)
    def __str__(self):
        return self.name if self.name else "Unnamed Teacher"

class Notes(models.Model):
    id = models.CharField(max_length=255, primary_key=True, db_index=False)
   
    year = models.CharField(max_length=255) 
    semester = models.CharField(max_length=255)
    c_code=models.CharField(max_length=255)
    unit =  models.CharField(max_length=255)
    subpoint= models.CharField(max_length=255)
    date = models.DateField()
    file = models.FileField()

    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    branch_id  =models.CharField(max_length=255) 
    def __str__(self):
        return self.id
   
class video(models.Model):
    university = models.CharField(max_length=255)  
    branch = models.CharField(max_length=255)  
    v_subject = models.CharField(max_length=255)  
    v_title = models.CharField(max_length=255)
    v_unit = models.CharField(max_length=255)
    v_subtopic = models.CharField(max_length=255)
    v_description= models.CharField(max_length=255)
    video_data = models.BinaryField()