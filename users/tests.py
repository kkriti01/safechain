import base64
import json
from rest_framework.test import APITestCase
from rest_framework import status

from users import models


class UserViewsTestCase(APITestCase):

    def setUp(self):
        # Create a test instance
        self.user_data = {
                     "username": "kriti",
                     "email": "kriti@123.com",
                     "password1": "asdf12345@12",
                     "password2": "asdf12345@12",
                     "first_name": "kriti",
                     "last_name": "kumari",
                     "is_staff": True
                   }

        self.user = models.User.objects.create(username="kriti01",
                                               email="kriti@1234.com",
                                               first_name="kriti",
                                               last_name="kumari",
                                               is_staff=True
                                               )

    def test_create_user(self):
        """
        Test User registration
        """
        response = self.client.post('/api/v1/user/signup/', self.user_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_list_set(self):
        """
        Test User listing api
        """

        response = self.client.get("/api/v1/users/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content)[0]["first_name"], self.user_data.get("first_name"))

    def test_update_user(self):
        """
        Test user update api
        :return:
        """
        self.client.force_authenticate(user=self.user)
        self.user_data.update({"first_name": "abc"})
        response = self.client.put('/api/v1/users/'+str(self.user.id)+"/", self.user_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content)["first_name"], self.user_data.get("first_name"))

    def test_user_profile(self):
        """
        List user profiles
        :return:
        """
        response = self.client.get('/api/v1/list_profiles/'+str(self.user.id)+"/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content)[0]["user"], self.user.id)

    def test_show_pdf(self):
        response = self.client.get('/api/v1/show_pdf/'+str(self.user.id)+"/")
        response = json.loads(response.content.decode("utf-8"))

        self.assertEqual(response["message"], 'ok')
        self.assertEqual(json.loads(base64.b64decode(response["user"]))["email"], self.user.email)
        self.assertEqual(json.loads(base64.b64decode(response["user"]))["username"], self.user.username)

    def test_delete_user(self):
        """
        Test User delete
        :return:
        """
        self.client.force_authenticate(user=self.user)
        response = self.client.delete("/api/v1/users/"+str(self.user.id)+"/")

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

