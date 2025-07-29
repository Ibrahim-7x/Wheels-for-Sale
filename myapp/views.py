import os
import uuid
import pandas as pd
from django.db import transaction
from django.conf import settings
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Test_Bulk, Test_CallPool


def main(request):
    """Render the main uploader page."""
    return render(request, "uploader.html")


@require_POST
def upload_file(request):
    if not request.FILES.get("file"):
        return JsonResponse({"error": "No file uploaded"}, status=400)
    
    uploaded_file = request.FILES["file"]
    
    if not uploaded_file.name.lower().endswith(('.xls', '.xlsx')):
        return JsonResponse({"error": "Only Excel files (.xls, .xlsx) are allowed"}, status=400)
    
    unique_filename = f"{uuid.uuid4().hex}_{uploaded_file.name}"
    file_path = os.path.join(settings.MEDIA_ROOT, unique_filename)
    
    os.makedirs(settings.MEDIA_ROOT, exist_ok=True)
    
    with open(file_path, "wb") as f:
        for chunk in uploaded_file.chunks():
            f.write(chunk)

    try:
        with transaction.atomic():
            df = pd.read_excel(file_path)
            
            if df.empty:
                return JsonResponse({"error": "The Excel file is empty"}, status=400)
            
            required_columns = ["StartTime", "Hangup Time", "Cli", "Call Staus", 
                               "Total Talk Time", "LoginId", "Citrix ID"]
            
            missing_columns = [col for col in required_columns if col not in df.columns]
            if missing_columns:
                return JsonResponse({
                    "error": f"Missing required columns: {', '.join(missing_columns)}"
                }, status=400)
            
            records_created = 0
            for _, row in df.iterrows():
                Test_Bulk.objects.create(
                    start_time=row.get("StartTime", ""),
                    hangUp_time=row.get("Hangup Time", ""),
                    cli=row.get("Cli", ""),
                    call_status=row.get("Call Staus", ""),
                    talk_time=row.get("Total Talk Time", ""),
                    login_id=row.get("LoginId", ""),
                    citrix_id=row.get("Citrix ID", ""),
                )
                records_created += 1

        return JsonResponse({
            "message": f"File uploaded and {records_created} records processed successfully!"
        })

    except Exception as e:
        if os.path.exists(file_path):
            os.remove(file_path)
        return JsonResponse({"error": f"Data processing failed: {str(e)}"}, status=500)


@require_POST
def pick_calls(request):
    try:
        import json
        data = json.loads(request.body)
        num_calls_per_citrix = int(data.get("num_calls_per_citrix", 0))

        if num_calls_per_citrix <= 0:
            return JsonResponse({"error": "Number of calls must be positive"}, status=400)

        total_calls_added = 0

        with transaction.atomic():
            citrix_ids = Test_Bulk.objects.values_list("citrix_id", flat=True).distinct()

            if not citrix_ids:
                return JsonResponse({"message": "No Citrix IDs found in the system"}, status=200)

            for citrix_id in citrix_ids:
                if not citrix_id:
                    continue

                # ✅ Always pick N new unpicked calls regardless of Pool count
                available_calls = Test_Bulk.objects.filter(
                    citrix_id=citrix_id,
                    call_picked=False
                )[:num_calls_per_citrix]

                print(f"[DEBUG] Found {available_calls.count()} unpicked calls for {citrix_id}")

                for call in available_calls:
                    # ✅ Prevent picking the same call twice
                    if not Test_CallPool.objects.filter(bulk_table=call).exists():
                        Test_CallPool.objects.create(
                            bulk_table=call,
                            citrix_id=call.citrix_id,
                        )

                        call.call_picked = True
                        call.save()

                        total_calls_added += 1

        if total_calls_added > 0:
            return JsonResponse({
                "message": f"✅ Added {total_calls_added} new calls across {len(citrix_ids)} Citrix IDs"
            })
        else:
            return JsonResponse({
                "message": "No new calls were added. All available calls have already been picked."
            })

    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON data"}, status=400)
    except ValueError as e:
        return JsonResponse({"error": f"Value error: {str(e)}"}, status=400)
    except Exception as e:
        return JsonResponse({"error": f"An error occurred: {str(e)}"}, status=500)

