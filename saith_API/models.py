from django.db import models

class Users(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=254, blank=False, null=False)
    password = models.CharField(max_length=254, blank=False, null=False)
    email = models.EmailField(unique=True, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        default_related_name = 'users'

class Sessions(models.Model):
    id = models.AutoField(primary_key=True)
    token = models.CharField(max_length=254, blank=False, null=False)
    user = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='sessions')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        default_related_name = 'sessions'

class Document(models.Model):
    id = models.AutoField(primary_key=True)
    document = models.CharField(max_length=14, blank=False, null=False)
    last_ncu = models.CharField(max_length=254, default='0')
    last_batch = models.CharField(max_length=254, default='1')
    last_request_nfe = models.DateTimeField()

    class Meta:
        default_related_name = 'document'
class Certificate(models.Model):
    id = models.AutoField(primary_key=True)
    certificate = models.BinaryField(null=False)
    uf = models.CharField(max_length=2, blank=False, null=False)
    code = models.CharField(max_length=30, blank=False, null=False)
    password = models.CharField(max_length=254, blank=False, null=False)
    expiration = models.DateTimeField(null=False)
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    is_valid = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        default_related_name = 'certificate'
    

    
class User_Certificate_Document(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    certificate = models.ForeignKey(Certificate, on_delete=models.CASCADE)
    document = models.ForeignKey(Document, on_delete=models.CASCADE)

    class Meta:
        default_related_name = 'user_certificate_document'
    
class User_Document_Valid(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    is_valid = models.BooleanField(default=False)

    class Meta:
        default_related_name = 'user_document_valid'

class NFE(models.Model):
    id = models.AutoField(primary_key=True)
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    nsu = models.CharField(max_length=254, blank=False, null=False)
    document_seller = models.CharField(max_length=14, blank=False, null=False)
    seller = models.CharField(max_length=254, blank=False, null=False)
    number = models.CharField(max_length=254, blank=False, null=False)
    value_nfe = models.FloatField(null=False)
    date = models.DateTimeField(null=False)
    has_nfe_complete = models.BooleanField(default=False)
    nfe = models.BinaryField()
    answered = models.BooleanField(default=False)
    operation_science = models.BooleanField(default=False)
    operation_science_date = models.DateTimeField()
    answer = models.CharField(max_length=254)
    class Meta:
        default_related_name = 'nfe'
