from rest_framework.views import APIView
from .serializer import UserSerializer, ProductSerializer, ReviewSerializer, OrderSerializer
from .models import client, Product, Review, Order, ShippingAddress, OrderItem
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .middleware import AuthMiddleware
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from django.utils import timezone
import jwt


# GETS A CERTAIN USER WITHOUT ADMIN PERMISSION , UPDATE AND DELETE
class get_certain_user(APIView):
    def get(self, request, *args, **kwargs):
        instance = client.objects.get(id=kwargs["pk"])
        serializer = UserSerializer(instance)
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        serializer = UserSerializer(instance=client.objects.filter(id=kwargs["pk"])[0], data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    def delete(self, request, *args, **kwargs):
        user_id = kwargs.get('pk')
        if user_id:
            try:
                user = client.objects.get(id=user_id)
                user.delete()
                return Response({'message': 'User deleted successfully.'})
            except Exception as es:
                return Response({'message': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'message': 'Please provide a valid  ID.'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def Register(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.create(validated_data=serializer.validated_data)
        return Response({'message': 'User created successfully.'}, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def login(request):
    try:
        data = request.data
        username = data["username"]
        password = data["password"]
        user = client.objects.get(username=username)
        if user.check_password(password):
            user_dict = {
                "id": user.id,
                "username": user.username,
                "password": user.password
            }
            token = jwt.encode(user_dict, key='asdrft123')
            return Response({"token": token})

        else:
            return Response({"error": "Invalid username or password"}, status=status.HTTP_401_UNAUTHORIZED)
    except client.DoesNotExist:
        return Response({"error": "Invalid username or password"}, status=status.HTTP_401_UNAUTHORIZED)
    except Exception as ex:
        return Response({"error": str(ex)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# HANDLES ADMIN GET ALL USERS
class AdminUserListView(APIView):
    @method_decorator(AuthMiddleware)
    def get(self, request):
        users = client.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)


# HANDLES ADMIN DELETE ,UPDATE OR GET CERTAIN USER
class AdminUserDetailView(APIView):
    @method_decorator(AuthMiddleware)
    def delete(self, request, pk):
        user_id = request.query_params.get('pk')
        user = client.objects.get(id=user_id)
        user.delete()
        return Response({"message": f"User with id {pk} was deleted successfully."})

    @method_decorator(AuthMiddleware)
    def get(self, request):
        user_id = request.query_params.get('pk')
        user = client.objects.get(id=user_id)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    @method_decorator(AuthMiddleware)
    def put(self, request, pk):
        user_id = request.query_params.get('pk')
        user = client.objects.get(id=user_id)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            user_dict = {
                "id": user.id,
                "username": user.username,
                "is_admin": user.isAdmin
            }
            token = jwt.encode(user_dict, key='asdrft123')
            return Response({"user": serializer.data, "token": token})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# HANDLES GET AND POST PRODUCT
class ProductList(APIView):
    def get(self, request):
        keyword = request.query_params.get('keyword', '')
        products = Product.objects.filter(name__icontains=keyword)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# HANDLES ALL THE PRODUCT DETAILS UPDATE,GET,DELETE
class ProductDetail(APIView):
    def get(self, request, pk):
        product = self.get_object(pk)
        if product is not None:
            serializer = ProductSerializer(product)
            return Response(serializer.data)
        return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        product = self.get_object(pk)
        if product is not None:
            serializer = ProductSerializer(product, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        product = self.get_object(pk)
        if product is not None:
            product.delete()
            return Response({'message': 'Product deleted successfully'})
        return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)


# Create product Review
class ProductReviewCreateAPIView(APIView):
    def post(self, request):

        token = request.headers.get('Authorization').split(' ')[1]
        try:
            user = jwt.decode(token, key='asdrft123', algorithms=["HS256"])
        except jwt.exceptions.DecodeError:
            return JsonResponse({"error": "Invalid token encoding"}, status=401)

        client_obj = client.objects.get(id=user['id'])
        product_id = request.query_params.get('product_id')
        if not product_id:
            return Response({'error': 'Product ID is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            product = Product.objects.get(pk=product_id)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

        if request.data is None:
            return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)

        rating = request.data.get('rating')
        comment = request.data.get('comment')

        if not rating or not comment:
            return Response({'error': 'Rating and comment are required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            rating = int(rating)
        except ValueError:
            return Response({'error': 'Rating should be an integer'}, status=status.HTTP_400_BAD_REQUEST)

        if rating < 1 or rating > 5:
            return Response({'error': 'Rating should be an integer between 1 and 5'},
                            status=status.HTTP_400_BAD_REQUEST)

        print(request.data)
        review = Review(product_id=product, user_id=client_obj, rating=rating, comment=comment)
        review.save()

        product.num_reviews += 1
        product.avg_rating = ((product.avg_rating * (product.num_reviews - 1)) + rating) / product.num_reviews
        product.save()

        serializer = ReviewSerializer(review)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def addOrderItems(request):
    token = request.headers.get('Authorization').split(' ')[1]
    try:
        user = jwt.decode(token, key='asdrft123', algorithms=["HS256"])
    except jwt.exceptions.DecodeError:
        return JsonResponse({"error": "Invalid token encoding"}, status=401)

    user = client.objects.get(id=user['id'])

    # Get data from request
    order_items = request.data.get('orderItems', [])
    shipping_address = request.data.get('shippingAddress', {})
    payment_method = request.data.get('paymentMethod', '')

    # Calculate order total and create new order
    order_items_total = 0
    for item in order_items:
        product = Product.objects.get(id=item['product'])
        order_items_total += item['quantity'] * product.price

    order = Order.objects.create(
        user=user,
        payment_method=payment_method,
        total_price=int(order_items_total),
    )

    # Create  shipping address for the order

    shipping_address_obj = ShippingAddress.objects.create(
        street_address=shipping_address['street_address'],
        city=shipping_address['city'],
        state=shipping_address['state'],
        country=shipping_address['country'],
        order=order,
    )

    # reduce product count with each orderd item
    for item in order_items:
        product = Product.objects.get(id=item['product'])

        order_item = OrderItem.objects.create(
            product=product,
            order=order,
            quantity=item['quantity'],
        )

        product.quantity -= item['quantity']
        product.save()

    serializer = OrderSerializer(order, many=False)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
def getMyOrders(request):
    token = request.headers.get('Authorization').split(' ')[1]
    try:
        user = jwt.decode(token, key='asdrft123', algorithms=["HS256"])
    except jwt.exceptions.DecodeError:
        return JsonResponse({"error": "Invalid token encoding"}, status=401)

    user = client.objects.get(id=user['id'])
    orders = user.orders.all()
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


# Get All Orders (Only for Admin User)
@api_view(['GET'])
@method_decorator(AuthMiddleware)
def getAllOrders(request):
    orders = Order.objects.all()
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['PUT'])
def UpdateOrderToPaid( request, pk):
    token = request.headers.get('Authorization').split(' ')[1]
    try:
        user = jwt.decode(token, key='asdrft123', algorithms=["HS256"])
    except jwt.exceptions.DecodeError:
        return JsonResponse({"error": "Invalid token encoding"}, status=401)

    user = client.objects.get(id=user['id'])
    # check if the order exists
    try:
        order = Order.objects.get(pk=pk)
    except Order.DoesNotExist:
        return Response({'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)

    # check if the user has permission to update the order
    if order.user != user:
        return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)

    # update order to paid state
    order.is_paid = True
    order.paid_at = timezone.now()
    order.save()

    return Response({'message': 'Order updated to paid state.'}, status=status.HTTP_200_OK)
