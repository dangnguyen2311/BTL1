from django.http import HttpResponseRedirect
from django.shortcuts import render , redirect, get_object_or_404

from django.contrib.auth.hashers import  check_password, make_password
from core.models import Category, Customer 
from core.form import ProductSearchForm
from django.views import  View
from core.models import Products, Order



def store(request):                                 # Thao tác với thanh danh mục sản phẩm 
    # print("test store func")
    cart = request.session.get('cart')              # Lấy cart từ session
    if not cart:
        request.session['cart'] = {}                # Tạo mới cart
    products = None
    categories = Category.get_all_categories()      # Lấy các danh mục sản phẩm
    # print(categories)
    categoryID = request.GET.get('category')        # Lấy id các danh mục, All Product thì id = None, có ha không thì nó nằm trong request
    
    # print(categoryID)
    if categoryID:
        products = Products.get_all_products_by_categoryid(categoryID)       # Hiển thị sản phẩm theo danh mục sản phẩm
    else:
        products = Products.get_all_products();                              # Xử lý khi ấn All Product

    # Cập nhật data 
    data = {}
    data['products'] = products                                              
    data['categories'] = categories

    # Gửi data đến index.html
    return render(request, 'index.html', data)    



class Index(View):
    def post(self , request):
        # print("test post")
        product = request.POST.get('product')       # Lấy product.id từ index.html khi tăng/giảm số lượng sản phẩm từ trang chủ
        remove = request.POST.get('remove')         # Nếu giảm quantity xuống 1 thì remove = True để có quyền xoá sản phẩm khỏi cart.
        # print(product, remove)                  
        cart = request.session.get('cart')          # Lấy dict cart chứa thông tin về số lượng sản phẩm đang được chọn từ session
        if cart:                                    # Nếu cart có sản phẩm đó
            quantity = cart.get(product)            # Láy số lượng
            if quantity:                        
                if remove:                      
                    if quantity<=1:                 # Xoá sản phẩm khỏi cart nếu ấn nút "-" khi số lượng còn 1
                        cart.pop(product)
                    else:                           # Giảm số lượng sản phẩm
                        cart[product]  = quantity-1
                        print(cart[product])
                else:                           
                    cart[product]  = quantity+1     # Nếu tăng số lượng sản phẩm khi đã có sản phẩm cho cart thì số lượng tăng
                    # print(cart[product])

            else:
                cart[product] = 1                   # Chưa có sản phẩm đó trong cart thì set số lượng = 1 khi ấn add to cart
                # print(cart[product])
        else:
            cart = {}                               # cart không có sản phẩm nào thì khi ấn add to cart set số lượng = 1 của sản phẩm được chọn
            cart[product] = 1
            # print(cart[product])

        request.session['cart'] = cart              # Cập nhật cart
        # print('cart' , request.session['cart'])
        return redirect('homepage')

    def get(self, request):     # tìm kiếm
        form = ProductSearchForm(request.GET)  # Lấy form data từ get request

        # Kiểm tra form có hợp lệ hay không
        if form.is_valid():
            # Hợp lệ thì lấy thông tin user nhập
            search_query = form.cleaned_data.get('search_query', '')
        else:
            # Không hợp lệ thì không thực hiện tìm kiếm
            search_query = ''

        # Cập nhật thông tin giỏ hàng
        cart = request.session.get('cart')
        if not cart:
            request.session['cart'] = {}

        categories = Category.get_all_categories()      
        categoryID = request.GET.get('category')        # Lấy id từ url parameter khi click vào từng danh mục

        # id hợp lệ thì trả về thông tin tất cả các sản phẩm thuộc cùng 1 danh mục
        if categoryID:
            products = Products.get_all_products_by_categoryid(categoryID)
        else:
            # Xử lý data nhập vào form tìm kiếm
            if search_query:
                # Tìm sản phẩm dựa trên data nhập vào
                products = Products.objects.filter(name__icontains=search_query)
            else:
                products = Products.get_all_products()
        
        # Data gửi về index.html
        data = {    
            'products': products,       # Sản phẩm dựa trên danh mục hoặc được tìm kiếm
            'categories': categories,   # Tất cả danh mục
            'form': form,               # Search form
        }

        return render(request, 'index.html', data)



class Cart(View):   # path('cart', auth_middleware(Cart.as_view()) , name='cart'),
    def get(self , request):
        ids = list(request.session.get('cart').keys())
        products = Products.get_products_by_id(ids)
        print(products)
        return render(request , 'cart.html' , {'products' : products} )



class Change(View): # path('up_cart', Change.up_cart, name='up_cart'), path('down_cart', Change.down_cart, name='down_cart'),
    def down_cart(request):
        product_id = request.POST['product_id']
        cart = request.session.get('cart', {})  # Lấy thông tin giỏ hàng từ session

        if product_id in cart:
            if cart[product_id] > 1:
                cart[product_id] -= 1  # Giảm số lượng sản phẩm đi 1
            else:
                del cart[product_id]  # Xóa sản phẩm khỏi giỏ hàng nếu số lượng là 1

        request.session['cart'] = cart  # Cập nhật session cart sau khi bỏ sản phẩm

        return redirect('cart')  # Redirect người dùng đến trang giỏ hàng sau khi cập nhật
    
    def up_cart(request):
        product_id = request.POST['product_id']
        cart = request.session.get('cart', {})  # Lấy thông tin giỏ hàng từ session

        if product_id in cart:
            # if cart[product_id] > 1:
            #     cart[product_id] += 1  # Giảm số lượng sản phẩm đi 1
            # else:
            #     del cart[product_id]  # Xóa sản phẩm khỏi giỏ hàng nếu số lượng là 1
            cart[product_id] += 1

        request.session['cart'] = cart  # Cập nhật session cart sau khi bỏ sản phẩm

        return redirect('cart')
    
    
    
class CheckOut(View):   # path('check-out', CheckOut.as_view() , name='checkout'),
    def post(self, request):
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        customer = request.session.get('customer')
        cart = request.session.get('cart')
        products = Products.get_products_by_id(list(cart.keys()))
        print(address, phone, customer, cart, products)
        for product in products:
            print(cart.get(str(product.id)))
            order = Order(customer=Customer(id=customer),
                          product=product,
                          price=product.price,
                          address=address,
                          phone=phone,
                          quantity=cart.get(str(product.id)))
            order.save()
        request.session['cart'] = {}
        return redirect('cart')



def detail_product(request, product_id):
    product = Products.objects.get(id=product_id)
    return render(request, 'detail_product.html', {'product': product})



class Login(View):
    return_url = None

    def get(self, request):
        Login.return_url = request.GET.get ('return_url')
        return render (request, 'login.html')

    def post(self, request):
        email = request.POST.get ('email')
        password = request.POST.get ('password')
        customer = Customer.get_customer_by_email (email)
        error_message = None
        if customer:
            flag = check_password (password, customer.password)
            if flag:
                request.session['customer'] = customer.id

                if Login.return_url:
                    return HttpResponseRedirect (Login.return_url)
                else:
                    Login.return_url = None
                    return redirect ('homepage')
            else:
                error_message = 'Invalid !!'
        else:
            error_message = 'Invalid !!'

        print (email, password)
        return render (request, 'login.html', {'error': error_message})



def logout(request):
    request.session.clear()
    return redirect('login')       
 


class OrderView(View):
    def get(self , request):
        customer = request.session.get('customer')
        orders = Order.get_orders_by_customer(customer)
        print(orders)
        return render(request , 'orders.html'  , {'orders' : orders})



class Signup (View):
    def get(self, request):
        return render (request, 'signup.html')

    def post(self, request):
        postData = request.POST
        first_name = postData.get('firstname')
        last_name = postData.get('lastname')
        phone = postData.get('phone')
        email = postData.get('email')
        password = postData.get('password')
        # validation
        value = {
            'first_name': first_name,
            'last_name': last_name,
            'phone': phone,
            'email': email
        }
        error_message = None

        customer = Customer (first_name=first_name,
                             last_name=last_name,
                             phone=phone,
                             email=email,
                             password=password)
        error_message = self.validateCustomer(customer)

        if not error_message:
            print(first_name, last_name, phone, email, password)
            customer.password = make_password(customer.password)
            customer.register()
            return redirect('homepage')
        else:
            data = {
                'error': error_message,
                'values': value
            }
            return render (request, 'signup.html', data)

    def validateCustomer(self, customer):
        error_message = None
        if (not customer.first_name):
            error_message = "Please Enter your First Name !!"
        elif len (customer.first_name) < 3:
            error_message = 'First Name must be 3 char long or more'
        elif not customer.last_name:
            error_message = 'Please Enter your Last Name'
        elif len (customer.last_name) < 3:
            error_message = 'Last Name must be 3 char long or more'
        elif not customer.phone:
            error_message = 'Enter your Phone Number'
        elif len (customer.phone) < 10:
            error_message = 'Phone Number must be 10 char Long'
        elif len (customer.password) < 5:
            error_message = 'Password must be 5 char long'
        elif len (customer.email) < 5:
            error_message = 'Email must be 5 char long'
        elif customer.isExists ():
            error_message = 'Email Address Already Registered..'
        # saving

        return error_message
    
    
    

# class Index(View):
#     def post(self , request):
#         product = request.POST.get('product')
#         remove = request.POST.get('remove')
#         cart = request.session.get('cart')
#         if cart:
#             quantity = cart.get(product)
#             if quantity:
#                 if remove:
#                     if quantity<=1:
#                         cart.pop(product)
#                     else:
#                         cart[product]  = quantity-1
#                 else:
#                     cart[product]  = quantity+1
#             else:
#                 cart[product] = 1
#         else:
#             cart = {}
#             cart[product] = 1
#         request.session['cart'] = cart
#         print('cart' , request.session['cart'])
#         return redirect('homepage')
    
#     def get(self , request):
#         # print()
#         return HttpResponseRedirect(f'/store{request.get_full_path()[1:]}')


# sửa lại
# class Index(View):
#     def post(self , request):
#         # print("test post")
#         product = request.POST.get('product')       # Lấy product.id từ index.html khi tăng/giảm số lượng sản phẩm từ trang chủ
#         remove = request.POST.get('remove')         # Nếu giảm quantity xuống 1 thì remove = True để có quyền xoá sản phẩm khỏi cart.
#         # print(product, remove)                  
#         cart = request.session.get('cart')          # Lấy dict cart chứa thông tin về số lượng sản phẩm đang được chọn từ session
#         if cart:                                    # Nếu cart có sản phẩm đó
#             quantity = cart.get(product)            # Láy số lượng
#             if quantity:                        
#                 if remove:                      
#                     if quantity<=1:                 # Xoá sản phẩm khỏi cart nếu ấn nút "-" khi số lượng còn 1
#                         cart.pop(product)
#                     else:                           # Giảm số lượng sản phẩm
#                         cart[product]  = quantity-1
#                         print(cart[product])
#                 else:                           
#                     cart[product]  = quantity+1     # Nếu tăng số lượng sản phẩm khi đã có sản phẩm cho cart thì số lượng tăng
#                     # print(cart[product])

#             else:
#                 cart[product] = 1                   # Chưa có sản phẩm đó trong cart thì set số lượng = 1 khi ấn add to cart
#                 # print(cart[product])
#         else:
#             cart = {}                               # cart không có sản phẩm nào thì khi ấn add to cart set số lượng = 1 của sản phẩm được chọn
#             cart[product] = 1
#             # print(cart[product])

#         request.session['cart'] = cart              # Cập nhật cart
#         # print('cart' , request.session['cart'])
#         return redirect('homepage')



#     def get(self, request):
#         form = ProductSearchForm(request.GET)  # Lấy form data từ get request

#         # Kiểm tra form có hợp lệ hay không
#         if form.is_valid():
#             # Hợp lệ thì lấy thông tin user nhập
#             search_query = form.cleaned_data.get('search_query', '')
#         else:
#             # Không hợp lệ thì không thực hiện tìm kiếm
#             search_query = ''

#         # Cập nhật thông tin giỏ hàng
#         cart = request.session.get('cart')
#         if not cart:
#             request.session['cart'] = {}


#         categories = Category.get_all_categories()      
#         categoryID = request.GET.get('category')        # Lấy id từ url parameter khi click vào từng danh mục

#         # id hợp lệ thì trả về thông tin tất cả các sản phẩm thuộc cùng 1 danh mục
#         if categoryID:
#             products = Products.get_all_products_by_categoryid(categoryID)
#         else:
#             # Xử lý data nhập vào form tìm kiếm
#             if search_query:
#                 # Tìm sản phẩm dựa trên data nhập vào
#                 products = Products.objects.filter(name__icontains=search_query)
#             else:
#                 products = Products.get_all_products()
        
#         # Data gửi về index.html
#         data = {
#             'products': products,       # Sản phẩm dựa trên danh mục hoặc được tìm kiếm
#             'categories': categories,   # Tất cả danh mục
#             'form': form,               # Search form
#         }

#         return render(request, 'index.html', data)

# def store(request):                                 # Thao tác với thanh danh mục sản phẩm 
#     # print("test store func")
#     cart = request.session.get('cart')              # Lấy cart từ session
#     if not cart:
#         request.session['cart'] = {}                # Tạo mới cart
#     products = None
#     categories = Category.get_all_categories()      # Lấy các danh mục sản phẩm
#     # print(categories)
#     categoryID = request.GET.get('category')        # Lấy id các danh mục, All Product thì id = None
#     # print(categoryID)
#     if categoryID:
#         products = Products.get_all_products_by_categoryid(categoryID)       # Hiển thị sản phẩm theo danh mục sản phẩm
#     else:
#         products = Products.get_all_products();                              # Xử lý khi ấn All Product

#     # Cập nhật data 
#     data = {}
#     data['products'] = products                                              
#     data['categories'] = categories

#     # Gửi data đến index.html
#     return render(request, 'index.html', data)  

    

# def store(request):
#     cart = request.session.get('cart')
#     if not cart:
#         request.session['cart'] = {}
#     products = None
#     categories = Category.get_all_categories()
#     categoryID = request.GET.get('category')
#     if categoryID:
#         products = Products.get_all_products_by_categoryid(categoryID)
#     else:
#         products = Products.get_all_products()
#     data = {}
#     data['products'] = products
#     data['categories'] = categories
#     print('you are : ', request.session.get('email'))
#     return render(request, 'index.html', data)

