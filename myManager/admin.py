from django.contrib import admin

from .models import Citoyen
from .models import Marriage
from .models import Temoin
from .models import Naissanse
from .models import Deces
from .models import Officier
from .models import BeureuEtatciv
from .models import Commune
from .models import Daira
from .models import Willaya
from .models import Pays
from .models import Registre_naissance
from .models import Registre_marriage
from .models import Registre_deces

# Register your models here.

admin.site.register(Citoyen)
admin.site.register(Marriage)
admin.site.register(Temoin)
admin.site.register(Naissanse)
admin.site.register(Deces)
admin.site.register(Officier)
admin.site.register(BeureuEtatciv)
admin.site.register(Commune)
admin.site.register(Daira)
admin.site.register(Willaya)
admin.site.register(Pays)
admin.site.register(Registre_naissance)
admin.site.register(Registre_marriage)
admin.site.register(Registre_deces)
