import json
# from .configSetting import SECRETID,SECRETKEY
from utils.configSetting import SECRETID,SECRETKEY
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.ocr.v20181119 import ocr_client, models


def id_cardOCR(image_base64):
    
    """
    识别身份证人像面的文字识别，返回身份证上的文字信息. Authority and ValidDate 为空
    识别身份证国徽面的文字识别，Authority and ValidDate 有值其他为空

    :param image_base64: 传入图片的 base64格式  注意：需要去掉相关前缀data:image/jpg;base64,和换行符\n。
    :return: dict
    Name: 	String	姓名（人像面）
    Sex:	String	性别（人像面）
    Nation:	String	民族（人像面）
    Birth:	String	出生日期（人像面）
    Address:	String	地址（人像面）
    IdNum:	String	身份证号（人像面）
    Authority:	String	发证机关（国徽面）
    ValidDate:	String	证件有效期（国徽面）
    """
    try:
        cred = credential.Credential(SECRETID, SECRETKEY)
        httpProfile = HttpProfile()
        httpProfile.endpoint = "ocr.tencentcloudapi.com"

        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile
        client = ocr_client.OcrClient(cred, "ap-beijing", clientProfile)

        req = models.IDCardOCRRequest()
        params = {
            "ImageBase64": image_base64
        }
        req.from_json_string(json.dumps(params))

        resp = client.IDCardOCR(req)
        respDict = resp.__dict__
        respDict.pop('RequestId')
        return respDict

    except TencentCloudSDKException as err:
        """
        错误码：
        code:                           message:
        FailedOperation.DownLoadError	文件下载失败。
        FailedOperation.EmptyImageError	图片内容为空。
        FailedOperation.IdCardInfoIllegal	身份证信息不合法（身份证号、姓名字段校验非法等）。
        FailedOperation.ImageBlur	图片模糊。
        FailedOperation.ImageDecodeFailed	图片解码失败。
        FailedOperation.ImageNoIdCard	图片中未检测到身份证。
        FailedOperation.ImageSizeTooLarge	图片尺寸过大，请参考输出参数中关于图片大小限制的说明。
        FailedOperation.MultiCardError	照片中存在多张卡。
        FailedOperation.OcrFailed	OCR识别失败。
        FailedOperation.UnKnowError	未知错误。
        FailedOperation.UnOpenError	服务未开通。
        InvalidParameter.ConfigFormatError	Config不是有效的JSON格式。
        InvalidParameterValue.InvalidParameterValueLimit	参数值错误。
        LimitExceeded.TooLargeFileError	文件内容太大。
        """
        raise err
