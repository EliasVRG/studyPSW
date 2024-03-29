from django.shortcuts import render, redirect
from .models import Categoria, Flashcard
from django.contrib.messages import constants
from django.contrib import messages

# Create your views here.

def novo_flashcard(request):
    if not request.user.is_authenticated:
        return redirect('/usuarios/login')

    if request.method == 'GET':
        categorias = Categoria.objects.all()
        dificuldades = Flashcard.DIFICULDADE_CHOICES
        flashcards = Flashcard.objects.filter(user=request.user)

        categoria_filtrar = request.GET.get('categoria')
        dificuldade_filtrar = request.GET.get('dificuldade')

        if categoria_filtrar:
            flashcards = flashcards.filter(categoria__id=categoria_filtrar)

        if dificuldade_filtrar:
            flashcards = flashcards.filter(dificuldade=dificuldade_filtrar)
        
        return render(
            request,
            'novo_flashcard.html',
            {
                'categorias': categorias,
                'dificuldades': dificuldades,
                'flashcards': flashcards,
            }
            
        )
    
    elif request.method == "POST":
        pergunta = request.POST.get('pergunta')
        resposta = request.POST.get('resposta')
        categoria = request.POST.get('categoria')
        dificuldade = request.POST.get('dificuldade')

        if len(pergunta.strip()) == 0 or len(resposta.strip()) == 0:
            messages.add_message(
                request,
                constants.ERROR,
                'Preencha os campos de pergunta e resposta',
            )
            return redirect('/flashcard/novo_flashcard')

        flashcard = Flashcard(
            user=request.user,
            pergunta=pergunta,
            resposta=resposta,
            categoria_id=categoria,
            dificuldade=dificuldade,
        )

        flashcard.save()

        messages.add_message(
            request, constants.SUCCESS, 'Flashcard criado com sucesso'
        )
        return redirect('/flashcard/novo_flashcard')
    

def deletar_flashcard(request, id):
    try:
        flashcard = Flashcard.objects.get(id=id)
    except Flashcard.DoesNotExist:
        raise Http404("Flashcard não encontrado")

    if request.user.is_authenticated:
        # Verifica se o usuário autenticado é o proprietário do flashcard
        if flashcard.usuario == request.user:
            flashcard.delete()
            messages.add_message(
                request, constants.SUCCESS, 'Flashcard deletado com sucesso!'
            )
        else:
            messages.add_message(
                request,
                constants.ERROR,
                'Você não tem permissão para excluir este flashcard',
            )
    else:    
        messages.add_message(
            request,
            constants.ERROR,
            'Você não está logado nesta conta',
        )

    return redirect('/flashcard/novo_flashcard')