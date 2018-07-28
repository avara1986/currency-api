# -*- coding: utf-8 -*-
"""
========
Managers
========
"""
from django.db import models


class SelectRelatedManager(models.Manager):

    def get_queryset(self):
        # Esta línea se ejecuta siempre pero en los test no entra por alguna razón....
        return super(SelectRelatedManager, self).get_queryset().select_related()  # pragma: no cover