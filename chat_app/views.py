from django.shortcuts import render

# Create your views here.
from firebase_admin import auth

def google_auth(request):
    token = request.POST.get("token")
    try:
        decoded_token = auth.verify_id_token(token)
        uid = decoded_token['uid']
        # The token is valid and we have the user's id
        return JsonResponse({"status": "success"})
    except Exception as e:
        return JsonResponse({"status": "failure", "message": str(e)})

from firebase_admin import firestore

def get_users(request):
    db = firestore.client()
    users_ref = db.collection("users")
    docs = users_ref.stream()

    users = [{"id": doc.id, "data": doc.to_dict()} for doc in docs]
    return JsonResponse({"users": users})

def send_message(request):
    sender = request.POST.get("sender")
    receiver = request.POST.get("receiver")
    content = request.POST.get("content")

    db = firestore.client()
    messages_ref = db.collection("messages")

    messages_ref.add({
        "sender": sender,
        "receiver": receiver,
        "content": content,
    })
    return JsonResponse({"status": "success"})


def get_messages(request):
    sender = request.GET.get("sender")
    receiver = request.GET.get("receiver")

    db = firestore.client()
    messages_ref = db.collection("messages")
    query_ref = messages_ref.where("sender", "==", sender).where("receiver", "==", receiver)

    messages = [{"id": doc.id, "data": doc.to_dict()} for doc in query_ref.stream()]
    return JsonResponse({"messages": messages})

