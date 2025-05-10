from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from mainApp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home),
    path('shop/<str:mc>/<str:sc>/<str:br>/', views.shop),
    path('single-product/<slug:id>/', views.singleProduct, name='single_product'),
    path('login/', views.loginPage),
    path('signup/', views.signupPage),
    path('logout/', views.logoutPage),
    path('profile/', views.profilePage, name='profile'),
    path('update-profile/', views.updateProfilePage),
    path('add-to-cart/<int:id>/', views.addToCart),
    path('cart/', views.cartPage),
    path('delete-cart/<int:pid>/', views.deleteCart),
    path('update-cart/<int:pid>/<str:op>/',views.updateCart)



] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

