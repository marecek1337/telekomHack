from django.http import JsonResponse
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
import json
import os 

def current_date(request):
    # Ensure the request is a GET request
    if request.method == 'GET':
        # Get the current date and time
        now = datetime.now()
        current_date_str = now.strftime("%Y-%m-%d %H:%M:%S")

        # Return the current date and time in a JSON response
        return JsonResponse({'current_date': current_date_str})
    else:
        # If the request is not a GET, return a 405 Method Not Allowed error
        return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def get_info(request):
    """
    Vracia jednoduchý text ako jednu položku v JSON formáte.
    """
    if request.method == 'GET':
        # Jednoduchý text ako jedna položka JSON
        info = {
            "message": "Hello, this is your single JSON response!"
        }
        return JsonResponse(info)
    else:
        # Ak nie je požiadavka typu GET
        return JsonResponse({'error': 'Method not allowed'}, status=405)

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def get_chart(request):
    """
    Vracia JavaScriptový kód na vykreslenie grafu v JSON formáte.
    """
    if request.method == 'GET':
        # JavaScriptový kód na graf
        chart_code = """
const dataset = {
  labels: ["1/22/20", "1/23/20", "1/24/20", "1/25/20", "1/26/20", "1/27/20", "1/28/20", "1/29/20", "1/30/20", "1/31/20", "2/1/20", "2/2/20", "2/3/20", "2/4/20", "2/5/20", "2/6/20", "2/7/20", "2/8/20", "2/9/20", "2/10/20", "2/11/20", "2/12/20", "2/13/20", "2/14/20", "2/15/20", "2/16/20", "2/17/20", "2/18/20", "2/19/20", "2/20/20", "2/21/20", "2/22/20", "2/23/20", "2/24/20", "2/25/20", "2/26/20", "2/27/20", "2/28/20", "2/29/20", "3/1/20", "3/2/20", "3/3/20", "3/4/20", "3/5/20", "3/6/20", "3/7/20", "3/8/20", "3/9/20"],
  datasets: [
    {
      label: "Afghanistan",
      data: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
      fill: false,
      borderColor: "red"
    },
    {
      label: "Albania",
      data: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
      fill: false,
      borderColor: "blue"
    },
    {
      label: "Algeria",
      data: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
      fill: false,
      borderColor: "green"
    }
  ]
};

const ctx = document.getElementById("myChart").getContext("2d");
const myChart = new Chart(ctx, {
  type: "line",
  data: dataset,
  options: {
    responsive: true,
    plugins: {
      title: {
        display: true,
        text: "COVID-19 Deaths"
      }
    },
    scales: {
      x: {
        display: true,
        title: {
          display: true,
          text: "Date"
        }
      },
      y: {
        display: true,
        title: {
          display: true,
          text: "Deaths"
        }
      }
    }
  }
});

        """

        # Vrátenie JavaScriptového kódu v JSON formáte
        return JsonResponse({"chart_code": chart_code})
    else:
        # Ak nie je požiadavka typu GET
        return JsonResponse({'error': 'Method not allowed'}, status=405)

