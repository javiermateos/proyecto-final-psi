import os
from datetime import timedelta

import django
from django.utils import timezone


def main():
    """
    Funcion principal que ejecuta el test.
    """
    from core.models import (Pair, Student, OtherConstraints)
    # Comprueba si existe un usuario con id=1000 e  id=10001
    # y si no existen los crea.
    user_1000 = Student.objects.get_or_create(id=1000)[0]
    user_1001 = Student.objects.get_or_create(id=1001)[0]

    # Crea una pareja con dichos estudiantes
    Pair.objects.get_or_create(student1=user_1000, student2=user_1001)

    # Busca todas las parejas donde user_1000 figure como student1
    query = Pair.objects.filter(student1=user_1000)
    for pair in query:
        print(pair)
        pair.validated = True
        pair.save()

    OtherConstraints.objects.get_or_create(
        selectGroupStartDate=timezone.now() + timedelta(days=1))

    otherConstraint = OtherConstraints.objects.all().first()
    if otherConstraint.selectGroupStartDate < timezone.now():
        print("La fecha 'SelectGroupStartDate': {0} es una fecha en el pasado".
              format(otherConstraint.selectGroupStartDate))
    elif otherConstraint.selectGroupStartDate > timezone.now():
        print("La fecha 'SelectGroupStartDate': {0} es una fecha en el futuro".
              format(otherConstraint.selectGroupStartDate))
    else:
        print("La fecha 'SelectGroupStartDate': {0} es la fecha actual".format(
            otherConstraint.selectGroupStartDate))


if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'labassign.settings')
    django.setup()
    main()
