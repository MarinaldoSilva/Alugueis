# API de Reservas de Imóveis 🏡

## Projeto
Projeto desenvolvido do forma autônoma, usando como base a documentação do Django Rest Framework e muita pesquisa.
O projeto em si consiste em uma API de Reservas/Alugueis de imóveis, para desenvolvimento usei os princípios S.O.L.I.D. mas tomei cuidado para não ser verboso, a simplicidade funcional foi o objetivo.
Com esse sistema é possível que um usuário se cadastre com a única rota liberada para acesso são sem precisar de validação de ``usuário/senha e Token``, após isso o user tem duas opções:

* Cadastrar uma casa para aluguel.
* Alugar um casa já cadastrada.

Para que isso seja possível as foram criadas funções e validações para evitar conflitos.

### Processo de criação
Esse foi o projeto com uma lógica simples, porém complexa que tem como o core central a sobreposição de datas, usando o ``Q`` do próprio django, foi possível estabelecer um parâmetro de cruzamento de datas, assim 
evitando que a data de entrada fosse inferior a data de saída de um usuário, evitando conflito de datas, o usuário é injetado pela view, quando um usuário autenticado faz a requisição, todo o processo de:
* calcular preço das diárias
* validação de dadas
* calular datas para as entradas e saidas
* verificar se é um PUT para manipulação do self.instance que vem do banco para atualizações.

é feito quando o ``serializer.is_valid()`` é chamado, e após isso o meu ``data`` que é meu candidado a ``serializer.validated_data`` é validado e virá o meu ``validated``, com isso no ``serializer.save()``
os dados são persistidos no banco.
Caso aconteça algo nesse processo, uma mensagem do erro com o status vai ser fornecido para o cliente, assim facilitando a identificação do erro.

O projeto vai passar por melhorias futuras, tais como:
* Atualização para JWT
* Upload de imagens das casas
* Filtros e buscas

Com essas futuras implementações vamos ter um sistema bem mais robusto.

## Funções

### Alugueis
* Criação de usuários com ``Token`` de único vinculado ao ``username``
* Listagem de casas de um usuário (Dono das casas)
* Detalhes de um casas especificas
* Atualizar detalhes de uma casa (descrição, título, preço da diária e etc...)
* Injeção de user de forma automática (serializer)

### Casas
 * Criar novos alugueis para uma casa especifica
 * Validação de datas para evitar sobreposição(Q - formulas complexas)
 * Calcula automaticamente o valor do aluguel com base na quantidade dias que o usuário vai ficar
 * Casas que o usuário tem com alugueis ativos e inativos
 * Detalhes de um aluguel
 * Exclusão de alugueis


### Endpoints
Sendo extremamente honesto, não foi fácil fazer isso, envolveu muito estudo e dedicação, parece simples né? Não foi tão simples assim, agora eu vejo como ficou e penso "na teória é simples, na prática agente sofre", mas a vida é assim, com o passar do tempo vamos fazer isso de forma natural.
Vamos listar os princípais endpoints da API.

* **Criar user com Token**

  ```python
    class UserRegisterAPIView(APIView):
      permission_classes = [AllowAny]
  
      def post(self, request):
          serializer = UserSerializer(data=request.data)
          serializer.is_valid(raise_exception=True)
          user = serializer.save()    
          token, criar = Token.objects.get_or_create(user=user)
          """Quando a view é acessado por qualquer usuário, após as validações o token é gerado para o novo user"""
          return Response({
              'user_id':user.id,
              'username': user.username,
              'email': user.email,
              'token': token.key
              }, status=status.HTTP_201_CREATED)
  ```

  esse foi o processo de criação de token de usuário, no retorno do create vamos diponibilizar o token do user.


    ```json
    {
     	"username":"Rita39",
     	"email":"Ritastefanie91@hotmail.com",
     	"firts_name": "Rita",
     	"last_name": "Sfanie",
     	"password": "minha_senha"
    }
    ```

  Nossa requisição no insomnia seria assim.

  

* **POST - CASA**
  
  para cadastrar uma casa temos que estar validados com um token(aquele que foi gerado acima)

  ```python
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
  ```

  Não precisamos passar nada, o dono já vem na requisição (request.user)

  ```json
    {
   	"titulo": "Internal Tactics Administrator",
   	"descricao": "Lead",
   	"endereco": "4385 E Park Avenue",
   	"num_quartos": 2,
   	"preco_dia": "497.19",
    }
    ```

* **GET - CASA**

  Listando as casas pelo ID/PK, fiz somente uma view, porém verifico se o PK foi passado no parâmetro, caso seja é um ``detail``, se não for é um ``list all()``
  Requsição:
  ```
  http://127.0.0.1:8000//api/v1/reservas/casas/1/datalhes/
  ```
  resposta do servidor:

  ```json
    {
   	"id": 1,
   	"dono": "Narciso.Little",
   	"titulo": "Casa na praia de Igrejina",
   	"descricao": "Casa beira mar, abriu a porta já esta na beira mar para um mergulho único na sua vida.",
   	"endereco": "Recife, bairro de piedade",
   	"num_quartos": 2,
   	"preco_dia": "250.00",
   	"data_cadastro": "2025-10-14T18:26:04.776985Z"
    }
  ```


* **UPDATE - CASA**

  O processo de atualização foi o mais desafiador de todos para fazer, temos que prever possíveis erros, se o usuário tentar extender a estadia e esse imóvel já estiiver com reserva para o dia em       questão? como fazer para evitar sobrepossição de datas? Usando o ``Q`` do Django para criar formulas complexas(parece ser fácil, mas não é)
  
  ```python
      sobreposicao_de_alugueis = alugueis_da_casa.filter(
            Q(data_entrada__lt=data_saida, data_saida__gt=data_entrada)
        ).exists()

        if sobreposicao_de_alugueis:
            raise serializers.ValidationError({"error":"A data escolhida já está ocupada no momento."}) 
  ```

  e também temos o processo de calcular as diárias, onde vai ser baseado no valor diária x dias de estadia do hospede.

  ```py
   if data_entrada and data_saida:
            periodo_alugado = data_saida - data_entrada
            num_dias = periodo_alugado.days
            data['valor_aluguel'] = num_dias * casa_registrada.preco_dia
            return data
  ```
  
* **DELETE - CASA**

  Processo solimilar ao de listar PK, porém com o verbo HTTP setado para delete
  ```py
  class CasaDestroyAPIView(APIView):
    permission_classes=[IsAuthenticated]

    def delete(self, request, pk):
        try:
            casa = Casa.objects.get(pk=pk, dono=self.request.user)
            casa.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Casa.DoesNotExist:
            return Response({"error":"Não é possivel excluir uma casa que não é sua."}, status=status.HTTP_401_UNAUTHORIZED)
    ```
  Requisição
    ```
      http://127.0.0.1:8000/api/v1/reservas/aluguel/1/excluir/

  response:
  204 - No content

  ```

* **CRIAR ALUGUEL**

  Um demonstração de como o aluguel é criado.

  ```py
  class AluguelCreateAPIView(APIView):

    permission_classes=[IsAuthenticated]

    def post(self, request):
        serializer = AluguelSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(hospede=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
  ```

  a nossa requisição só precisa da data e casa, a resposta da requisição quando passo pelo seralizer faz o resto por nós

  ```py
  {
	 "casa": 2,
	 "data_entrada":"2025-10-19",
	 "data_saida" : "2025-10-22"
  }


  Response

  {
  "id": 3,
  "casa": 2,
  "hospede": 3,
  "valor_aluguel": "976.65",
  "data_entrada": "2025-10-19",
  "data_saida": "2025-10-22"
  }
  
  ```

  e se o usuário tentar fazer algum tipo de alteração irregular nas datas(como tentar alterar a estadia de um outro usuário)

  ```json
  {
    "casa": 1, 
    "data_entrada": "2024-09-01", 
    "data_saida": "2024-09-10" 
  }

  ```
  <br>


### Teste

Para testar é necessário ter o Python, minha versão é 3.12, clone o repositório do projeto.
```git
https://github.com/MarinaldoSilva/Alugueis
```

Verifique os arquivos `urls.py` de `config`, `reservas` e `users` para os endpoints completos, lembrando do caminho base `api/v1/`.
* Crie seu usuário e anote o seu Token
* cadastre uma casa
* tente fazer o aluguel da casa

crie seu ambinete virtual:
```bash
  python -m venv venv
  .\venv\Scipts\activate
```

instale o arquivido de libs:

```py
    pip install -r requirements.txt
```

Faça as migrações para o banco

```py
    python manage.py migrate
```

Teste o serviço rodando o servidor próprio do Django.

 ```py
    python manage.py runserver
 ```

Toda e qualquer sugestão é bem-vinda, meu email é ``marinaldo12@hotmail.com``, me escreve sua sugestão de melhoria e ideias, podemos construir isso juntos.
