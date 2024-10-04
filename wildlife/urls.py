
from django.contrib import admin
from django.urls import path

from django.conf import settings
from django.conf.urls.static import static
from core import views as core_views
from pre import views as pre_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("",core_views.home),
    path("features/",core_views.features,name="features"),
    
    
   path('quiz/', core_views.fetch_and_display_quiz, name='quiz_list'),
    path('quiz/submit/<int:quiz_id>/', core_views.quiz_submit, name='quiz_submit'),
    path("dashboard/",core_views.dashboard,name="dashboard"),
     path('edit_profile/', core_views.edit_profile, name='edit_profile'),
    path("blog/",core_views.blog,name="blog"),
    path('add/', core_views.add_blog_post, name='add_blog_post'),
    path('edit/<int:pk>/', core_views.edit_blog_post, name='edit_blog_post'),
    path('delete/<int:pk>/', core_views.delete_blog_post, name='delete_blog_post'),
     path("event1/",core_views.event1,name="event1"),
     path("event2/",core_views.event2,name="event2"),
     path("contact/",core_views.contact,name="contact"),
    path("login/",core_views.user_login,name="login"),
    path("logout/",core_views.user_logout,name="logout"),
    path("signup/",core_views.user_signup,name="signup"),
    path("encyclopedia/",core_views.encyclopedia,name="map"),
        path("aq/",core_views.aq,name="aq"),
            path("pet/",core_views.pet,name="pet"),
            path("tank/",core_views.tank,name="tank"),
    path('ap/', core_views.ap_view, name='ap'),
    path('as/', core_views.as_view, name='as'),
    path('ar/', core_views.ar_view, name='ar'),
    path('br/', core_views.br_view, name='br'),
    path('ct/', core_views.ct_view, name='ct'),
    path('ga/', core_views.ga_view, name='ga'),
    path('gj/', core_views.gj_view, name='gj'),
    path('hp/', core_views.hp_view, name='hp'),
    path('hr/', core_views.hr_view, name='hr'),
    path('jh/', core_views.jh_view, name='jh'),
    path('ka/', core_views.ka_view, name='ka'),
    path('kl/', core_views.kl_view, name='kl'),
    path('mh/', core_views.mh_view, name='mh'),
    path('mn/', core_views.mn_view, name='mn'),
    path('mp/', core_views.mp_view, name='mp'),
    path('mz/', core_views.mz_view, name='mz'),  # Add path for Mizoram
    path('nl/', core_views.nl_view, name='nl'),  # Add path for Nagaland
    path('or/', core_views.or_view, name='or'),
    path('pb/', core_views.pb_view, name='pb'),  # Add path for Punjab
    path('rj/', core_views.rj_view, name='rj'),  # Add path for Rajasthan
    path('sk/', core_views.sk_view, name='sk'),  # Add path for Sikkim
    path('tn/', core_views.tn_view, name='tn'),
    path('tg/', core_views.tg_view, name='tg'),  # Add path for Telangana
    path('tr/', core_views.tr_view, name='tr'),
    path('up/', core_views.up_view, name='up'),
    path('ut/', core_views.ut_view, name='ut'),  # Add path for Uttarakhand
    path('wb/', core_views.wb_view, name='wb'),
    path('an/', core_views.an_view, name='an'),  # Add path for Andaman and Nicobar Islands
    path('ch/', core_views.ch_view, name='ch'),  # Add path for Chandigarh
    path('dl/', core_views.dl_view, name='dl'),  # Add path for Delhi
    path('ld/', core_views.ld_view, name='ld'),  # Add path for Lakshadweep
    path('py/', core_views.py_view, name='py'),  # Add path for Puducherry
    path('wb/', core_views.wb_view, name='wb'),  # Add path for West Bengal
    path('jk/', core_views.jk_view, name='jk'),
    path('ml/', core_views.ml_view, name='ml'),


                 path('donate/', core_views.donate, name='donate'),
                  path('upload/', pre_views.predict, name='upload'),  # Home page for file upload
    path('result/', pre_views.predict, name='result'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)