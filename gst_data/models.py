from django.db import models


class OnboardedGSTIN(models.Model):
    gstin = models.CharField(max_length=15, unique=True)
    trade_name = models.CharField(max_length=255)
    legal_name = models.CharField(max_length=255)
    state = models.CharField(max_length=100)
    admin_email = models.EmailField(default='')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.gstin} - {self.trade_name}"


class GSTINFilingStatus(models.Model):
    class ReturnType(models.TextChoices):
        GSTR1 = 'GSTR1', 'GSTR-1'
        GSTR3B = 'GSTR3B', 'GSTR-3B'
        GSTR9 = 'GSTR9', 'GSTR-9'

    class Status(models.TextChoices):
        FILED = 'Filed', 'Filed'
        NOT_FILED = 'Not Filed', 'Not Filed'
        PENDING = 'Pending', 'Pending'

    gstin = models.ForeignKey(OnboardedGSTIN, on_delete=models.CASCADE, related_name='filing_statuses')
    return_type = models.CharField(max_length=10, choices=ReturnType.choices)
    period = models.CharField(max_length=10)  # e.g. "Jan-2026"
    status = models.CharField(max_length=10, choices=Status.choices)
    filed_date = models.DateField(null=True, blank=True)
    due_date = models.DateField()

    class Meta:
        unique_together = ('gstin', 'return_type', 'period')

    def __str__(self):
        return f"{self.gstin.gstin} | {self.return_type} | {self.period} | {self.status}"
