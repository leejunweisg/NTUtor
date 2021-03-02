from django.db import models
from users.models import Profile

class Module(models.Model):
    #Django cannot have composite primary keys, thus, using auto increment for pri key
    moduleID = models.AutoField(primary_key = True)

    #If school is deleted, then module is also deleted
    moduleCode = models.CharField(max_length=20, unique=True)
    moduleName = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.moduleCode}: {self.moduleName}"

class Listing(models.Model):
    listingID = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50)
    description = models.TextField()

    # Will automatically fill in date when listing created
    datePosted = models.DateTimeField(auto_now_add=True)

    # If module code does not exist, do not delete listing, but set the code to null
    module = models.ForeignKey(Module, on_delete=models.SET_NULL, null=True)

    # Get user from profile, if profile is deleted, the listings will also be deleted
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    
    # Either Tutor or Tutee
    typeOfStudent = models.CharField(max_length=10)

    # Once tutor wants to stop teaching, can close tuition listing
    closed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.listingID}: {self.title}"


class TuitionSession(models.Model):
    tuitionSessionID = models.AutoField(primary_key = True)
    tutor = models.ForeignKey(Profile, on_delete=models.SET_NULL, related_name="tutor", null=True)
    learner = models.ForeignKey(Profile, on_delete=models.SET_NULL, related_name="learner", null=True)

    # When listing deleted, user can still leave review on the tutor, thus dont delete session
    listing = models.ForeignKey(Listing, on_delete=models.SET_NULL, null=True)

    # Once complete
    completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.tuitionSessionID}"
