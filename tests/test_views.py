import pytest
from rest_framework import status
from django.urls import reverse
from Telephone.factory import *


@pytest.mark.django_db
@pytest.mark.parametrize(
        "url_name, method, payload, expected_status", [
            ("account-list",  "GET", None, status.HTTP_200_OK),
            ("phone-list", "POST", {"type_phone": "samsung"}, status.HTTP_400_BAD_REQUEST),
        ]
        )

def test_telmart_api_endpoints(api, unique_user, url_name, method, payload, expected_status):
    api.force_authenticate(user=unique_user)
        
    url = reverse(url_name)

    if method == "GET":
        response = api.get(url)

    elif method == "POST":
        response = api.post(url, data=payload, format='json')
    assert response.status_code == expected_status


# GET && POST 

# class Account GET {متاح للمسجلين حساب الوصول لحساب معين} / 200 ok,
#  POST {ودخول لبتقي الكلاسات   غير متاح لشخص غير المسجل أنشاء فيه}  / UnAUth 403

# class Phone GET {متاح للمسجلين رؤية عرض الهاتف} / 200 ok,
#  POST { متاح لشخص أنشاء مواصفات} / Bad 400

# class Specs GET {متاح للمسجلين رؤية المواصفات} / 
# 200 ok, POST {متاح لشخص أنشاء} / Bad 400 

# class Voucher GET {متاح فقط للبائع والمشتري} / 200 ok,
#  POST {أنشاء من خلال طرفين عقد البيع} / 201 created


