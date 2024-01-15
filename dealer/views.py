from django.contrib import messages
from django.db.models import F, ExpressionWrapper, PositiveIntegerField, Sum, FloatField
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import View
from django.views.generic import ListView
from django.http import JsonResponse
from authentication.mixins import CustomUserPassesTestMixin
from authentication.models import CustomUser
from authentication.strings.string import UNIT_CHOICES
from dsr.models import (
    DSRProductWallet,
    DSRVoucher,
    DSRSellingVoucher,
    DSRSales,
    DSRCollections,
)
from .models import (
    DealerExpense,
    Product,
    Stock,
    Voucher,
    DealerRepresentative,
    DamageStock,
)
from .forms import (
    DSRUserForm,
    DSRUserInfoForm,
    CollectionForm,
    DSRIndividualCollectionForm,
)
from super_admin.models import ExpenseName, DealerCompany, Company


# Create your views here.
class DealerHome(CustomUserPassesTestMixin, View):
    template_name = "dealer_home.html"
    user_type = "is_dealer"

    def get(self, request):
        return render(request, self.template_name)


class DealerTraining(CustomUserPassesTestMixin, View):
    user_type = "is_dealer"
    template_name = "training_dealer.html"

    def get(self, request):
        return render(request, template_name=self.template_name)


class DealerPrivacyPolicy(CustomUserPassesTestMixin, View):
    user_type = "is_dealer"
    template_name = "privacy_policy_dealer.html"

    def get(self, request):
        return render(request, template_name=self.template_name)


class DealerExpenses(CustomUserPassesTestMixin, View):
    user_type = "is_dealer"
    template_name = "dealer_expenses.html"
    expenses_obj = ExpenseName.objects.all()

    def get(self, request):
        data = {"expenses_name": self.expenses_obj}
        return render(request, template_name=self.template_name, context=data)

    def post(self, request):
        image_input = request.FILES.get("expenseImage")
        type_of_expense_id = request.POST.get("productSelected")
        paid_amount_input = request.POST.get("paidAmount")
        date_input = request.POST.get("datePicker")
        comments_input = request.POST.get("comment")

        expense_obj = ExpenseName.objects.filter(id=type_of_expense_id).first()

        if not (type_of_expense_id and expense_obj):
            messages.error(request, "খরচের ধরণ সিলেক্ট করুন !")
            data = {
                "expenses_name": self.expenses_obj,
                "expenseImage": image_input,
                "paidAmount": paid_amount_input,
                "comment": comments_input,
                "datePicker": date_input,
            }
            return render(request, template_name=self.template_name, context=data)

        obj_data = {
            "name": expense_obj,
            "paid_amount": paid_amount_input,
            "date": date_input,
            "comments": comments_input,
            "dealer": request.user,
        }

        if image_input:
            obj_data["image"] = image_input

        obj = DealerExpense.objects.create(**obj_data)
        messages.success(request, "খরচ সফলভাবে অ্যাড হয়েছে !")
        return redirect("dealer:home")


class ProductUpload(CustomUserPassesTestMixin, View):
    user_type = "is_dealer"
    template_name = "product_upload.html"

    def get(self, request):
        return render(request, template_name=self.template_name)


class NewProductUpload(CustomUserPassesTestMixin, View):
    user_type = "is_dealer"
    template_name = "upload_new_product.html"

    def get(self, request):
        data = {
            "companies": request.user.dealer_companies.all(),
            "unit_choices": UNIT_CHOICES,
        }
        return render(request, template_name=self.template_name, context=data)

    def post(self, request):
        product_name = request.POST.get("productName")
        product_company_id = request.POST.get("company")
        product_factor = int(request.POST.get("factor"))
        product_unit = request.POST.get("boxCategory")
        dealer_buying_price_of_product = float(request.POST.get("dp"))
        dealer_selling_price_of_product = float(request.POST.get("tp"))
        product_quantity_in_unit = int(request.POST.get("cartoon"))
        product_quantity_in_pieces = int(request.POST.get("pieces"))
        product_total_price = float(request.POST.get("productPrice"))
        product_price_per_piece = float(request.POST.get("pricePerpiece"))

        product_info = {
            "product_name": product_name,
            "product_company_id": int(product_company_id)
            if product_company_id
            else None,
            "product_factor": product_factor,
            "product_unit": product_unit,
            "dealer_buying_price_of_product": dealer_buying_price_of_product,
            "dealer_selling_price_of_product": dealer_selling_price_of_product,
            "product_quantity_in_unit": product_quantity_in_unit,
            "product_quantity_in_pieces": product_quantity_in_pieces,
            "product_total_price": product_total_price,
            "product_price_per_piece": product_price_per_piece,
            "companies": request.user.dealer_companies.all(),
            "unit_choices": UNIT_CHOICES,
        }
        print(product_info)
        company_obj = Company.objects.filter(id=product_company_id).first()
        if product_company_id is None or company_obj is None:
            messages.error(request, "কোম্পানি সিলেক্ট করুন!")
            return render(request, self.template_name, context=product_info)

        elif product_price_per_piece != dealer_buying_price_of_product:
            messages.error(
                request, "ডিলারের ক্রয়মূল্য এবং পণ্যের প্রতি পিচের মূল্য সমান নয়!"
            )
            return render(request, self.template_name, context=product_info)
        else:
            product_obj = Product.objects.filter(
                name=product_name,
                dealer=request.user,
                company=company_obj.id,
                factor=product_factor,
                unit=product_unit,
            ).first()
            if product_obj is None:
                product_obj = Product.objects.create(
                    name=product_name,
                    dealer=request.user,
                    company=company_obj,
                    factor=product_factor,
                    unit=product_unit,
                    dealer_buying_price=dealer_buying_price_of_product,
                    dealer_selling_price=dealer_selling_price_of_product,
                )
                stock_obj = Stock.objects.create(
                    product=product_obj,
                    quantity=int(
                        product_factor * product_quantity_in_unit
                        + product_quantity_in_pieces
                    ),
                )
                voucher_obj = Voucher.objects.create(
                    product=product_obj,
                    quantity=int(
                        product_factor * product_quantity_in_unit
                        + product_quantity_in_pieces
                    ),
                    dealer=request.user,
                )
                messages.success(request, "প্রডাক্ট সফলভাবে অ্যাড হয়েছে !")
                return redirect("dealer:dealer-product-upload")
            else:
                messages.info(
                    request,
                    "প্রডাক্টি আগে অ্যাড করা হয়েছে। পরিমাণ আপডেটের জন্য আপডেট পেজে যান!",
                )
                return render(request, self.template_name, context=product_info)


class EditProduct(CustomUserPassesTestMixin, View):
    user_type = "is_dealer"
    template_name = "dealer_edit_product.html"

    def get(self, request, pk):
        product_obj = Product.objects.get(pk=pk)
        product_info = {
            "product_name": product_obj.name,
            "product_company_id": product_obj.company.id,
            "product_factor": product_obj.factor,
            "product_unit": product_obj.unit,
            "dealer_buying_price_of_product": product_obj.dealer_buying_price,
            "dealer_selling_price_of_product": product_obj.dealer_selling_price,
            "product_quantity_in_unit": product_obj.stock.get_quantity_in_unit(),
            "product_quantity_in_pieces": product_obj.stock.get_quantity_in_piece(),
            "product_total_price": product_obj.stock.get_total_buying_price(),
            "product_price_per_piece": product_obj.stock.quantity
            / product_obj.stock.get_total_buying_price(),
            "companies": request.user.dealer_companies.all(),
            "unit_choices": UNIT_CHOICES,
        }
        return render(request, template_name=self.template_name, context=product_info)

    def post(self, request, pk):
        product_name = request.POST.get("productName")
        product_company_id = request.POST.get("company")
        product_factor = int(request.POST.get("factor"))
        product_unit = request.POST.get("boxCategory")
        dealer_buying_price_of_product = float(request.POST.get("dp"))
        dealer_selling_price_of_product = float(request.POST.get("tp"))
        product_quantity_in_unit = int(request.POST.get("cartoon"))
        product_quantity_in_pieces = int(request.POST.get("pieces"))
        product_total_price = float(request.POST.get("productPrice"))
        product_price_per_piece = float(request.POST.get("pricePerpiece"))

        product_info = {
            "product_name": product_name,
            "product_company_id": int(product_company_id)
            if product_company_id
            else None,
            "product_factor": product_factor,
            "product_unit": product_unit,
            "dealer_buying_price_of_product": dealer_buying_price_of_product,
            "dealer_selling_price_of_product": dealer_selling_price_of_product,
            "product_quantity_in_unit": product_quantity_in_unit,
            "product_quantity_in_pieces": product_quantity_in_pieces,
            "product_total_price": product_total_price,
            "product_price_per_piece": product_price_per_piece,
            "companies": request.user.dealer_companies.all(),
            "unit_choices": UNIT_CHOICES,
        }
        print(product_info)
        company_obj = Company.objects.filter(id=product_company_id).first()
        if product_company_id is None or company_obj is None:
            messages.error(request, "কোম্পানি সিলেক্ট করুন!")
            return render(request, self.template_name, context=product_info)

        elif product_price_per_piece != dealer_buying_price_of_product:
            messages.error(
                request, "ডিলারের ক্রয়মূল্য এবং পণ্যের প্রতি পিচের মূল্য সমান নয়!"
            )
            return render(request, self.template_name, context=product_info)
        else:
            product_obj = Product.objects.get(pk=pk)
            difference_from_current_stock = (
                int(
                    product_factor * product_quantity_in_unit
                    + product_quantity_in_pieces
                )
                - product_obj.stock.quantity
            )

            if product_obj:
                product_obj.name = product_name
                product_obj.company = company_obj
                product_obj.factor = product_factor
                product_obj.unit = product_unit
                product_obj.dealer_buying_price = dealer_buying_price_of_product
                product_obj.dealer_selling_price = dealer_selling_price_of_product
                product_obj.stock.quantity = int(
                    product_factor * product_quantity_in_unit
                    + product_quantity_in_pieces
                )
                product_obj.stock.save()
                product_obj.save()
                if difference_from_current_stock != 0:
                    voucher_obj = Voucher.objects.create(
                        product=product_obj, quantity=difference_from_current_stock,
                    )
                messages.success(request, "প্রডাক্ট সফলভাবে অ্যাড হয়েছে !")
                return redirect("dealer:product-stock")
            else:
                messages.info(
                    request, "Not Found",
                )
                return render(request, self.template_name, context=product_info)


class ProductListViewForAPI(CustomUserPassesTestMixin, ListView):
    user_type = "is_dealer"
    model = Product
    # template_name = "product_list.html"  # This can be any template or an empty string.
    context_object_name = "products"

    def get_queryset(self):
        # Select the required fields and rename 'dealer_buying_price' to 'price'
        return (
            Product.objects.filter(dealer=self.request.user)
            .values("id", "name", "factor", price=F("dealer_buying_price"))
            .order_by("id")
        )

    def render_to_response(self, context, **response_kwargs):
        # Convert the queryset to a list of dictionaries
        product_data = list(self.get_queryset())

        # Return the data as JSON
        return JsonResponse(product_data, safe=False, json_dumps_params={"indent": 4})


class ProductBulkUpload(CustomUserPassesTestMixin, View):
    user_type = "is_dealer"

    def post(self, request):
        post_data = request.POST

        # Initialize a list to store the dictionaries
        data_list = []

        # Extract the data and create dictionaries
        product_ids = post_data.getlist("product_id")
        product_names = post_data.getlist("product_name")
        cartons = post_data.getlist("carton")
        pieces = post_data.getlist("piece")

        for i in range(len(product_ids)):
            item_dict = {
                "product_id": product_ids[i],
                "product_name": product_names[i],
                "carton": cartons[i],
                "piece": pieces[i],
            }
            product_object = Product.objects.filter(id=product_ids[i]).first()
            if product_object.name == product_names[i]:
                if int(cartons[i]) > 0 or int(pieces[i]) > 0:
                    stock_obj = Stock.objects.get(product=product_object)
                    stock_obj.quantity += int(cartons[i]) * product_object.factor + int(
                        pieces[i]
                    )
                    stock_obj.save()
                    voucher_obj = Voucher.objects.create(
                        product=product_object,
                        quantity=int(cartons[i]) * product_object.factor
                        + int(pieces[i]),
                        dealer=request.user,
                    )

            else:
                messages.info(
                    request, f"{product_names[i]} প্রডাক্টি পাওয়া যাইনি।",
                )

        messages.success(
            request, f"প্রোডাক্টগুলো সফলভাবে আপডেট হয়েছে।",
        )
        return redirect("dealer:home")


class ProductListView(CustomUserPassesTestMixin, ListView):
    user_type = "is_dealer"

    model = Product
    template_name = "dealer_product_stock.html"
    context_object_name = "products"
    paginate_by = 10

    def get_queryset(self):
        return Product.objects.filter(dealer=self.request.user).order_by("id")


class DSRList(CustomUserPassesTestMixin, ListView):
    user_type = "is_dealer"

    model = DealerRepresentative
    template_name = "dealer_dsr_list.html"
    context_object_name = "dsrs"
    paginate_by = 10

    def get_queryset(self):
        return DealerRepresentative.objects.filter(dealer=self.request.user).order_by(
            "id"
        )


class DSRRequest(CustomUserPassesTestMixin, View):
    user_type = "is_dealer"
    template_name = "dsr_profile.html"

    def get(self, request):
        user_form = DSRUserForm()
        user_info_form = DSRUserInfoForm()
        data = {"forms": [user_form, user_info_form]}
        return render(request, template_name=self.template_name, context=data)

    def post(self, request):
        user_form = DSRUserForm(request.POST)
        user_info_form = DSRUserInfoForm(request.POST, request.FILES)
        if user_form.is_valid() and user_info_form.is_valid():
            user = user_form.save(commit=False)
            user.is_delivery_sales_representative = True
            user.is_active = False
            user.save()
            info = user_info_form.save(commit=False)
            info.user = user
            info.save()
            dsr_relation = DealerRepresentative.objects.get_or_create(
                dealer=request.user, representative=user, status="requested"
            )
            messages.success(request, "নতুন ইউজার তৈরি হয়েছে।")
            return redirect("dealer:dsr-list")
        else:
            data = {"forms": [user_form, user_info_form]}
            for field, errors in user_form.errors.items():
                error_messages = ", ".join(errors)
                messages.error(request, f"{error_messages}")
            for field, errors in user_info_form.errors.items():
                error_messages = ", ".join(errors)
                messages.error(request, f"{error_messages}")
            return render(request, template_name=self.template_name, context=data)


class DSRDetails(CustomUserPassesTestMixin, View):
    user_type = "is_dealer"
    template_name = "dealer_dsr_details.html"

    def get(self, request, pk):
        representative = DealerRepresentative.objects.get(pk=pk)
        dsr_sales_queryset_for_all_date = DSRSales.objects.filter(
            dsr=representative.representative
        )
        agg_data = dsr_sales_queryset_for_all_date.values("dsr").aggregate(
            total_selling_price_sum=Sum("total_selling_price"),
            paid_amount_sum=Sum("paid_amount"),
            due_amount_sum=Sum("total_selling_price")
            - Sum("discount")
            - Sum("paid_amount"),
        )

        today = timezone.now().date()

        # Filter the queryset for the representative and today
        dsr_sales_queryset_today = DSRSales.objects.filter(
            dsr=representative.representative, date=today
        )

        # Aggregate sums based on the dsr field
        agg_data_today = dsr_sales_queryset_today.aggregate(
            total_selling_price_sum=Sum("total_selling_price"),
            paid_amount_sum=Sum("paid_amount"),
            due_amount_sum=Sum("total_selling_price")
            - Sum("discount")
            - Sum("paid_amount"),
        )

        sales_info = {
            "total_selling_price_sum_today": agg_data_today.get(
                "total_selling_price_sum", 0
            )
            if agg_data_today.get("total_selling_price_sum", 0)
            else 0,
            "paid_amount_sum_today": agg_data_today.get("paid_amount_sum", 0)
            if agg_data_today.get("paid_amount_sum", 0)
            else 0,
            "due_amount_sum_today": agg_data_today.get("due_amount_sum", 0)
            if agg_data_today.get("due_amount_sum", 0)
            else 0,
            "total_selling_price_sum": agg_data.get("total_selling_price_sum", 0)
            if agg_data.get("total_selling_price_sum", 0)
            else 0,
            "paid_amount_sum": agg_data.get("paid_amount_sum", 0)
            if agg_data.get("paid_amount_sum", 0)
            else 0,
            "due_amount_sum": agg_data.get("due_amount_sum", 0)
            if agg_data.get("due_amount_sum", 0)
            else 0,
        }
        return render(
            request,
            template_name=self.template_name,
            context={"representative": representative, "sales_info": sales_info},
        )


class DSRProductVanLoad(CustomUserPassesTestMixin, View):
    user_type = "is_dealer"
    template_name = "dealer_dsr_van_load.html"

    def get(self, request, pk):
        representative = DealerRepresentative.objects.get(pk=pk)
        return render(
            request,
            template_name=self.template_name,
            context={"representative": representative},
        )

    def post(self, request, pk):
        representative = DealerRepresentative.objects.get(pk=pk)
        post_data = request.POST
        product_ids = post_data.getlist("product_id")
        product_names = post_data.getlist("product_name")
        returns = post_data.getlist("return")
        receives = post_data.getlist("receive")

        for i in range(0, len(product_ids)):
            product = Product.objects.filter(id=product_ids[i]).first()
            if product is not None and int(returns[i]) + int(receives[i]) > 0:
                total_quantity = int(returns[i]) + int(receives[i])
                if total_quantity > product.stock.quantity:
                    messages.error(
                        request,
                        f"{product.name} has received {total_quantity} is out of stock.",
                    )
                    return redirect("dealer:dsr-product-van-load", pk=pk)
                dsr_wallet_obj, created = DSRProductWallet.objects.get_or_create(
                    dsr_product=product, dsr=representative.representative
                )
                dsr_wallet_obj.quantity += total_quantity
                dsr_wallet_obj.returned_quantity = 0
                dsr_wallet_obj.save()
                dsr_voucher = DSRVoucher.objects.create(
                    product=product,
                    quantity=total_quantity,
                    price=total_quantity * product.dealer_selling_price,
                    dsr=representative.representative,
                )
                product.stock.quantity -= total_quantity
                product.stock.save()
                product.save()
        messages.success(request, f"ভ্যানে লোড হয়েছে সফলভাবে।")
        return redirect("dealer:dsr-details", pk=pk)


class DSRProductForAPI(CustomUserPassesTestMixin, View):
    user_type = "is_dealer"

    def get(self, request, pk):
        path = request.path
        # print(path)
        dsr = DealerRepresentative.objects.get(pk=pk)
        dealer = CustomUser.objects.get(pk=request.user.pk)
        products = Product.objects.filter(dealer=dealer).order_by("id")
        data = []
        for product in products:
            dsr_wallet = DSRProductWallet.objects.filter(
                dsr_product=product, dsr=dsr.representative
            ).first()
            temp = {
                "id": product.id,
                "productName": product.name,
                "stock": product.stock.quantity
                if "dsr-return-product" not in path
                else dsr_wallet.quantity
                if dsr_wallet
                else 0,
                "returnProduct": dsr_wallet.returned_quantity if dsr_wallet else 0,
            }
            data.append(temp)
        return JsonResponse(data, safe=False)


class DSRReturnProduct(CustomUserPassesTestMixin, View):
    user_type = "is_dealer"
    template_name = "dealer_dsr_return_product.html"

    def get(self, request, pk):
        representative = DealerRepresentative.objects.get(pk=pk)
        return render(
            request,
            template_name=self.template_name,
            context={"representative": representative},
        )

    def post(self, request, pk):
        representative = DealerRepresentative.objects.get(pk=pk)
        dealer = CustomUser.objects.get(pk=request.user.pk)
        post_data = request.POST
        product_ids = post_data.getlist("product_id")
        product_names = post_data.getlist("product_name")
        returns = post_data.getlist("return")
        damage = post_data.getlist("damage")
        total_price = 0
        for i in range(0, len(product_ids)):
            product = Product.objects.filter(id=product_ids[i]).first()
            if product:

                damage_product_quantity = int(damage[i])
                return_product_quantity = int(returns[i])

                if return_product_quantity >= 0 or damage_product_quantity >= 0:
                    if damage_product_quantity > 0:
                        damage_product_obj = DamageStock.objects.create(
                            dealer=dealer,
                            dsr=representative.representative,
                            product=product,
                            quantity=damage_product_quantity,
                        )
                    dsr_wallet_obj = DSRProductWallet.objects.filter(
                        dsr=representative.representative, dsr_product=product
                    ).first()
                    if dsr_wallet_obj:
                        sold_product_quantity = (
                            dsr_wallet_obj.quantity
                            - return_product_quantity
                            - damage_product_quantity
                        )
                        dsr_wallet_obj.quantity -= dsr_wallet_obj.quantity - (
                            return_product_quantity + damage_product_quantity
                        )
                        dsr_wallet_obj.returned_quantity = return_product_quantity
                        dsr_wallet_obj.dsr_product.stock.quantity += (
                            return_product_quantity
                        )
                        dsr_wallet_obj.dsr_product.stock.save()
                        dsr_wallet_obj.dsr_product.save()
                        dsr_wallet_obj.save()
                        dsr_selling_voucher = DSRSellingVoucher.objects.create(
                            dsr=representative.representative,
                            product=dsr_wallet_obj,
                            sold_quantity=sold_product_quantity,
                            returned_product=return_product_quantity,
                            damage_product=damage_product_quantity,
                        )
                        total_price += dsr_selling_voucher.get_sold_price

        if total_price > 0:
            dsr_sales = DSRSales.objects.create(
                dsr=representative.representative, total_selling_price=total_price
            )

            messages.success(request, f"ভ্যানে লোড হয়েছে সফলভাবে।")
            return redirect("dealer:dsr-calculation-individual", pk=dsr_sales.id)
        else:
            messages.error(request, "Your sales is zero")
            return redirect("dealer:dsr-details", pk=representative.pk)


class DSRProductWalletView(CustomUserPassesTestMixin, ListView):
    user_type = "is_dealer"

    model = Product
    template_name = "dsr_product_wallet.html"
    context_object_name = "products"
    paginate_by = 10

    def get_queryset(self):
        dsr_id = self.kwargs.get("pk", None)
        if dsr_id is not None:
            return DSRProductWallet.objects.filter(dsr_id__exact=dsr_id).order_by("id")


class DSRIndividualCalculationView(CustomUserPassesTestMixin, View):
    user_type = "is_dealer"
    template_name = "dealer_dsr_calculation_individual.html"

    def get(self, request, *args, **kwargs):
        dealer_sales_id = self.kwargs.get("pk", None)
        dsr_sales = DSRSales.objects.filter(id=dealer_sales_id).first()

        form = DSRIndividualCollectionForm(
            initial={"total_bill": dsr_sales.total_selling_price}
        )

        return render(
            request, template_name=self.template_name, context={"form": form},
        )

    def post(self, request, *args, **kwargs):
        pk = self.kwargs.get("pk", None)
        dsr_sale = DSRSales.objects.filter(id=pk).first()

        form = DSRIndividualCollectionForm(
            request.POST, initial={"total_bill": dsr_sale.total_selling_price}
        )
        representative = DealerRepresentative.objects.filter(
            dealer=request.user, representative_id__exact=dsr_sale.dsr.id
        ).first()

        if form.is_valid():
            # print(form.cleaned_data)
            total_bill = form.cleaned_data.get("total_bill")
            discount = form.cleaned_data.get("discount")
            deposit = form.cleaned_data.get("totalDeposit")
            net_bill = form.cleaned_data.get("net_bill")
            collection_obj = DSRCollections.objects.create(
                dsr=dsr_sale.dsr, collected_amount=deposit
            )
            dsr_sale.discount = discount
            # dsr_sale.save()

            payable_amount = dsr_sale.get_payable_amount
            due_amount = dsr_sale.get_due_amount
            if due_amount > 0 and deposit > 0:
                if deposit - payable_amount == 0:
                    dsr_sale.paid_amount += payable_amount
                    deposit -= payable_amount
                elif deposit - payable_amount <= 0:
                    dsr_sale.paid_amount += deposit
                    deposit -= deposit
                else:
                    messages.error(request, f"জমার টাকা বিলের থেকে বেশি।")
                    return render(
                        request,
                        template_name=self.template_name,
                        context={"form": form},
                    )
                dsr_sale.save()

            return redirect("dealer:dsr-details", pk=representative.id)
        else:
            # print(form.errors)
            for field, errors in form.errors.items():
                for error in errors:
                    print(error)
                    messages.error(request, f"{error}")
            return render(
                request, template_name=self.template_name, context={"form": form},
            )


class DSRCalculationView(CustomUserPassesTestMixin, View):
    user_type = "is_dealer"
    template_name = "dealer_dsr_calculation.html"

    def get(self, request, pk, *args, **kwargs):
        dsr_id = self.kwargs.get("pk", None)
        dsr_sales = DSRSales.objects.filter(dsr_id__exact=dsr_id)
        total_due_amount = 0

        for sale in dsr_sales:
            total_due_amount += sale.get_due_amount

        form = CollectionForm(initial={"prevDue": total_due_amount})

        return render(
            request, template_name=self.template_name, context={"form": form},
        )

    def post(self, request, pk, *args, **kwargs):
        dsr_id = self.kwargs.get("pk", None)
        representative = DealerRepresentative.objects.filter(
            dealer=request.user, representative_id__exact=dsr_id
        ).first()
        dsr_sales = DSRSales.objects.filter(dsr_id__exact=dsr_id).order_by("-date")
        total_due_amount = 0

        for sale in dsr_sales:
            total_due_amount += sale.get_due_amount

        form = CollectionForm(request.POST, initial={"prevDue": total_due_amount})

        if form.is_valid():
            prev_due = form.cleaned_data.get("prevDue")
            total_deposit = form.cleaned_data.get("totalDeposit")
            collection_obj = DSRCollections.objects.create(
                dsr=representative.representative, collected_amount=total_deposit
            )
            for sale in dsr_sales:
                payable_amount = sale.get_payable_amount
                due_amount = sale.get_due_amount
                if due_amount > 0 and total_deposit > 0:
                    if total_deposit - payable_amount >= 0:
                        sale.paid_amount += payable_amount
                        total_deposit -= payable_amount
                    else:
                        sale.paid_amount += total_deposit
                        total_deposit -= total_deposit
                    sale.save()

            return redirect("dealer:dsr-details", pk=representative.id)
        else:
            # Access individual error messages
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{error}")
            return render(
                request, template_name=self.template_name, context={"form": form},
            )
