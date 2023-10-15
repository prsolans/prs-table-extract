from django.shortcuts import render, redirect
from table_extraction.forms import DocumentForm
from django.http import HttpResponse
from docx import Document
from .models import Document
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import generics
from .serializers import TableDataSerializer, DocumentSerializer
import json


def index(request):
    context = {
        "title": "Django example",
    }
    return render(request, "index.html", context)


def parse_word_document(file_path):
    doc = Document(file_path)
    return doc

def extract_table_data(doc):
    tables_data = []

    for table in doc.tables:
        table_data = []
        for row in table.rows:
            row_data = []
            for cell in row.cells:
                row_data.append(cell.text)
            table_data.append(row_data)
        tables_data.append(table_data)

    return tables_data

def upload_doc(request):
    print(request)
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save()  # Save the uploaded file instance
            doc = parse_word_document(instance.upload.path)
            tables_data = extract_table_data(doc)

            json_string_1 = json.dumps(tables_data[0], indent=4)
            json_string_2 = json.dumps(tables_data[1], indent=4)

            # Do something with tables_data, e.g., send it to a template, save it to DB, etc.
            return render(request, 'results.html', {'data_table': json_string_1, 'data_table2' : json_string_2})
            # return redirect('some_view_name')
    else:
        form = DocumentForm()

    return render(request, 'upload.html', {'form': form})

def results(request):
    context = {
        "title": "Data Results",
    }
    return render(request, "results.html", context)

@api_view(['POST'])
def table_extraction_api(request):
    if request.method == 'POST':
        word_file = request.FILES.get('document')
        table_data = upload_doc(word_file)  # your logic to extract tables
        serializer = TableDataSerializer(data={'data': table_data})

        if serializer.is_valid():
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=400)

class DocumentAPI(generics.CreateAPIView):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer

    def perform_create(self, serializer):
        instance = serializer.save()
        doc = parse_word_document(instance.upload.path)
        tables_data = extract_table_data(doc)
        # Process the tables_data or add to the model as needed
