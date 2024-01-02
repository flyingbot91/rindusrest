from django.test import TestCase

from api.models import Comment, Post


class PostTestCase(TestCase):

    def setUp(self):
        _ = Post.objects.create(
            body='foobar',
            title='foobar'
        )

    def test_post(self):
        post = Post.objects.last()
        self.assertEqual(post.body, 'foobar')
        self.assertEqual(post.title, 'foobar')
        self.assertEqual(post.user_id, 99999942)


class CommentTestCase(TestCase):

    def setUp(self):
        post = Post.objects.create(
            body='foobar',
            title='foobar'
        )
        _ = Comment.objects.create(
            body='foobar',
            name='foobar',
            email='foo@bar.com',
            post=post,
        )

    def test_comments(self):
        comment = Comment.objects.last()
        #self.assertEqual(comment.name, "foobar")
