# توثيق روابط الملف الشخصي والمتجر (Profile & Store API)

هذا الملف يوضح الروابط (Endpoints) الخاصة بالملف الشخصي للمستخدم، إعدادات التنبيهات، وبيانات المتجر.

---

## 1. بيانات الملف الشخصي (User Profile)
جلب بيانات المستخدم الحالي مع بيانات متجره (إن وجد).

- **الرابط:** `/api/users/profile/`
- **الطريقة:** `GET`
- **التوثيق:** يحتاج تسجيل دخول (Bearer Token).
- **الاستجابة (Response):**
```json
{
    "id": "uuid",
    "phone": "0123456789",
    "name": "Full Name",
    "email": "email@example.com",
    "role": "trader",
    "address": "Address text",
    "notification_settings": {
        "push_enabled": true,
        "email_enabled": false,
        "order_updates_enabled": true,
        "offers_enabled": true
    },
    "store": {
        "id": "uuid",
        "name": "Store Name",
        "logo_url": "...",
        "description": "...",
        "category": "...",
        "rating": 4.5
    },
    "created_at": "..."
}
```

---

## 2. تعديل الملف الشخصي (Update Profile)
تعديل الاسم، الإيميل، أو العنوان.

- **الرابط:** `/api/users/profile/`
- **الطريقة:** `PATCH` / `PUT`
- **البادي (Body):**
```json
{
    "name": "New Name",
    "email": "new_email@example.com",
    "address": "New Address"
}
```

---

## 3. إعدادات التنبيهات (Notification Settings)
جلب أو تعديل إعدادات التنبيهات.

- **الرابط:** `/api/users/profile/notifications/`
- **الطريقة:** `GET` لجلب البيانات، و `PATCH` للتعديل.
- **البادي للتعديل (Body):**
```json
{
    "push_enabled": false,
    "email_enabled": true
}
```

---

## 4. تغيير كلمة المرور (Change Password)
تغيير الباسورد الحالي.

- **الرابط:** `/api/users/profile/change-password/`
- **الطريقة:** `PUT` / `PATCH`
- **البادي (Body):**
```json
{
    "old_password": "كلمة_المرور_القديمة",
    "new_password": "كلمة_المرور_الجديدة",
    "confirm_password": "تأكيد_كلمة_المرور_الجديدة"
}
```
- **الاستجابة عند النجاح:** `{"message": "تم تغيير كلمة المرور بنجاح."}`

---

## 5. بيانات المتجر الخاص بي (My Store)
الوصول المباشر لمتجر المستخدم الحالي وتعديله دون الحاجة للـ ID الخاص بالمتجر.

- **الرابط:** `/api/stores/my-store/`
- **الطريقة:** `GET` لجلب بيانات المتجر، و `PATCH` لتعديلها.
- **البادي للتعديل (Body):**
```json
{
    "name": "اسم المتجر الجديد",
    "description": "وصف جديد",
    "logo_url": "رابط اللوجو الجديد"
}
```

---

## 6. إحصائيات المتجر (Store Statistics)
جلب بيانات المتجر الأساسية مع إحصائيات الأداء والمبيعات.

- **الرابط:** `/api/stores/my-store/statistics/`
- **الطريقة:** `GET`
- **الاستجابة (Response):**
```json
{
    "id": "uuid",
    "name": "Store Name",
    "logo_url": "http://...",
    "avg_order_value_placed": 1250.50,
    "avg_order_value_received": 3400.00,
    "new_orders_count": 5,
    "total_sales": 55000.00
}
```
- **شرح الحقول:**
    - `avg_order_value_placed`: متوسط سعر الطلبات التي قام المستخدم بعملها (كمشتري).
    - `avg_order_value_received`: متوسط سعر الطلبات التي استلمها المتجر (كمورد).
    - `new_orders_count`: عدد الطلبات الجديدة (بانتظار الموافقة) التي وصلت في آخر 48 ساعة.
    - `total_sales`: إجمالي قيمة الطلبات المكتملة (`completed`) التي باعها المتجر.
