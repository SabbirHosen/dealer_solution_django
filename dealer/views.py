from django.contrib import messages
from django.db.models import F, ExpressionWrapper, PositiveIntegerField
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView
from django.http import JsonResponse
from authentication.mixins import CustomUserPassesTestMixin
from authentication.strings.string import UNIT_CHOICES
from .models import DealerExpense, Product, Stock, Voucher
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
        return render(
            request,
            template_name=self.template_name,
            context={"expanses_name": self.expenses_obj},
        )

    def post(self, request):
        image_input = request.FILES.get("expenseImage")
        type_of_expense = request.POST.get("productSelected")
        paid_amount_input = request.POST.get("paidAmount")
        date_input = request.POST.get("datePicker")
        comments_input = request.POST.get("comment")
        expense_obj = ExpenseName.objects.filter(id=type_of_expense).first()
        if type_of_expense is None or expense_obj is None:
            messages.error(request, "খরচের ধরণ সিলেক্ট করুন !")
            data = {
                "expanses_name": self.expenses_obj,
                "expenseImage": image_input,
                "paidAmount": paid_amount_input,
                "comment": comments_input,
                "datePicker": date_input,
            }
            return render(request, template_name=self.template_name, context=data)
        if image_input:
            obj = DealerExpense.objects.create(
                image=image_input,
                name=expense_obj,
                paid_amount=paid_amount_input,
                date=date_input,
                comments=comments_input,
                dealer=request.user,
            )
        else:
            obj = DealerExpense.objects.create(
                name=expense_obj,
                paid_amount=paid_amount_input,
                date=date_input,
                comments=comments_input,
                dealer=request.user,
            )
        obj.save()
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
            if not product_obj:
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
                    price=product_total_price,
                )
                messages.success(request, "প্রডাক্ট সফলভাবে অ্যাড হয়েছে !")
                return redirect("dealer:dealer-product-upload")
            else:
                messages.info(
                    request,
                    "প্রডাক্টি আগে অ্যাড করা হয়েছে। পরিমাণ আপডেটের জন্য আপডেট পেজে যান!",
                )
                return render(request, self.template_name, context=product_info)


class ProductListViewForAPI(CustomUserPassesTestMixin, ListView):
    user_type = "is_dealer"
    model = Product
    # template_name = "product_list.html"  # This can be any template or an empty string.
    context_object_name = "products"

    def get_queryset(self):
        # Select the required fields and rename 'dealer_buying_price' to 'price'
        return Product.objects.values(
            "id", "name", "factor", price=F("dealer_buying_price")
        )

    def render_to_response(self, context, **response_kwargs):
        # Convert the queryset to a list of dictionaries
        product_data = list(self.get_queryset())

        # Return the data as JSON
        return JsonResponse(product_data, safe=False, json_dumps_params={"indent": 4})


class ProductBulkUpload(CustomUserPassesTestMixin, View):
    user_type = "is_dealer"
    # template_name = "bulk_product_upload.html"

    # def get(self, request):
    #     return render(request=request, template_name=self.template_name)
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
                        price=int(
                            int(cartons[i]) * product_object.factor + int(pieces[i])
                        )
                        * product_object.dealer_buying_price,
                    )

            else:
                messages.info(
                    request, f"{product_names[i]} প্রডাক্টি পাওয়া যাইনি।",
                )
            # data_list.append(item_dict)
        messages.success(
            request, f"প্রোডাক্টগুলো সফলভাবে আপডেট হয়েছে।",
        )
        return redirect("dealer:home")


class ProductListView(ListView):
    model = Product
    template_name = "dealer_product_stock.html"  # Change this to your desired template
    context_object_name = "products"
    paginate_by = 10

    def get_queryset(self):
        # # Define the fields you want to retrieve from the Product and Stock models
        # fields = [
        #     "name",
        #     "company",
        #     "factor",
        #     "dealer_buying_price",
        #     "dealer_selling_price",
        # ]
        #
        # # Retrieve the data and calculate the formatted quantity from Stock
        # queryset = (
        #     Product.objects.select_related("stock")
        #     .annotate(
        #         quantity_formatted=ExpressionWrapper(
        #             F("stock__quantity") % F("factor"),
        #             output_field=PositiveIntegerField(),
        #         ),
        #     )
        #     .values(*fields, "quantity_formatted")
        # )
        # print(queryset)
        #
        # obj = Product.objects.filter(dealer=self.request.user).values(
        #     "name", "stock__quantity", "get_quantity_by_format"
        # )
        # print(obj)
        return Product.objects.filter(dealer=self.request.user)
