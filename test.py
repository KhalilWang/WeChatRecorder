import wechat_sdk

conf = wechat_sdk.WechatConf(
	token = 'helloworld',
	encrypt_mode = 'normal'
)

wechat = wechat_sdk.WechatBasic(conf = conf)


