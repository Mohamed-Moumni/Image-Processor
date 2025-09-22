from rest_framework.views import APIView

class ImageListView(APIView):
    def post(self, request):
        print("HERE --------------------------------------- HERE")

        for elem in request:
            print(elem)