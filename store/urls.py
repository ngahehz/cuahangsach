from django.urls import include, path

from . import views

urlpatterns = [
	path('', views.store, name="store"),
	path('cart/', views.cart, name="cart"),
	path('search/', views.search, name="search"),
	path('product/<int:pk>/', views.productInfo, name="product"),
	path('checkout/', views.checkout, name="checkout"),
	path('update_item/', views.updateItem, name="update_item"),
	path('process_order/', views.processOrder, name="process_order"),
	#path('profile/', views.ProfileView.as_view(), name="profile"),
	path('register/', views.register_user, name="register"),
    path('logout/', views.logout_user, name='logout'),
	path('register/ok/', views.SiteRegisterOkView.as_view(), name="register_ok"),
	path('profile/', views.profile, name="profile"),
	path('', include('django.contrib.auth.urls')),
]