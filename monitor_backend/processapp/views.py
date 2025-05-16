from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import ProcessData, SystemInfo
from .serializers import ProcessDataSerializer
from django.utils import timezone

API_KEY = "1234567890abcdef"
    
class ReceiveAgentData(APIView):
    def post(self, request):
        system = request.data.get("system")
        print(system)
        processes = request.data.get("processes")

        if not system or not processes:
            return Response({"error": "Invalid format"}, status=400)

        # Upsert system info
        system_obj, _ = SystemInfo.objects.update_or_create(
            hostname=system["hostname"],
            defaults={
                "os": system["os"],
                "cpu": system["cpu"],
                "cpu_threads": system.get("cpu_threads"),
                "cpu_cores": system.get("cpu_cores"),
                "ram_total": system["ram_total"],
                "ram_available": system.get("ram_available"),
                "ram_used": system.get("ram_used"),
                "ram_free": system.get("ram_free"),
                "storage_total": system["storage_total"],
                "storage_free": system["storage_free"],
            }
        )

        # Replace process list for this host
        ProcessData.objects.filter(hostname=system["hostname"]).delete()

        for proc in processes:
            ProcessData.objects.create(
                hostname=system["hostname"],
                process_name=proc["process_name"],
                pid=proc["pid"],
                ppid=proc["ppid"],
                cpu_usage=proc["cpu_usage"],
                memory_usage=proc["memory_usage"],
            )

        return Response({"status": "success"})


class GetAllData(APIView):
    def get(self, request):
        all_data = []

        for sys in SystemInfo.objects.all():
            proc_qs = ProcessData.objects.filter(hostname=sys.hostname)
            # print(proc_qs)
            for proc in proc_qs:
                # print(proc)
                all_data.append({
                    "hostname": sys.hostname,
                    "os": sys.os,
                    "cpu": sys.cpu,
                    "cpu_threads": sys.cpu_threads,
                    "cpu_cores": sys.cpu_cores,
                    "ram_available": sys.ram_available,
                    "ram_used": sys.ram_used,
                    "ram_free": sys.ram_free,
                    "ram_total": sys.ram_total,
                    "storage_total": sys.storage_total,
                    "storage_free": sys.storage_free,
                    "process_name": proc.process_name,
                    "pid": proc.pid,
                    "ppid": proc.ppid,
                    "cpu_usage": proc.cpu_usage,
                    "memory_usage": proc.memory_usage,
                })

        return Response(all_data)
    
from django.shortcuts import render

def index(request):
    print(request)
    return render(request, 'process.html')
