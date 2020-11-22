import tweepy

class MyStreamListener( tweepy.StreamListener ):

    def on_direct_message(self, status):
        author = status.author.screen_name
        api.send_direct_message(screen_name=author, text='response')

        return True

    def on_status(self, status):

        author = status.author.screen_name
        statusID = status.id

        print(status.text + "\n")

        api.update_status('response')
        api.send_direct_message(screen_name='my username', text='Just sent a Tweet')

        return True

    def on_data(self, status):
        print('Entered on_data()')
        print(status)

        return True

    def on_error(self, status_code):
        print("Error Code: " + str(status_code))
        if status_code == 420:
            return False
        else:
            return True

    def on_timeout(self):
        print('Timeout...')
        return True