import flask
import wechat_sdk

conf = wechat_sdk.WechatConf(
	token = 'helloworld',
	encrypt_mode = 'normal'
)


app = flask.Flask(__name__)

@app.route('/')
def index():
  msg = flask.request.args.get('msg')
  return 'helloWorld! <br/>' + msg


@app.route('/wx')
def wechat():
  print 'in Wechat case!'  
 
  signature = request.args.get('signature')
  timestamp = request.args.get('timestamp')
  nonce = request.args.get('nonce')
  print 'sign = ' + signature
  wechat_instance = wechat_sdk.WechatBasic(conf=conf)
  if not wechat_instance.check_signature(signature=signature, timestamp=timestamp, nonce=nonce):
      return HttpResponseBadRequest('Verify Failed')
  else:
      if request.method == 'GET':
          response = request.GET.get('echostr', 'error')
      else:
          try:
              wechat_instance.parse_data(request.body)    
              message = wechat_instance.get_message()            
              if isinstance(message, TextMessage):            
                  reply_text = 'text'
              elif isinstance(message, VoiceMessage):            
                  reply_text = 'voice'
              elif isinstance(message, ImageMessage):            
                  reply_text = 'image'
              elif isinstance(message, LinkMessage):            
                  reply_text = 'link'
              elif isinstance(message, LocationMessage):        
                  reply_text = 'location'
              elif isinstance(message, VideoMessage):            
                  reply_text = 'video'
              elif isinstance(message, ShortVideoMessage):    
                  reply_text = 'shortvideo'
              else:
                  reply_text = 'other'
              response = wechat_instance.response_text(content=reply_text)
          except ParseError:    
              return HttpResponseBadRequest('Invalid XML Data')
      return HttpResponse(response, content_type="application/xml")


if __name__ == '__main__':
  app.run(host = '0.0.0.0', port = 80)
