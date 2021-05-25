from django import forms
from .models import Comment, Post
from django.db.models import Q

class CommentForm(forms.ModelForm):
    content = forms.CharField(required=True, widget=forms.Textarea(attrs={'class':"comment-input", 'placeholder':'write a comment', 'maxlength':500, 'rows':3}))

    class Meta:
        model= Comment
        fields = ['content']
        
        
class SearchForm(forms.Form):
    title = forms.CharField(required=False)
    tag = forms.CharField(required=False)
    author = forms.CharField(required=False)
    
    def return_query(self):
        data= super().clean()
        query = Post.objects.filter(Q(title__icontains=data['title']),
                                    Q(user__username__icontains=data['author']),
                                    Q(tags__name__icontains=data['tag']))
        print(query)
        return query
    # Q(title__icontains=data['title']) | Q(user_username__useprofile__username__icontains=data['author'])
    
    
class PostCreateForm(forms.ModelForm):
    
    class Meta:
        model = Post
        fields = ['title','content','picture', 'tags' ]
        
        widgets = {
            "title": forms.TextInput(attrs={"class": "input-prof", "placeholder": "Enter post title"}),
            "picture": forms.FileInput(attrs={"class": "input-prof", "placeholder": "Select a post picture"}),
            "tags" : forms.SelectMultiple(attrs={'class':"input-prof"}),
            "content": forms.Textarea(
                attrs={"class": "input-prof", "placeholder": "Enter post description", "rows":7 ,
                       'resize': 'none'}),
        }