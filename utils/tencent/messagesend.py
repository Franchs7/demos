def Sendcode(phone, code):
    # -*- coding: utf-8 -*-
    from tencentcloud.common import credential
    from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
    # 导入对应产品模块的client models。
    from tencentcloud.sms.v20190711 import sms_client, models

    try:
        phone = f'+86{phone}'
        code = str(code)
        cred = credential.Credential("secretid", "secretkey")

        client = sms_client.SmsClient(cred, "ap-guangzhou")

        # 实例化一个请求对象，根据调用的接口和实际情况，可以进一步设置请求参数
        # 你可以直接查询SDK源码确定SendSmsRequest有哪些属性可以设置
        # 属性可能是基本类型，也可能引用了另一个数据结构
        # 推荐使用IDE进行开发，可以方便的跳转查阅各个接口和数据结构的文档说明
        req = models.SendSmsRequest()

        req.SmsSdkAppid = ""
        # 短信签名内容: 使用 UTF-8 编码，必须填写已审核通过的签名，签名信息可登录 [短信控制台] 查看
        req.Sign = ""
        # 短信码号扩展号: 默认未开通，如需开通请联系 [sms helper]
        req.PhoneNumberSet = [phone]
        # 模板 ID: 必须填写已审核通过的模板 ID。模板ID可登录 [短信控制台] 查看
        req.TemplateID = ""
        # 模板参数: 若无模板参数，则设置为空
        req.TemplateParamSet = [code]

        # 通过client对象调用DescribeInstances方法发起请求。注意请求方法名与请求对象是对应的。
        # 返回的resp是一个DescribeInstancesResponse类的实例，与请求对象对应。
        resp = client.SendSms(req)

        # 输出json格式的字符串回包
        print(resp.to_json_string(indent=2))

    except TencentCloudSDKException as err:
        print(err)
