from django.db import models


class Word(models.Model):
    word = models.CharField(
        max_length=254,
        null=False,
        blank=False
    )
    idf = models.DecimalField(
        decimal_places=6,
        max_digits=10,
        verbose_name='Inverse document frequency',
        default=1.0
    )

    def __str__(self):
        return self.word[:30]

    class Meta:
        ordering = ('idf',)
        verbose_name = 'Word'
        verbose_name_plural = 'Words'


class File(models.Model):
    name = models.CharField(
        max_length=254,
        verbose_name='File name',
        null=True
    )
    file = models.FileField(
        upload_to='files/',
        null=False,
        unique=True,
        verbose_name='File'
    )
    uploaded_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Date/time loading'
    )
    words_qty = models.IntegerField(
        default=0
    )
    words_in = models.ManyToManyField(
        Word,
        through='WordFile'
    )

    def __str__(self):
        return self.name[:30]

    def save(self, **kwargs):
        self.name = self.file.name
        return super().save(**kwargs)

    class Meta:
        ordering = ('-uploaded_at',)
        verbose_name = 'File'
        verbose_name_plural = 'Files'


class WordFile(models.Model):
    word = models.ForeignKey(
        Word,
        on_delete=models.CASCADE,
        related_name='files'
    )
    file = models.ForeignKey(
        File,
        on_delete=models.CASCADE,
        related_name='words'
    )
    tf = models.DecimalField(
        decimal_places=6,
        max_digits=10,
        blank=False,
        verbose_name='Term frequency',
        default=1.0
    )
