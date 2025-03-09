from django.shortcuts import render
from django.views import View
from shop.models.product import Product
from shop.models.category import Category

class HomeView(View):
    def get(self, request):
        categories = Category.objects.all()
        category_id = request.GET.get('category')

        if category_id:
            products = Product.objects.filter(category_id=category_id)
        else:
            products = Product.objects.all()

        data = {'products': products, 'categories': categories}
        return render(request, 'index.html', data)
    
    def post(self, request):
        pass  # Implement if needed in the future
