import json
import os

from django.conf import settings
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse
from django.utils import timezone
from django.core.files import File

from farmhash import Fingerprint32
from .make_image import decode_puzzle, save_img_with_encoded_puzzle
from .models import UserPuzzle

# Create your views here.

timezone.activate('Asia/Seoul')

required_keys = [
    'puzzle_name',
    'puzzle_description',
    'user_name',
    'encoded_hint',
    'encoded_puzzle'
]

@csrf_exempt
def upload_request(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        print(data)
        if all(req_key in data.keys() for req_key in required_keys):
            print(data['encoded_puzzle'])
            board = decode_puzzle(data['encoded_puzzle'])
            for x in board:
                print(x)

            current_date = timezone.now()
            puzzle = UserPuzzle(
                puzzle_name=data['puzzle_name'],
                puzzle_description=data['puzzle_description'],
                user_name=data['user_name'],
                upload_date=current_date,
                encoded_hint=data['encoded_hint']
            )
            hash_str = [
                str(data['puzzle_name']),
                str(data['user_name']),
                str(current_date),
                str(data['encoded_hint']),
            ]
            hashed_str = str(Fingerprint32("_".join(hash_str)))
            puzzle.puzzle_hash = hashed_str

            temp_img_dir = save_img_with_encoded_puzzle(data['encoded_puzzle'], hashed_str)
            if temp_img_dir != "":
                img_file = File(open(temp_img_dir, 'rb'))
                puzzle.puzzle_image.save(os.path.basename(temp_img_dir), img_file)
                puzzle.save()
                return HttpResponse("Success")
        return HttpResponse("Failed")
    return HttpResponseForbidden()


def get_list(request, num: int = 10, last_id: int = None):
    puzzle_list = []
    puzzle_dict = {}

    if not last_id == None:
        try:
            last_puzzle = UserPuzzle.objects.get(id=last_id)
        except UserPuzzle.DoesNotExist:
            return JsonResponse({}, status=200)
        
        puzzles_after_last_id = UserPuzzle.objects.filter(upload_date__lt=last_puzzle.upload_date).order_by("-upload_date")[:num]
        puzzle_list = list(puzzles_after_last_id.values())
    else:
        puzzles = UserPuzzle.objects.all().order_by('-upload_date')[:num]
        puzzle_list = list(puzzles.values())

    for i in range(len(puzzle_list)):
        puzzle_dict[i] = puzzle_list[i]
        if 'puzzle_image' in puzzle_dict[i]:
            puzzle_dict[i]['puzzle_image'] = os.path.join(settings.MEDIA_URL, puzzle_dict[i]['puzzle_image'])
        if 'upload_date' in puzzle_dict[i]:
            puzzle_dict[i]['upload_date'] = puzzle_dict[i]['upload_date'].strftime('%Y-%m-%d')
    
    return JsonResponse(puzzle_dict)