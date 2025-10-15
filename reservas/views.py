from .serializer import CasaSerializer, AluguelSerializer
from .models import Casa, Aluguel

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated


class CasaListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        casa = Casa.objects.filter(dono=request.user)
        serializer = CasaSerializer(casa, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class CasaDetailAPIView(APIView):
    def get(self, request, pk):
        try:
            casa = Casa.objects.get(pk=pk, dono=self.request.user)
            serializer = CasaSerializer(casa)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Casa.DoesNotExist:
            return Response({"error":"Esta casa não pertence a você."}, status=status.HTTP_403_FORBIDDEN)

class CasaCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            serializer = CasaSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(dono=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Casa.DoesNotExist:
            return Response({"error":"Não é possível criar uma casa nova"},status=status.HTTP_403_FORBIDDEN)

class CasaUpdateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, pk):
        try:
            casa = Casa.objects.get(pk=pk, dono=self.request.user)
            serializer = CasaSerializer(instance=casa, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Casa.DoesNotExist:
            return Response({"error":"Não é possivel modificar uma casa que não é sua"}, status=status.HTTP_403_FORBIDDEN)


class CasaDestroyAPIView(APIView):
    permission_classes=[IsAuthenticated]

    def delete(self, request, pk):
        try:
            casa = Casa.objects.get(pk=pk, dono=self.request.user)
            casa.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Casa.DoesNotExist:
            return Response({"error":"Não é possivel excluir uma casa que não é sua."}, status=status.HTTP_401_UNAUTHORIZED)
    


class AluguelListAPIView(APIView):
    permission_classes=[IsAuthenticated]

    def get(self, request, pk=None):
        if pk:
            try:
                aluguel = Aluguel.objects.get(pk=pk, hospede=request.user)
                serializer = AluguelSerializer(aluguel)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Aluguel.DoesNotExist:
                return Response({"error":"Esse imovel não esta alugado em seu nome"}, status=status.HTTP_403_FORBIDDEN)
        else:
            alugueis = Aluguel.objects.filter(hospede=request.user)
            serializer = AluguelSerializer(alugueis, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
            

class AluguelCreateAPIView(APIView):

    permission_classes=[IsAuthenticated]

    def post(self, request):
        serializer = AluguelSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(hospede=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class AluguelUpdateAPIView(APIView):
    
    permission_classes = [IsAuthenticated]

    def put(self, request, pk):
        try:
            aluguel = Aluguel.objects.get(pk=pk, hospede=request.user)
            serializer = AluguelSerializer(aluguel, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Aluguel.DoesNotExist:
            return Response({"error":"você não pode atualizar o que não esta alocado a você."},
                            status=status.HTTP_403_FORBIDDEN)

class AluguelDestroyAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        try:
            aluguel = Aluguel.objects.get(pk=pk, hospede=request.user)
            aluguel.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Aluguel.DoesNotExist:
            return Response({"error":"esse aluguel não pertence a você"}, status=status.HTTP_403_FORBIDDEN)

