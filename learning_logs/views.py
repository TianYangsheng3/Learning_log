from django.shortcuts import render
from django.http import HttpResponseRedirect,Http404
from django.contrib.auth.decorators import login_required
# from django.core.urlresolvers import reverse

from .models import Topic,Entry
from .forms import TopicForm,EntryForm
# Create your views here.
def index(request):
    return render(request,'learning_logs/index.html')

@login_required
def topics(request):
    """show all topics"""
    topics = Topic.objects.filter(owner = request.user).order_by('date_added')
    context = {'topics':topics}
    return render(request, 'learning_logs/topics.html', context)

@login_required
def topic(request, topic_id):
    """show all items of specific topic"""
    topic = Topic.objects.get(id=topic_id)
    if request.user != topic.owner:
        raise Http404

    entries = topic.entry_set.order_by('-date_added')
    context = {'topic':topic, 'entries':entries}
    return render(request, 'learning_logs/topic.html', context)

@login_required
def new_topic(request):
    """add new topic"""
    if request.method != 'POST':
        form = TopicForm()
    else:
        form = TopicForm(request.POST)
        if form.is_valid():
            new_topic = form.save(commit = False)
            new_topic.owner = request.user
            new_topic.save()
            return HttpResponseRedirect('/topics/')
    context = {'form':form}
    return render(request, 'learning_logs/new_topic.html',context)

@login_required
def new_entry(request, topic_id):
    """add new item of the topic"""
    topic = Topic.objects.get(id=topic_id)

    if request.method != 'POST':
        form = EntryForm()
    else:
        form = EntryForm(data = request.POST)
        if form.is_valid():
            new_entry = form.save(commit = False)
            new_entry.topic = topic
            new_entry.save()
            return HttpResponseRedirect('/topics/{}/'.format(topic_id))
    context = {'topic':topic, 'form':form}
    return render(request, 'learning_logs/new_entry.html',context)

@login_required       
def edit_entry(request, entry_id):
    """edit entry"""
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic

    if request.user != topic.owner:
        raise Http404

    if request.method != 'POST':
        form = EntryForm(instance=entry)
    else:
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/topics/{}'.format(topic.id))
    context = {'entry':entry, 'topic':topic, 'form':form}
    return render(request, 'learning_logs/edit_entry.html', context)      

def test(request):
    return render(request, 'learning_logs/test.html')
