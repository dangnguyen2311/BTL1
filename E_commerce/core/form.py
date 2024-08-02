from django import forms

# form tìm kiếm sản phẩm theo tên
class ProductSearchForm(forms.Form):
    # Lấy data từ user khi nhập vào form tìm kiếm
    search_query = forms.CharField(max_length=100)