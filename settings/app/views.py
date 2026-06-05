import torch
from torchvision import transforms
from .serializers import *
from .models import UserProfile
from rest_framework.permissions import IsAdminUser
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from .serializers import RegisterSerializer, LogoutSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from PIL import Image
from CV.CIFAR10 import Vgg16Logic as CIFAR10Model
from CV.CIFAR100 import VggCIFAR100 as CIFAR100Model
from CV.Smartphones import Vgg16Logic as SmartphonesModel
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

class UserProfileListAPIView(generics.ListAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileListSerializer

    def get_queryset(self):
        return UserProfile.objects.filter(id=self.request.user.id)

class UserProfileDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileDetailSerializer

    def get_queryset(self):
        return UserProfile.objects.filter(id=self.request.user.id)

class UserProfileListAdminAPIView(generics.ListAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileListSerializer
    permission_classes = [IsAdminUser]

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
class RegisterView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            'detail': 'Sign up completed.',
            'avatar': user.avatar,
            'username': user.username,
            'status': user.status,
            'registered_date': user.registered_date
        }, status=status.HTTP_200_OK)

class LoginView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        tokens = get_tokens_for_user(user)
        return Response({
            'detail': 'Sign in completed.',
            **tokens,
        }, status=status.HTTP_200_OK)

class LogoutView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LogoutSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'detail': 'Logout completed.'}, status=status.HTTP_205_RESET_CONTENT)

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

cifar_10_model = CIFAR10Model().to(device)
cifar_10_model.load_state_dict(torch.load(BASE_DIR / 'pth_models' / 'cifar_10_model.pth', map_location=device))
cifar_10_model.eval()

cifar_10_labels = [
    'airplane', 'automobile', 'bird', 'cat', 'deer', 'dog', 'frog', 'horse', 'ship', 'truck'
]

cifar_10_transform = transforms.Compose([
    transforms.Resize((32, 32)),
    transforms.ToTensor()
])

class CIFAR10APIView(APIView):
    def post(self, request):
        serializer = CIFAR10Serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        image_data = serializer.validated_data['image']
        image = Image.open(image_data).convert('RGB')
        tensor_image = cifar_10_transform(image).unsqueeze(0).to(device)

        with torch.no_grad():
            predict = cifar_10_model(tensor_image)
            predict_index = torch.argmax(predict, dim=1).item()
            return Response({'Prediction': cifar_10_labels[predict_index]}, status=status.HTTP_200_OK)

cifar_100_model = CIFAR100Model().to(device)
cifar_100_model.load_state_dict(torch.load(BASE_DIR / 'pth_models' / 'cifar_100_model.pth', map_location=device))
cifar_100_model.eval()

cifar_100_labels = torch.load(BASE_DIR / 'pth_models' / 'labels' / 'cifar_100_labels.pth')

mean = [0.5071, 0.4867, 0.4408]
std  = [0.2675, 0.2565, 0.2761]

cifar_100_transform = transforms.Compose([
    transforms.Resize((32, 32)),
    transforms.ToTensor(),
    transforms.Normalize(mean, std)
])

class CIFAR100APIView(APIView):
    def post(self, request):
        serializer = CIFAR100Serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        image_data = serializer.validated_data['image']
        image = Image.open(image_data).convert('RGB')
        tensor_image = cifar_100_transform(image).unsqueeze(0).to(device)

        with torch.no_grad():
            predict = cifar_100_model(tensor_image)
            predict_index = torch.argmax(predict, dim=1).item()
            return Response({'Prediction': cifar_100_labels[predict_index]})

smartphones_model = SmartphonesModel().to(device)
smartphones_model.load_state_dict(torch.load(BASE_DIR / 'pth_models' / 'smartphones_model.pth', map_location=device))
smartphones_model.eval()

smartphones_labels = ['Google Pixel', 'Huawei', 'Iphone', 'Samsung', 'Xiaomi']

smartphones_transform = transforms.Compose([
    transforms.Resize((128, 128)),
    transforms.ToTensor(),
    transforms.RandomHorizontalFlip(),
    transforms.RandomRotation(10)
])

class SmartphonesAPIView(APIView):
    def post(self, request):
        serializer = SmartphonesSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        image_data = serializer.validated_data['image']
        image = Image.open(image_data).convert('RGB')
        tensor_image = smartphones_transform(image).unsqueeze(0).to(device)

        with torch.no_grad():
            predict = smartphones_model(tensor_image)
            predict_index = torch.argmax(predict, dim=1).item()
            return Response({'Prediction': smartphones_labels[predict_index]})